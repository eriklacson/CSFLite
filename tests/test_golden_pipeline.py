"""End-to-end comparison against recorded CLI output.

The recordings in tests/fixtures/golden/ were produced by the CLI pipeline. Phase 4 replaces that
CLI with a web application, after which nothing produces "the CLI output" to compare against — so
the reference is frozen here while the CLI still exists.

A failure means scoring behaviour changed. That is sometimes intended (a reweighted subcategory, a
deliberate rule change), in which case re-record and commit the new files as part of the same
change. It is never something to work around by loosening the comparison.
"""

import os
import sys
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.assess_helpers import (  # noqa: E402
    generate_governance_assessement,
    generate_governance_heatmap,
    get_csf_lookup,
    get_governance_checklist_results,
)
from tools.global_helpers import write_to_csv  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GOLDEN = PROJECT_ROOT / "tests" / "fixtures" / "golden"


def _run_pipeline():
    lookup = get_csf_lookup(PROJECT_ROOT / "data" / "csf_lookup.csv")
    rows = get_governance_checklist_results(GOLDEN / "governance_checklist.csv")
    assessment = generate_governance_assessement(rows, lookup)
    return assessment, generate_governance_heatmap(assessment)


def _assert_matches_recording(dataset, recorded_name, tmp_path):
    """Compare serialised bytes, not dicts — this has to catch formatting and row order too."""
    actual_path = tmp_path / recorded_name
    write_to_csv(dataset, actual_path)

    actual = actual_path.read_text(encoding="utf-8")
    expected = (GOLDEN / recorded_name).read_text(encoding="utf-8")

    assert actual == expected, (
        f"{recorded_name} differs from the recording in tests/fixtures/golden/. "
        "If the change is intended, re-record and commit the updated fixture."
    )


def test_golden_assessment_matches_recording(tmp_path: Path):
    assessment, _ = _run_pipeline()
    _assert_matches_recording(assessment, "governance_assessment.csv", tmp_path)


def test_golden_heatmap_matches_recording(tmp_path: Path):
    _, heatmap = _run_pipeline()
    _assert_matches_recording(heatmap, "governance_heatmap.csv", tmp_path)


def test_golden_input_covers_every_response_and_subcategory():
    """A recording that only exercises one response value would prove very little."""
    rows = get_governance_checklist_results(GOLDEN / "governance_checklist.csv")
    lookup = get_csf_lookup(PROJECT_ROOT / "data" / "csf_lookup.csv")

    assert {r["response"] for r in rows} == {"Yes", "Partial", "No"}
    assert {r["csf_subcategory_id"] for r in rows} == {item["csf_subcategory_id"] for item in lookup}
