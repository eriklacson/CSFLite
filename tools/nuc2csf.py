import json


def read_scan_json(file_path):
    # This function reads a JSON file and prints its contents in a formatted way.
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            data = json.load(file)
            print(json.dumps(data, indent=4))
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file at {file_path} is not a valid JSON file.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    # nuclei scan file
    scan_file = "../scans/sample_output.json"

    print("Hello from main!")
    read_scan_json(scan_file)


if __name__ == "__main__":
    main()
