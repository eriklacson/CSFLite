from pathlib import Path
import json
import pandas as pd
import numpy as np
import csv


def get_paths():
    """Returns the paths for input, reference, and output datasets."""

    return {
        # Input Data
        #
        # scan results
        "scan_input_json": "../scans/sample_output.json",
        # governance checklist answer questionaire
        "governance_checklist": "../scans/governance_checks.csv",
        # Reference Data
        #
        # nuclie to csf lookup - map of nuclie template to CSF Sub-category
        "lookup_csv": "../data/nuclie_csf_lookup.csv",
        # heatmap lookup - map of CSF Sub-category to weight and human-friendly name
        "heatmap_lookup": "../data/heat_map_lookup.csv",
        # map of CSF sub-category to with score weight and recommendation
        "csf_lookup": "../data/csf_lookup.csv",
        # Output Data
        #
        # mapped findings - nuclie findings mapped to CSF Sub-category (json and csv)
        "output_csv": "../output/mapped-findings.csv",
        "output_json": "../output/mapped-findings.json",
        # heatmap - heatmap data derived from mapped findings refactor: rename to scan_heatmap_csv when governance heatmap is in place
        "heatmap_csv": "../output/heatmap.csv",
    }


def get_csf_lookup(csf_lookup_path):
    """Reads the CSF lookup CSV file and returns a dictionary."""
    print("reading CSF lookup from:", csf_lookup_path)

    # Guards for early failure
    if not Path(csf_lookup_path).is_file():
        raise FileNotFoundError(f"CSF lookup file not found: {csf_lookup_path}")

    # Read the CSF lookup CSV file into a pandas DataFrame
    csf_lookup_df = pd.read_csv(csf_lookup_path)

    return csf_lookup_df.to_dict(orient="records")


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
    mapped_scan = []

    # Iterate over the findings in the scan results
    for f in scan_results:
        # Extract and strip the "templateID" from the current finding
        template_id = f.get("templateID", "").strip()

        # Find matching rows in the lookup DataFrame based on the "templateID"
        match = lookup_df[lookup_df["templateID"] == template_id]

        # If a match is found, map the finding to the corresponding CSF details
        if not match.empty:
            mapped_scan.append(
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
    return mapped_scan


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


def generate_scan_heatmap(mapped, heatmap_lookup):
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

    # Check if the required columns are present in the DataFrame
    if not {"csf_subcategory_id", "severity"}.issubset(mapped_df.columns):
        return []

    # normalize + map severities -> weights
    sev_w = {"low": 1, "medium": 2, "high": 3}
    sev_by_w = {v: k for k, v in sev_w.items()}

    # Convert the DataFrame to a format suitable for heatmap lookup
    #
    # refactor flag: provide check for missing or invalid data
    mapped_df["csf_subcategory_id"] = mapped_df["csf_subcategory_id"].astype(str).str.strip()
    mapped_df["sev_w"] = mapped_df["severity"].astype(str).str.strip().str.lower().map(sev_w)

    # If the DataFrame is empty after filtering, return an empty list
    if mapped_df.empty:
        return []

    # aggregate per subcategory
    df_aggregate = mapped_df.groupby("csf_subcategory_id", as_index=False).agg(
        count=("csf_subcategory_id", "size"), max_w=("sev_w", "max")
    )

    # sanity check required fields are in the Dataframe:
    # expect 'csf_subcategory_id', 'csf_subcategory_name' (optional), 'weight' (optional)

    pd_heatmap_lookup = pd.read_csv(heatmap_lookup)

    # convert field csf_subcategory_names to human-friendly name
    # for client-facing report outputs.
    pd_heatmap_lookup.rename(columns={"csf_subcategory_name": "name"}, inplace=True)

    if "csf_subcategory_id" not in pd_heatmap_lookup.columns:
        raise KeyError("lookup CSV must contain 'csf_subcategory_id'")
    if "name" not in pd_heatmap_lookup.columns:
        pd_heatmap_lookup["name"] = pd_heatmap_lookup["csf_subcategory_id"]
    if "weight" not in pd_heatmap_lookup.columns:
        pd_heatmap_lookup["weight"] = 1.0
    pd_heatmap_lookup["weight"] = pd_heatmap_lookup["weight"].astype(float)

    # join two datasets and compute heatmap scores
    pd_heatmap = df_aggregate.merge(
        pd_heatmap_lookup[["csf_subcategory_id", "name", "weight"]],
        on="csf_subcategory_id",
        how="left",
    )

    pd_heatmap["name"] = pd_heatmap["name"].fillna(pd_heatmap["csf_subcategory_id"])
    pd_heatmap["weight"] = pd_heatmap["weight"].fillna(1.0)
    pd_heatmap["score"] = pd_heatmap["weight"] * (
        pd_heatmap["max_w"] + np.log1p(pd_heatmap["count"])
    )
    pd_heatmap["max_severity"] = pd_heatmap["max_w"].map(sev_by_w).fillna("low")
    pd_heatmap["weighted_score"] = pd_heatmap["score"].map(lambda x: f"{x:.2f}")

    # shape + sort + return
    heatmap_columns = [
        "csf_subcategory_id",
        "name",
        "count",
        "max_severity",
        "weighted_score",
    ]
    heatmap = pd_heatmap.sort_values(["score", "csf_subcategory_id"], ascending=[False, True])[
        heatmap_columns
    ].to_dict(orient="records")

    return heatmap


def get_governance_checklist_results(governance_checklist_path):
    """guards for early failure"""
    # Convert governance checklist path to a path object
    governance_checklist_path = Path(governance_checklist_path)

    # Fail early if the lookup file is missing
    if not governance_checklist_path.is_file():
        raise FileNotFoundError(f"governance checklist file not found: {governance_checklist_path}")

    # Read the checklist questionaire CSV file into a pandas DataFrame
    raw_checklist_df = pd.read_csv(governance_checklist_path)

    # Data validation
    #
    # Check for required columns
    required_columns = ["csf_function", "csf_subcategory_id", "csf_subcategory_name", "response"]
    missing_columns = set(required_columns) - set(raw_checklist_df.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Create a new DataFrame with only the required columns
    governance_checklist_result_df = raw_checklist_df[required_columns]

    # organize data
    # shape + sort + return
    governance_checklist_result_columns = [
        "csf_function",
        "csf_subcategory_id",
        "csf_subcategory_name",
        "response",
    ]

    governance_checklist_results = governance_checklist_result_df.sort_values(
        ["csf_subcategory_id"], ascending=False
    )[governance_checklist_result_columns].to_dict(orient="records")

    # return checklist
    return governance_checklist_results


def generate_governance_assessement(governance_checklist_results, csf_lookup):
    """Generates governance findings based on the checklist results and CSF lookup"""
    print("generating governance findings placeholder...")

    # convert governance checklist results to DataFrame
    governance_checklist_df = pd.DataFrame(governance_checklist_results)
    csf_lookup = pd.DataFrame(csf_lookup)

    # normalize response
    response_score = {"yes": 1, "partial": 0.5, "no": 0}

    # Add a 'score' column based on the 'response' column
    governance_checklist_df["score"] = governance_checklist_df["response"].map(response_score)

    # Merge governance_checklist_df with csf_lookup on 'csf_subcategory_id'
    governance_score_df = governance_checklist_df.merge(
        csf_lookup[["csf_subcategory_id", "weight", "recommendation"]],
        on="csf_subcategory_id",
        how="left",
    )

    governance_score_df["weighted_score"] = (
        governance_score_df["score"] * governance_score_df["weight"]
    )

    # return list of findings with heatmap weight and recommendation
    return


def main():
    paths = get_paths()

    """get input data"""
    # nuclie scan outputt
    findings = read_scan_json(paths["scan_input_json"])

    """get reference data"""
    # CSF lookup
    csf_lookup = get_csf_lookup(paths["csf_lookup"])

    # map scan findings to CSF
    mapped_scan = map_scan_to_csf(findings, paths["lookup_csv"])

    # map governance check to CSF
    #
    # get check questionaire result
    governance_checklist_results = get_governance_checklist_results(paths["governance_checklist"])

    # generate governance assessment
    generate_governance_assessement(governance_checklist_results, csf_lookup)  # noqa: F841

    write_to_csv(mapped_scan, paths["output_csv"])
    write_to_json(mapped_scan, paths["output_json"])

    scan_heatmap = generate_scan_heatmap(mapped_scan, paths["heatmap_lookup"])
    write_to_csv(scan_heatmap, paths["heatmap_csv"])


if __name__ == "__main__":
    main()
