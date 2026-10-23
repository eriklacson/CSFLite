"""Validation of the reference data itself, `data/csf_lookup.csv`.

Everything else reads this file through pandas, which types a column by guessing. A bad cell does not
fail where it is made: a typo in `weight` surfaces as a TypeError deep in scoring, with no mention of
the file, the row, or the column. These tests read the raw cells and name the problem instead.

Scope is fixed at 25 subcategories (ADR-0002). A change to that number is a decision, not an edit, so
the count is asserted here rather than inferred.
"""

import csv
import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOOKUP = PROJECT_ROOT / "data" / "csf_lookup.csv"
CHECKLIST_TEMPLATE = PROJECT_ROOT / "templates" / "governance_checks_template.csv"

EXPECTED_COLUMNS = [
    "csf_subcategory_id",
    "csf_function",
    "csf_subcategory_name",
    "question",
    "evidence",
    "weight",
    "recommendation",
    "csf_outcome",
]
EXPECTED_ROW_COUNT = 25

ID_PATTERN = re.compile(r"^(GV|ID|PR|DE|RS|RC)\.[A-Z]{2}-\d{2}$")
FUNCTION_BY_PREFIX = {
    "GV": "Govern",
    "ID": "Identify",
    "PR": "Protect",
    "DE": "Detect",
    "RS": "Respond",
    "RC": "Recover",
}


def _problems(path):
    """Return one message per defect found in the lookup file at `path`. Empty means valid."""
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    if not rows:
        return ["file is empty"]

    header, body = rows[0], rows[1:]
    if header != EXPECTED_COLUMNS:
        return [f"header is {header}, expected {EXPECTED_COLUMNS}"]

    problems = []
    if len(body) != EXPECTED_ROW_COUNT:
        problems.append(f"{len(body)} rows, expected {EXPECTED_ROW_COUNT}")

    seen = set()
    for line_no, cells in enumerate(body, start=2):
        # A ragged row means an unquoted comma shifted every later column.
        if len(cells) != len(header):
            problems.append(f"line {line_no}: {len(cells)} fields, expected {len(header)} (unquoted comma?)")
            continue

        row = dict(zip(header, cells, strict=True))
        sub_id = row["csf_subcategory_id"]
        where = f"line {line_no} ({sub_id or 'no id'})"

        for column in header:
            if not row[column].strip():
                problems.append(f"{where}: {column} is empty")

        if not ID_PATTERN.match(sub_id):
            problems.append(f"{where}: csf_subcategory_id does not look like a CSF 2.0 ID")
        else:
            expected_function = FUNCTION_BY_PREFIX[sub_id[:2]]
            if row["csf_function"] != expected_function:
                problems.append(
                    f"{where}: csf_function is {row['csf_function']!r}, {sub_id[:2]} belongs to {expected_function!r}"
                )

        if sub_id in seen:
            problems.append(f"{where}: duplicate csf_subcategory_id")
        seen.add(sub_id)

        try:
            weight = float(row["weight"])
        except ValueError:
            problems.append(f"{where}: weight {row['weight']!r} is not a number")
        else:
            if weight <= 0:
                problems.append(f"{where}: weight {weight} must be greater than zero")

    return problems


def test_lookup_file_is_valid():
    assert _problems(LOOKUP) == []


def test_lookup_ids_match_the_checklist_template():
    """The template is the import format and the CLI's input. The two must name the same 25 controls."""
    with open(LOOKUP, newline="", encoding="utf-8") as f:
        lookup_ids = {row["csf_subcategory_id"] for row in csv.DictReader(f)}
    with open(CHECKLIST_TEMPLATE, newline="", encoding="utf-8") as f:
        template_ids = {row["csf_subcategory_id"] for row in csv.DictReader(f)}

    assert lookup_ids == template_ids


def _valid_text():
    return LOOKUP.read_text(encoding="utf-8")


@pytest.mark.parametrize(
    ("old", "new", "expected"),
    [
        (",1.5,Define and document", ",hgh,Define and document", "weight 'hgh' is not a number"),
        (",1.5,Define and document", ",0,Define and document", "must be greater than zero"),
        (",1.5,Define and document", ",-1,Define and document", "must be greater than zero"),
        ("GV.RR-01,Govern", "GV.PO-01,Govern", "duplicate csf_subcategory_id"),
        ("GV.RR-01,Govern", "GV.RR-01,Identify", "belongs to 'Govern'"),
        ("GV.RR-01,Govern", "GV.RR-1,Govern", "does not look like a CSF 2.0 ID"),
        (
            '"Security policy document, communication records, staff acknowledgments"',
            "Security policy document, communication records, staff acknowledgments",
            "fields, expected 8",
        ),
    ],
    ids=["typo-weight", "zero-weight", "negative-weight", "duplicate-id", "wrong-function", "bad-id", "ragged-row"],
)
def test_validator_catches_a_corrupted_file(tmp_path, old, new, expected):
    """The check is only worth having if it fails on the mistakes it exists for."""
    text = _valid_text()
    assert text.count(old) == 1, f"fixture drifted: {old!r} no longer unique in csf_lookup.csv"

    broken = tmp_path / "csf_lookup.csv"
    broken.write_text(text.replace(old, new), encoding="utf-8")

    assert any(expected in problem for problem in _problems(broken))


def test_validator_catches_a_missing_row(tmp_path):
    lines = _valid_text().splitlines(keepends=True)
    short = tmp_path / "csf_lookup.csv"
    short.write_text("".join(lines[:-1]), encoding="utf-8")

    assert any("24 rows, expected 25" in problem for problem in _problems(short))


def test_validator_catches_an_empty_cell(tmp_path):
    text = _valid_text()
    old = "Has a formal cybersecurity policy been established and communicated to the organization?"
    assert text.count(old) == 1

    broken = tmp_path / "csf_lookup.csv"
    broken.write_text(text.replace(old, ""), encoding="utf-8")

    assert any("question is empty" in problem for problem in _problems(broken))
