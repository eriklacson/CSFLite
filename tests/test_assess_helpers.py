import json
import os
import sys
from pathlib import Path

import pytest

# ensure project root is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# test get_paths function
def test_get_paths():
    from tools.global_helpers import get_paths

    config_path = Path(__file__).resolve().parent.parent / "config" / "path_config.json"

    with open(config_path, encoding="utf-8") as config_file:
        expected_paths = json.load(config_file)

    assert get_paths() == expected_paths


def test_get_csf_lookup(tmp_path: Path):
    from tools.assess_helpers import get_csf_lookup

    csv_content = (
        "csf_subcategory_id,weight,recommendation\nID.AM-02,1,Assess assets\nPR.AA-03,2,Enforce access control\n"
    )
    lookup_path = tmp_path / "csf_lookup.csv"
    lookup_path.write_text(csv_content)

    result = get_csf_lookup(lookup_path)
    assert len(result) == 2
    assert result[0]["csf_subcategory_id"] == "ID.AM-02"
    assert result[1]["weight"] == 2


def test_get_csf_lookup_missing_file():
    from tools.assess_helpers import get_csf_lookup

    with pytest.raises(FileNotFoundError):
        get_csf_lookup("missing.csv")


def test_get_governance_checklist_results(tmp_path: Path):
    from tools.assess_helpers import get_governance_checklist_results

    checklist_content = (
        "csf_function,csf_subcategory_id,csf_subcategory_name,notes,response\n"
        "Identify,ID.AM-02,Assets inventoried,,yes\n"
        "Protect,PR.AA-03,Access control,need to implement ssl,partial\n"
    )
    checklist_path = tmp_path / "checklist.csv"
    checklist_path.write_text(checklist_content)

    result = get_governance_checklist_results(checklist_path)
    assert result[0]["csf_subcategory_id"] == "PR.AA-03"
    assert result[1]["response"] == "yes"


def test_get_governance_checklist_results_missing_file():
    from tools.assess_helpers import get_governance_checklist_results

    with pytest.raises(FileNotFoundError):
        get_governance_checklist_results("no-file.csv")


def test_get_governance_checklist_results_missing_columns(tmp_path: Path):
    from tools.assess_helpers import get_governance_checklist_results

    checklist_content = "csf_function,csf_subcategory_id,response\nIdentify,ID.AM-02,yes\n"
    checklist_path = tmp_path / "checklist.csv"
    checklist_path.write_text(checklist_content)

    with pytest.raises(ValueError, match=r"Missing required columns: {'csf_subcategory_name'}"):
        get_governance_checklist_results(checklist_path)


def test_generate_governance_assessment():
    from tools.assess_helpers import generate_governance_assessement

    checklist = [
        {
            "csf_subcategory_id": "ID.AM-02",
            "csf_subcategory_name": "Assets inventoried",
            "notes": "",
            "response": "Yes",
        },
        {
            "csf_subcategory_id": "PR.AA-03",
            "csf_subcategory_name": "Access control",
            "notes": "need to implement ssl",
            "response": "Partial",
        },
    ]

    lookup = [
        {
            "csf_subcategory_id": "ID.AM-02",
            "weight": 2,
            "recommendation": "Assess assets",
        },
        {
            "csf_subcategory_id": "PR.AA-03",
            "weight": 1,
            "recommendation": "Enforce access control",
        },
    ]

    result = generate_governance_assessement(checklist, lookup)

    assert len(result) == 2
    result_by_id = {r["csf_subcategory_id"]: r for r in result}
    assert result_by_id["ID.AM-02"]["assessment_score"] == "2.00"
    assert result_by_id["ID.AM-02"]["gap_score"] == "0.00"
    assert result_by_id["PR.AA-03"]["recommendation"] == "Enforce access control"
    assert result_by_id["PR.AA-03"]["assessment_score"] == "0.50"
    assert result_by_id["PR.AA-03"]["gap_score"] == "0.50"


def test_generate_governance_heatmap():
    from tools.assess_helpers import generate_governance_heatmap

    assessment = [
        {
            "csf_subcategory_id": "GV.P0-01",
            "csf_subcategory_name": "Governance roles",
            "response": "No",
            "weight": 1.0,
            "assessment_score": "0.00",
        },
        {
            "csf_subcategory_id": "PR.AA-01",
            "csf_subcategory_name": "Access control",
            "response": "Yes",
            "weight": 2.0,
            "assessment_score": "2.00",
        },
    ]

    result = generate_governance_heatmap(assessment)

    assert len(result) == 2
    assert result[0]["csf_subcategory_id"] == "GV.P0-01"
    assert result[0]["severity"] == "high"
    assert result[0]["gap_score"] == "1.00"
    assert result[1]["severity"] == "low"
    assert result[1]["gap_score"] == "0.00"
