import json


def read_scan_json(file_path):
    """Reads a JSON file and returns the parsed object.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        json.JSONDecodeError: If the file content is not valid JSON.
        Exception: For any other unexpected errors.
    """
    with open(file_path, mode="r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            raise  # re-raise so tests/CI can detect failure
        else:
            print(json.dumps(data, indent=4))
            return data


def main():
    # nuclei scan file
    _scan_file = "../scans/sample_output.json"

    print("Hello from main!")


if __name__ == "__main__":
    main()
