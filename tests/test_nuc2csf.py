from unittest.mock import mock_open, patch
from pathlib import Path
import pytest
import json
import csv
import os
import sys

# ensure project root is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_get_paths():
    from tools.nuc2csf import get_paths

    expected_paths = {  # Input Data
        #
        # scan results
        "scan_input_json": "../scans/sample_output.json",
        # governance checklist answer questionaire
        "governance_checklist": "../scans/governance_checks.csv",
        # Reference Data
        #
        # nuclie to csf lookup - map of nuclie template to CSF Sub-category
        "lookup_csv": "../data/nuclie_csf_lookup.csv",
        # heatmap lookup - map of CSF Sub-category to weight and human-friendly name
        "heatmap_lookup": "../data/heat_map_lookup.csv",
        # map of CSF sub-category to with score weight and recommendation
        "csf_lookup": "../data/csf_lookup.csv",
        # Output Data
        #
        # mapped findings - nuclie findings mapped to CSF Sub-category (json and csv)
        "output_csv": "../output/mapped-findings.csv",
        "output_json": "../output/mapped-findings.json",
        # heatmap - heatmap data derived from mapped findings refactor: rename to scan_heatmap_csv when governance heatmap is in place
        "heatmap_csv": "../output/heatmap.csv",
        # governance assessment - governance assessment derived from governance checklist and csf lookup
        "governance_assessment_csv": "../output/governance_assessment.csv",
        # governance heatmap - heatmap data derived from governance assessment
        "governance_heatmap_csv": "../output/governance_heatmap_csv.csv",
    }

    assert get_paths() == expected_paths


def test_read_scan_json_valid():
    # Mock JSON content
    mock_json_content = '{"key": "value"}'
    expected_result = {"key": "value"}

    # Mock the open function and patch it
    with patch("builtins.open", mock_open(read_data=mock_json_content)):
        from tools.nuc2csf import read_scan_json

        # Call the function and assert the result
        result = read_scan_json("mock_file.json")
        assert result == expected_result


def test_read_scan_json_invalid():
    # Mock invalid JSON content
    mock_json_content = '{"key": "value"'

    # Mock the open function and patch it
    with patch("builtins.open", mock_open(read_data=mock_json_content)):
        from tools.nuc2csf import read_scan_json

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
    lookup_data = """templateID,csf_function,subcategory_id,subcategory_name
TEMPLATE-1,Identify,ID.AM-1,Asset Management
TEMPLATE-2,Protect,PR.AC-1,Access Control
"""
    lookup_csv_path = tmp_path / "lookup.csv"
    lookup_csv_path.write_text(lookup_data)
    return lookup_csv_path


def test_map_scan_to_csf(mock_lookup_csv):
    # import necessary functions
    from tools.nuc2csf import map_scan_to_csf

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
    assert result[0]["csf_subcategory_id"] == "ID.AM-1"
    assert "templateID" in result[0]
    assert "host" in result[1]


def test_write_with_data(tmp_path):
    # import necessary functions
    from tools.nuc2csf import write_to_csv

    test_data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
    path = tmp_path / "test.csv"

    status = write_to_csv(test_data, str(path))

    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert status == f"Dataset written to: {path}"
    assert len(rows) == 2
    assert rows[0]["name"] == "Alice"
    assert rows[1]["age"] == "25"


def test_write_no_data(tmp_path):
    # import necessary functions
    from tools.nuc2csf import write_to_csv

    path = tmp_path / "empty.csv"
    status = write_to_csv([], str(path))

    assert status == "No data to write."


def test_write_to_json_with_data(tmp_path: Path):
    # Import necessary functions
    from tools.nuc2csf import write_to_json

    # prep test data and file
    data = [{"a": 1, "b": 2}]
    output_file = tmp_path / "out.json"

    # call function
    status = write_to_json(data, output_file)

    # run test
    assert output_file.exists()
    written = json.loads(output_file.read_text())
    assert written == data
    assert f"Dataset written to: {output_file}" in status


def test_write_to_json_no_data(tmp_path: Path):
    # import necessary functions
    from tools.nuc2csf import write_to_json

    # prep test data and file
    data = []
    output_file = tmp_path / "out.json"

    # call function
    status = write_to_json(data, output_file)

    # run test
    assert not output_file.exists()
    assert status == "No data to write."


