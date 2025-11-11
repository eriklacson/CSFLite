import csv
import json
from pathlib import Path


def get_paths():
    """Return the paths for input, reference, and output datasets."""

    config_path = Path(__file__).resolve().parent.parent / "config" / "path_config.json"

    with open(config_path, encoding="utf-8") as config_file:
        return json.load(config_file)


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


def load_json_file(file_path):
    """
    Loads a JSON file and returns its content as a Python object.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


__all__ = [
    "get_paths",
    "write_to_csv",
    "write_to_json",
]
