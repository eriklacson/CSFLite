from pathlib import Path
import json
import pandas as pd
import numpy as np
import csv


def get_paths():
    """Returns the paths for input JSON, lookup CSV, and output CSV."""

    return {
        "input_json": "../scans/sample_output.json",
        "lookup_csv": "../data/nuclie_csf_lookup.csv",
        "heatmap_lookup": "../data/heat_map_lookup.csv",
        "output_csv": "../output/mapped-findings.csv",
        "output_json": "../output/mapped-findings.json",
        "heatmap_csv": "../output/heatmap.csv",
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


def generate_heatmap(mapped, heatmap_lookup):
    print("generating heatmap data...")

    # Guards for early failure
    #
    # Convert heatmap_lookup to a Path object
    heatmap_lookup_path = Path(heatmap_lookup)

    # Fail early if the lookup file is missing
    if not heatmap_lookup_path.is_file():
        raise FileNotFoundError(f"Heatmap lookup file not found: {heatmap_lookup}")

    # Fail early if the mapped data is empty
    if not mapped:
        return []

    mapped_df = pd.DataFrame(mapped)

    print(mapped_df)

    # Check if the required columns are present in the DataFrame
    if not {"csf_subcategory_id", "severity"}.issubset(mapped_df.columns):
        return []

    # normalize + map severities -> weights
    sev_w = {"low": 1, "medium": 2, "high": 3}
    sev_by_w = {v: k for k, v in sev_w.items()}  # noqa: F841

    # Convert the DataFrame to a format suitable for heatmap lookup
    #
    # refact: provide check for missing or invalid data
    mapped_df["subcat_id"] = mapped_df["csf_subcategory_id"].astype(str).str.strip()
    mapped_df["sev_w"] = mapped_df["severity"].astype(str).str.strip().str.lower().map(sev_w)

    # If the DataFrame is empty after filtering, return an empty list
    if mapped_df.empty:
        return []

    # aggregate per subcategory
    df_aggregate = mapped_df.groupby("subcat_id", as_index=False).agg(
        count=("csf_subcategory_id", "size"), max_w=("sev_w", "max")
    )

    print(df_aggregate)

    # sanity check required fields is in the Dataframe:
    # expect 'subcategory_id', 'name' (optional), 'weight' (optional)

    pd_heatmap_lookup = pd.read_csv(heatmap_lookup)
    if "subcategory_id" not in pd_heatmap_lookup.columns:
        raise KeyError("lookup CSV must contain 'subcategory_id'")
    if "subcategory_name" not in pd_heatmap_lookup.columns:
        pd_heatmap_lookup["subcategory_name"] = pd_heatmap_lookup["subcategory_id"]
    if "weight" not in pd_heatmap_lookup.columns:
        pd_heatmap_lookup["weight"] = 1.0
    pd_heatmap_lookup["weight"] = pd_heatmap_lookup["weight"].astype(float)

    # join two datasets and compute heatmap scores
    pd_heatmap = df_aggregate.merge(
        pd_heatmap_lookup[["subcategory_id", "name", "weight"]],
        left_on="subcat_id",
        right_on="subcategory_id",
        how="left",
    )
    pd_heatmap["name"] = pd_heatmap["name"].fillna(pd_heatmap["subcat_id"])
    pd_heatmap["weight"] = pd_heatmap["weight"].fillna(1.0)
    pd_heatmap["score"] = pd_heatmap["weight"] * (
        pd_heatmap["max_w"] + np.log1p(pd_heatmap["count"])
    )
    pd_heatmap["max_severity"] = pd_heatmap["max_w"].map(sev_by_w).fillna("low")
    pd_heatmap["weighted_score"] = pd_heatmap["score"].map(lambda x: f"{x:.2f}")

    # shape + sort + return
    heatmap_columns = ["subcat_id", "name", "count", "max_severity", "weighted_score"]
    heatmap = pd_heatmap.sort_values(["score", "subcat_id"], ascending=[False, True])[
        heatmap_columns
    ].to_dict(orient="records")

    return heatmap  # Return placeholder


def main():
    paths = get_paths()
    print(paths)
    findings = read_scan_json(paths["input_json"])
    mapped = map_scan_to_csf(findings, paths["lookup_csv"])
    write_to_csv(mapped, paths["output_csv"])
    write_to_json(mapped, paths["output_json"])
    heatmap = generate_heatmap(mapped, paths["heatmap_lookup"])
    write_to_csv(heatmap, paths["heatmap_csv"])


if __name__ == "__main__":
    main()