def test_generate_scan_heatmap_handles_info_and_critical(tmp_path: Path):
    from tools.nuc2csf import generate_scan_heatmap
    import numpy as np

    mapped = [
        {"csf_subcategory_id": "ID.AM-02", "severity": "critical"},
        {"csf_subcategory_id": "ID.AM-02", "severity": "info"},
    ]

    lookup_csv = tmp_path / "heatmap_lookup.csv"
    lookup_csv.write_text(
        "csf_subcategory_id,csf_subcategory_name,weight\n"
        "ID.AM-02,Devices and systems inventoried,1.0\n"
    )

    result = generate_scan_heatmap(mapped, lookup_csv)

    assert len(result) == 1
    assert result[0]["csf_subcategory_id"] == "ID.AM-02"
    assert result[0]["max_severity"] == "critical"
    assert result[0]["count"] == 2
    expected_score = 4 + np.log1p(2)
    assert float(result[0]["weighted_score"]) == pytest.approx(expected_score, rel=1e-2)


def test_get_csf_lookup(tmp_path: Path):
    from tools.nuc2csf import get_csf_lookup

    csv_content = (
        "csf_subcategory_id,weight,recommendation\n"
        "ID.AM-1,1,Assess assets\n"
        "PR.AC-1,2,Enforce access control\n"
    )
    lookup_path = tmp_path / "csf_lookup.csv"
    lookup_path.write_text(csv_content)

    result = get_csf_lookup(lookup_path)
    assert len(result) == 2
    assert result[0]["csf_subcategory_id"] == "ID.AM-1"
    assert result[1]["weight"] == 2


def test_get_csf_lookup_missing_file():
    from tools.nuc2csf import get_csf_lookup

    with pytest.raises(FileNotFoundError):
        get_csf_lookup("missing.csv")


def test_get_governance_checklist_results(tmp_path: Path):
    from tools.nuc2csf import get_governance_checklist_results

    checklist_content = (
        "csf_function,csf_subcategory_id,csf_subcategory_name,notes,response\n"
        "Identify,ID.AM-1,Assets inventoried,,yes\n"
        "Protect,PR.AC-1,Access control,need to implement ssl,partial\n"
    )
    checklist_path = tmp_path / "checklist.csv"
    checklist_path.write_text(checklist_content)

    result = get_governance_checklist_results(checklist_path)
    assert result[0]["csf_subcategory_id"] == "PR.AC-1"
    assert result[1]["response"] == "yes"


def test_get_governance_checklist_results_missing_file():
    from tools.nuc2csf import get_governance_checklist_results

    with pytest.raises(FileNotFoundError):
        get_governance_checklist_results("no-file.csv")


def test_get_governance_checklist_results_missing_columns(tmp_path: Path):
    from tools.nuc2csf import get_governance_checklist_results

    checklist_content = "csf_function,csf_subcategory_id,response\nIdentify,ID.AM-1,yes\n"
    checklist_path = tmp_path / "checklist.csv"
    checklist_path.write_text(checklist_content)

    with pytest.raises(ValueError):
        get_governance_checklist_results(checklist_path)


def test_generate_governance_assessment():
    from tools.nuc2csf import generate_governance_assessement

    checklist = [
        {
            "csf_subcategory_id": "ID.AM-1",
            "csf_subcategory_name": "Assets inventoried",
            "notes": "",
            "response": "Yes",
        },
        {
            "csf_subcategory_id": "PR.AC-1",
            "csf_subcategory_name": "Access control",
            "notes": "need to implement ssl",
            "response": "Partial",
        },
    ]

    lookup = [
        {
            "csf_subcategory_id": "ID.AM-1",
            "weight": 2,
            "recommendation": "Assess assets",
        },
        {
            "csf_subcategory_id": "PR.AC-1",
            "weight": 1,
            "recommendation": "Enforce access control",
        },
    ]

    result = generate_governance_assessement(checklist, lookup)

    assert len(result) == 2
    result_by_id = {r["csf_subcategory_id"]: r for r in result}
    assert result_by_id["ID.AM-1"]["weighted_score"] == "2.00"
    assert result_by_id["PR.AC-1"]["recommendation"] == "Enforce access control"
    assert result_by_id["PR.AC-1"]["weighted_score"] == "0.50"


def test_generate_governance_heatmap():
    from tools.nuc2csf import generate_governance_heatmap

    assessment = [
        {
            "csf_subcategory_id": "ID.GV-01",
            "csf_subcategory_name": "Governance roles",
            "response": "Yes",
            "weight": 1.0,
            "weighted_score": "0.00",
        },
        {
            "csf_subcategory_id": "PR.AC-01",
            "csf_subcategory_name": "Access control",
            "response": "No",
            "weight": 2.0,
            "weighted_score": "2.00",
        },
    ]

    result = generate_governance_heatmap(assessment)

    assert len(result) == 2
    assert result[0]["csf_subcategory_id"] == "ID.GV-01"
    assert result[0]["severity"] == "high"
    assert result[0]["weighted_score"] == "1.00"
    assert result[1]["severity"] == "low"
    assert result[1]["weighted_score"] == "0.00"
