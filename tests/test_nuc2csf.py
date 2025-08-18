from unittest.mock import mock_open, patch
import pytest
import json
import csv


def test_get_paths():
    from tools.nuc2csf import get_paths

    expected_paths = {
        "input_json": "../scans/sample_output.json",
        "lookup_csv": "../data/csf_lookup.csv",
        "output_csv": "../data/mapped-findings.csv",
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

    assert status == f"Mapped results written to: {path}"
    assert len(rows) == 2
    assert rows[0]["name"] == "Alice"
    assert rows[1]["age"] == "25"


def test_write_no_data(tmp_path):
    # import necessary functions
    from tools.nuc2csf import write_to_csv

    path = tmp_path / "empty.csv"
    status = write_to_csv([], str(path))

    assert status == "No data to write."
