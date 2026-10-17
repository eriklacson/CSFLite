"""CLI entry point behaviour."""

import os
import sys
from pathlib import Path

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.governance_check import main  # noqa: E402


def test_main_exits_nonzero_on_missing_arguments():
    with pytest.raises(SystemExit) as exc:
        main([])

    assert exc.value.code == 1


def test_main_exits_nonzero_on_unscoreable_checklist(tmp_path: Path):
    """The shipped template has every response blank, so this is the routine failure path."""
    checklist = tmp_path / "checklist.csv"
    checklist.write_text(
        "csf_function,csf_subcategory_id,csf_subcategory_name,response\nGovern,GV.PO-01,Policy,\n",
        encoding="utf-8",
    )
    assessment = tmp_path / "assessment.csv"
    heatmap = tmp_path / "heatmap.csv"

    with pytest.raises(SystemExit) as exc:
        main(
            [
                "--governance_checklist",
                str(checklist),
                "--governance_assessment_csv",
                str(assessment),
                "--governance_heatmap",
                str(heatmap),
            ]
        )

    assert exc.value.code == 1
    assert not assessment.exists()
    assert not heatmap.exists()
