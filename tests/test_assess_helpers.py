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
            "score": 0.0,
            "assessment_score": "0.00",
        },
        {
            "csf_subcategory_id": "PR.AA-01",
            "csf_subcategory_name": "Access control",
            "response": "Yes",
            "weight": 2.0,
            "score": 1.0,
            "assessment_score": "2.00",
        },
    ]

    result = generate_governance_heatmap(assessment)

    assert len(result) == 2
    assert result[0]["csf_subcategory_id"] == "GV.P0-01"
    assert result[0]["severity"] == "high"
    assert result[0]["gap_score"] == "1.00"
    assert result[1]["severity"] == "none"
    assert result[1]["gap_score"] == "0.00"


def test_generate_governance_heatmap_severity_is_weight_invariant():
    """Severity depends only on coverage. Weight must never demote a finding."""
    from tools.assess_helpers import generate_governance_heatmap

    def row(sid, weight, score):
        return {
            "csf_subcategory_id": sid,
            "csf_subcategory_name": sid,
            "response": "-",
            "weight": weight,
            "score": score,
        }

    # every weight a maintainer could plausibly set, including degenerate ones
    assessment = []
    for i, w in enumerate([1.0, 1.2, 1.5, 0.5, 0.0, 100.0]):
        for label, sc in [("cov", 1.0), ("par", 0.5), ("abs", 0.0)]:
            assessment.append(row(f"{label}-{i}", w, sc))

    sev = {r["csf_subcategory_id"]: r["severity"] for r in generate_governance_heatmap(assessment)}

    for i in range(6):
        assert sev[f"cov-{i}"] == "none", f"covered control at weight index {i}"
        assert sev[f"par-{i}"] == "medium", f"partial control at weight index {i}"
        assert sev[f"abs-{i}"] == "high", f"absent control at weight index {i}"


def test_generate_governance_heatmap_orders_by_weighted_gap():
    """Weight drives priority through the sort, not through severity."""
    from tools.assess_helpers import generate_governance_heatmap

    def row(sid, weight, score):
        return {
            "csf_subcategory_id": sid,
            "csf_subcategory_name": sid,
            "response": "-",
            "weight": weight,
            "score": score,
        }

    assessment = [
        row("FOUNDATIONAL", 1.0, 0.0),  # absent, gap 1.00
        row("CRITICAL", 1.5, 0.0),  # absent, gap 1.50
    ]

    result = generate_governance_heatmap(assessment)

    # same severity, but the critical one sorts first
    assert [r["csf_subcategory_id"] for r in result] == ["CRITICAL", "FOUNDATIONAL"]
    assert result[0]["severity"] == result[1]["severity"] == "high"


def test_generate_governance_heatmap_gap_score_matches_assessment():
    """Regression: the heatmap must not recompute the gap from the rounded assessment_score."""
    from tools.assess_helpers import generate_governance_assessement, generate_governance_heatmap

    checklist = [{"csf_subcategory_id": "XX.AA-01", "csf_subcategory_name": "Quarter", "response": "Partial"}]
    lookup = [{"csf_subcategory_id": "XX.AA-01", "weight": 1.25, "recommendation": "-"}]

    assessment = generate_governance_assessement(checklist, lookup)
    heatmap = generate_governance_heatmap(assessment)

    assert heatmap[0]["gap_score"] == assessment[0]["gap_score"]


def test_generate_governance_assessement_rejects_blank_response():
    from tools.assess_helpers import generate_governance_assessement

    checklist = [
        {
            "csf_subcategory_id": "GV.PO-01",
            "csf_subcategory_name": "Policy established",
            "response": "",
        }
    ]
    lookup = [{"csf_subcategory_id": "GV.PO-01", "weight": 1.5, "recommendation": "Write a policy"}]

    with pytest.raises(ValueError, match="GV.PO-01"):
        generate_governance_assessement(checklist, lookup)


def test_generate_governance_assessement_rejects_unknown_subcategory():
    from tools.assess_helpers import generate_governance_assessement

    checklist = [
        {
            "csf_subcategory_id": "XX.XX-99",
            "csf_subcategory_name": "Not in the framework",
            "response": "Yes",
        }
    ]
    lookup = [{"csf_subcategory_id": "GV.PO-01", "weight": 1.5, "recommendation": "Write a policy"}]

    with pytest.raises(ValueError, match="not found in CSF lookup"):
        generate_governance_assessement(checklist, lookup)
