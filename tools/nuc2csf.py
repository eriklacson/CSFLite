import json
import pandas as pd
import csv


def get_paths():
    """Returns the paths for input JSON, lookup CSV, and output CSV."""

    return {
        "input_json": "../scans/sample_output.json",
        "lookup_csv": "../data/csf_lookup.csv",
        "output_csv": "../output/mapped-findings.csv",
        "output_json": "../output/mapped-findings.json",
    }


def read_scan_json(file_path):
    """Reads a JSON file and returns the parsed object.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        json.JSONDecodeError: If the file content is not valid JSON.
        Exception: For any other unexpected errors.
    """
    print("reading scan results from:", file_path)
    with open(file_path, mode="r", encoding="utf-8") as file:
        try:
            scan_result = json.load(file)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {file_path}")
            raise  # re-raise so tests/CI can detect failure
        else:
            return scan_result


def map_scan_to_csf(scan_results, lookup_csv_path):
    print("mapping scan results to CSF...")
    # Read the lookup CSV file into a pandas DataFrame
    lookup_df = pd.read_csv(lookup_csv_path)

    # Strip whitespace from the "templateID" column in the DataFrame
    lookup_df["templateID"] = lookup_df["templateID"].str.strip()

    # Initialize an empty list to store the mapped results
    mapped = []

    # Iterate over the findings in the scan results
    for f in scan_results:
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


def write_to_csv(mapped_data, output_path):
    print("writing mapped results to CSV...")
    if mapped_data:
        keys = mapped_data[0].keys()
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(mapped_data)
        status = f"Mapped results written to: {output_path}"
    else:
        status = "No data to write."

    return status


def write_to_json(mapped_data, output_path):
    print("writing mapped results to JSON...")
    if mapped_data:
        with open(output_path, "w") as f:
            json.dump(mapped_data, f, indent=4)
        status = f"Mapped results written to: {output_path}"
    else:
        status = "No data to write."
    return status


def main():
    paths = get_paths()
    findings = read_scan_json(paths["input_json"])
    mapped = map_scan_to_csf(findings, paths["lookup_csv"])
    write_to_csv(mapped, paths["output_csv"])
    write_to_json(mapped, paths["output_json"])


if __name__ == "__main__":
    main()
