import json
import os
import sys
from pathlib import Path
from unittest.mock import mock_open, patch

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


def test_read_scan_json_valid():
    """tests reading valid scan JSON"""
    from tools.assess_helpers import read_scan_json

    # Mock JSON content
    mock_json_content = '{"key": "value"}'
    expected_result = {"key": "value"}

    # Mock the open function and patch it
    with patch("builtins.open", mock_open(read_data=mock_json_content)):
        # Call the function and assert the result
        result = read_scan_json("mock_file.json")
        assert result == expected_result


def test_read_scan_json_invalid():
    """test handling of invalid scan JSON"""
    from tools.assess_helpers import read_scan_json

    # Mock invalid JSON content
    mock_json_content = '{"key": "value"'

    # Mock the open function and patch it
    with patch("builtins.open", mock_open(read_data=mock_json_content)):
        # Assert that a JSONDecodeError is raised
        try:
            read_scan_json("mock_file.json")
        except json.JSONDecodeError:
            pass
        else:
            raise AssertionError("JSONDecodeError was not raised")


# test_map_scan_to_csf.py
@pytest.fixture
def mock_lookup_csv(tmp_path):
    # Create a temporary CSV file for the lookup data
    lookup_data = """templateID,csf_function,subcategory_id,subcategory_name,recommended_remediation
TEMPLATE-1,Identify,ID.AM-02,Asset Management,Remediate template 1
TEMPLATE-2,Protect,PR.AA-03,Access Control,Remediate template 2
"""
    lookup_csv_path = tmp_path / "lookup.csv"
    lookup_csv_path.write_text(lookup_data)
    return lookup_csv_path


def test_map_scan_to_csf(mock_lookup_csv):
    # import necessary functions
    from tools.assess_helpers import map_scan_to_csf

    # Sample findings (must be list of dicts, not strings)
    test_findings = [
        {
            "templateID": "TEMPLATE-1",
            "host": "https://dev.example.com",
            "timestamp": "2025-08-08T10:02:00Z",
            "severity": "medium",
            "matcher-name": "self-signed-cert",
            "description": "TLS uses a self-signed certificate",
        },
        {
            "templateID": "TEMPLATE-2",
            "host": "http://example.com/admin",
            "timestamp": "2025-08-08T10:01:00Z",
            "severity": "high",
            "matcher-name": "unauth-admin-panel",
            "description": "Accessible admin panel without authentication",
        },
    ]

    result = map_scan_to_csf(test_findings, mock_lookup_csv)
    assert len(result) == 2
    assert result[0]["csf_function"] == "Identify"
    assert result[0]["csf_subcategory_id"] == "ID.AM-02"
    assert "templateID" in result[0]
    assert "host" in result[1]


def test_generate_scan_heatmap_handles_info_and_critical(tmp_path: Path):
    import numpy as np

    from tools.assess_helpers import generate_scan_heatmap

    mapped = [
        {"csf_subcategory_id": "ID.AM-02", "severity": "critical"},
        {"csf_subcategory_id": "ID.AM-02", "severity": "info"},
    ]

    lookup_csv = tmp_path / "heatmap_lookup.csv"
    lookup_csv.write_text(
        "csf_subcategory_id,csf_subcategory_name,weight\nID.AM-02,Devices and systems inventoried,1.0\n"
    )

    result = generate_scan_heatmap(mapped, lookup_csv)

    assert len(result) == 1
    assert result[0]["csf_subcategory_id"] == "ID.AM-02"
    assert result[0]["max_severity"] == "critical"
    assert result[0]["count"] == 2
    expected_score = 4 + np.log1p(2)
    assert float(result[0]["weighted_score"]) == pytest.approx(expected_score, rel=1e-2)


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
            "weighted_score": "0.00",
        },
        {
            "csf_subcategory_id": "PR.AA-01",
            "csf_subcategory_name": "Access control",
            "response": "Yes",
            "weight": 2.0,
            "weighted_score": "2.00",
        },
    ]

    result = generate_governance_heatmap(assessment)

    assert len(result) == 2
    assert result[0]["csf_subcategory_id"] == "GV.P0-01"
    assert result[0]["severity"] == "high"
    assert result[0]["gap_score"] == "1.00"
    assert result[1]["severity"] == "low"
    assert result[1]["gap_score"] == "0.00"
