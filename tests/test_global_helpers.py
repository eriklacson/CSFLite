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


def write_to_csv(dataset, output_path):
    print("writing mapped results to CSV...")
    if dataset:
        keys = dataset[0].keys()
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(dataset)
        status = f"Dataset written to: {output_path}"
    else:
        status = "No data to write."

    return status


def write_to_json(dataset, output_path):
    print("writing dataset to JSON...")
    if dataset:
        with open(output_path, "w") as f:
            json.dump(dataset, f, indent=4)
        status = f"Dataset written to: {output_path}"
    else:
        status = "No data to write."
    return status
