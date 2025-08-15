import json
import pandas as pd


def get_paths():
    """Returns the paths for input JSON, lookup CSV, and output CSV."""

    return {
        "input_json": "data/nuclei-output.json",
        "lookup_csv": "data/csf_lookup.csv",
        "output_csv": "data/mapped-findings.csv",
    }


def read_scan_json(file_path):
    """Reads a JSON file and returns the parsed object.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        json.JSONDecodeError: If the file content is not valid JSON.
        Exception: For any other unexpected errors.
    """
    with open(file_path, mode="r", encoding="utf-8") as file:
        try:
            scan_result = json.load(file)
        except json.JSONDecodeError:
            raise  # re-raise so tests/CI can detect failure
        else:
            print(json.dumps(scan_result, indent=4))
            return scan_result


def map_scan_to_csf(scan_results, lookup_csv_path):
    # Read the lookup CSV file into a pandas DataFrame
    lookup_df = pd.read_csv(lookup_csv_path)

    # Strip whitespace from the "templateID" column in the DataFrame
    lookup_df["templateID"] = lookup_df["templateID"].str.strip()

    # Initialize an empty list to store the mapped results
    mapped = []

    # Iterate over the findings in the scan results
    for f in scan_results.get("findings", []):
        # Extract and strip the "templateID" from the current finding
        template_id = f.get("templateID", "").strip()

        # Find matching rows in the lookup DataFrame based on the "templateID"
        match = lookup_df[lookup_df["templateID"] == template_id]

        # If a match is found, map the finding to the corresponding CSF details
        if not match.empty:
            mapped.append(
                {
                    "timestamp": f.get("timestamp"),  # Timestamp of the finding
                    "host": f.get("host"),  # Host where the finding was detected
                    "templateID": template_id,  # Template ID of the finding
                    "severity": f.get("severity"),  # Severity level of the finding
                    "matcher_name": f.get("matcher-name"),  # Matcher name of the finding
                    "description": f.get("description"),  # Description of the finding
                    "csf_function": match.iloc[0]["csf_function"],  # CSF function from the lookup
                    "csf_subcategory_id": match.iloc[0]["subcategory_id"],  # CSF subcategory ID
                    "csf_subcategory_name": match.iloc[0][
                        "subcategory_name"
                    ],  # CSF subcategory name
                }
            )

    # Return the list of mapped findings
    return mapped


def main():
    # nuclei scan file
    _scan_file = "../scans/sample_output.json"

    print("Hello from main!")


if __name__ == "__main__":
    main()
