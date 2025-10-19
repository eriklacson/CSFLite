import csv
import json
from pathlib import Path


# test get_paths function
def test_get_paths():
    from tools.global_helpers import get_paths

    config_path = Path(__file__).resolve().parent.parent / "config" / "path_config.json"

    with open(config_path, encoding="utf-8") as config_file:
        expected_paths = json.load(config_file)

    assert get_paths() == expected_paths


def test_write_with_data(tmp_path):
    # import necessary functions
    from tools.global_helpers import write_to_csv

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
    from tools.global_helpers import write_to_csv

    path = tmp_path / "empty.csv"
    status = write_to_csv([], str(path))

    assert status == "No data to write."


def test_write_to_json_with_data(tmp_path: Path):
    # Import necessary functions
    from tools.global_helpers import write_to_json

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
    from tools.global_helpers import write_to_json

    # prep test data and file
    data = []
    output_file = tmp_path / "out.json"

    # call function
    status = write_to_json(data, output_file)

    # run test
    assert not output_file.exists()
    assert status == "No data to write."
