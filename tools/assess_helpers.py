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

    # Guard: an unscoreable response or an unknown subcategory yields NaN, which propagates
    # into assessment_score and makes score_to_sev fall through to "low" — an unanswered
    # control would be reported as having no gap. Fail early instead.
    scores = governance_score_df["response"].map(response_score)

    unscored = [str(i) for i in governance_score_df.loc[scores.isna(), "csf_subcategory_id"]]
    if unscored:
        raise ValueError(
            f"Response must be exactly Yes, Partial, or No — missing or invalid for: {', '.join(unscored)}"
        )

    unknown = [str(i) for i in governance_score_df.loc[governance_score_df["weight"].isna(), "csf_subcategory_id"]]
    if unknown:
        raise ValueError(f"Subcategory not found in CSF lookup: {', '.join(unknown)}")

    # Add a 'score' column based on the 'response' column
    governance_score_df["score"] = scores.astype(float)

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
        "score",
    }
    if not required.issubset(df.columns):
        return []

    # normalize numeric fields
    df["weight"] = df["weight"].astype(float)
    df["score"] = df["score"].astype(float)

    # compute gap score (higher means bigger governance gap).
    # Derived from score x weight rather than the incoming assessment_score, which is a
    # presentation string already rounded to 2dp. Recomputing from the rounded value made this
    # disagree with the gap_score in the assessment output.
    df["gap_score"] = df["weight"] - (df["score"] * df["weight"])

    # determine heat level from coverage. Weight is deliberately not a factor: with weights
    # spanning only 1.0-1.5 there is no room to band on the weighted gap without demoting real
    # findings, so weight drives ordering through gap_score instead, which is the sort key below.
    def score_to_sev(score):
        if score >= 1:
            return "none"
        elif score > 0:
            return "medium"
        else:
            return "high"

    df["severity"] = df["score"].map(score_to_sev)

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
