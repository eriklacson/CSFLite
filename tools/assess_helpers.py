"""
Helper functions for the assess tool.
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd


def get_csf_lookup(csf_lookup_path):
    """Read the CSF lookup CSV file and return a dictionary."""

    print("reading CSF lookup from:", csf_lookup_path)

    # Guards for early failure
    if not Path(csf_lookup_path).is_file():
        raise FileNotFoundError(f"CSF lookup file not found: {csf_lookup_path}")

    # Read the CSF lookup CSV file into a pandas DataFrame
    csf_lookup_df = pd.read_csv(csf_lookup_path)

    return csf_lookup_df.to_dict(orient="records")


def read_scan_json(file_path):
    """Read a JSON file and return the parsed object.

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
                    "csf_subcategory_name": match.iloc[0]["subcategory_name"],  # CSF subcategory name
                    "recommended_remediation": match.iloc[0]["recommended_remediation"],  # Suggested remediation steps
                }
            )

    # Return the list of mapped findings
    return mapped_scan


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
    # include informational (lowest) and critical (highest) severities
    sev_w = {
        "info": 0,
        "low": 1,
        "medium": 2,
        "high": 3,
        "critical": 4,
    }

    sev_by_w = {v: k for k, v in sev_w.items()}

    # Convert the DataFrame to a format suitable for heatmap lookup
    #
    # refactor flag: provide check for missing or invalid data
    mapped_df["csf_subcategory_id"] = mapped_df["csf_subcategory_id"].astype(str).str.strip()
    mapped_df["sev_w"] = mapped_df["severity"].astype(str).str.strip().str.lower().map(sev_w).fillna(0)

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
    pd_heatmap["score"] = pd_heatmap["weight"] * (pd_heatmap["max_w"] + np.log1p(pd_heatmap["count"]))
    pd_heatmap["max_severity"] = pd_heatmap["max_w"].map(sev_by_w).fillna("info")
    pd_heatmap["weighted_score"] = pd_heatmap["score"].map(lambda x: f"{x:.2f}")

    # shape + sort + return
    heatmap_columns = [
        "csf_subcategory_id",
        "name",
        "count",
        "max_severity",
        "weighted_score",
    ]
    scan_heatmap = pd_heatmap.sort_values(["score", "csf_subcategory_id"], ascending=[False, True])[
        heatmap_columns
    ].to_dict(orient="records")

    return scan_heatmap


def get_governance_checklist_results(governance_checklist_path):
    """Guards for early failure when loading the governance checklist."""

    print("reading governance checklist from:", governance_checklist_path)

    # Convert governance checklist path to a path object
    governance_checklist_path = Path(governance_checklist_path)

    # Fail early if the lookup file is missing
    if not governance_checklist_path.is_file():
        raise FileNotFoundError(f"governance checklist file not found: {governance_checklist_path}")

    # Read the checklist questionnaire CSV file into a pandas DataFrame
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

    # organise data
    # shape + sort + return
    governance_checklist_result_columns = [
        "csf_function",
        "csf_subcategory_id",
        "csf_subcategory_name",
        "response",
    ]

    governance_checklist_results = governance_checklist_result_df.sort_values(["csf_subcategory_id"], ascending=False)[
        governance_checklist_result_columns
    ].to_dict(orient="records")

    # return checklist
    return governance_checklist_results


def generate_governance_assessement(governance_checklist_results, csf_lookup):
    """Generate governance findings based on the checklist results and CSF lookup."""

    print("generating governance assessment...")

    # normalize response
    response_score = {"Yes": 1, "Partial": 0.5, "No": 0}

    if not governance_checklist_results:
        return []

    """convert inputs to DataFrame"""
    # convert governance checklist results to DataFrame
    governance_checklist_df = pd.DataFrame(governance_checklist_results)
    # convert csf_lookup to DataFrame
    csf_lookup_df = pd.DataFrame(csf_lookup)

    # merge governance_checklist_df with csf_lookup on 'csf_subcategory_id'
    governance_score_df = governance_checklist_df.merge(
        csf_lookup_df[["csf_subcategory_id", "weight", "recommendation"]],
        on="csf_subcategory_id",
        how="left",
    )

    # Add a 'score' column based on the 'response' column
    governance_score_df["score"] = governance_checklist_df["response"].map(response_score).astype(float)

    # Calculate assessment and gap score
    governance_score_df["assessment_score"] = governance_score_df["score"] * governance_score_df["weight"]

    governance_score_df["gap_score"] = governance_score_df["weight"] - governance_score_df["assessment_score"]

    # format scores to 2 decimal places
    governance_score_df["assessment_score"] = governance_score_df["assessment_score"].map(lambda x: f"{x:.2f}")
    governance_score_df["gap_score"] = governance_score_df["gap_score"].map(lambda x: f"{x:.2f}")

    # shape + return relevant columns
    columns = [
        "csf_subcategory_id",
        "csf_subcategory_name",
        "response",
        "score",
        "weight",
        "recommendation",
        "assessment_score",
        "gap_score",
    ]

    # return list of findings with heatmap weight and recommendation
    governance_assessment = governance_score_df[columns].to_dict(orient="records")

    return governance_assessment


def generate_governance_heatmap(governance_assessment):
    print("generating governance heatmap data...")

    # Fail early if no assessment data is provided
    if not governance_assessment:
        return []

    df = pd.DataFrame(governance_assessment)

    # Ensure required columns exist
    required = {
        "csf_subcategory_id",
        "csf_subcategory_name",
        "response",
        "weight",
        "assessment_score",
    }
    if not required.issubset(df.columns):
        return []

    # normalize numeric fields
    df["weight"] = df["weight"].astype(float)
    df["assessment_score"] = df["assessment_score"].astype(float)

    # determine heat level from asessment score
    def score_to_sev(row):
        if row["assessment_score"] <= 0:
            return "high"
        elif row["assessment_score"] < row["weight"]:
            return "medium"
        else:
            return "low"

    df["severity"] = df.apply(score_to_sev, axis=1)

    # compute gap score (higher means bigger governance gap)
    df["gap_score"] = df["weight"] - df["assessment_score"]

    # prepare final shape
    df["name"] = df["csf_subcategory_name"]
    heatmap_columns = [
        "csf_subcategory_id",
        "name",
        "response",
        "severity",
        "gap_score",
    ]

    df = df.sort_values(["gap_score", "csf_subcategory_id"], ascending=[False, True])
    df["gap_score"] = df["gap_score"].map(lambda x: f"{x:.2f}")

    governance_heatmap = df[heatmap_columns].to_dict(orient="records")

    return governance_heatmap


__all__ = [
    "get_csf_lookup",
    "read_scan_json",
    "map_scan_to_csf",
    "generate_scan_heatmap",
    "get_governance_checklist_results",
    "generate_governance_assessement",
    "generate_governance_heatmap",
]
