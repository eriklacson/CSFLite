"""
Helper functions for the assess tool.
"""

from pathlib import Path

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
    "get_governance_checklist_results",
    "generate_governance_assessement",
    "generate_governance_heatmap",
]
