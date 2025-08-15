from unittest.mock import mock_open, patch
import json


def test_get_paths():
    from tools.nuc2csf import get_paths

    expected_paths = {
        "input_json": "data/nuclei-output.json",
        "lookup_csv": "data/csf_lookup.csv",
        "output_csv": "data/mapped-findings.csv",
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


if __name__ == "__main__":
    test_read_scan_json_valid()
    test_read_scan_json_invalid()
