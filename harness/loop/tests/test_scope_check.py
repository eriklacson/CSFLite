"""Tests for harness/loop/scope-check.sh and the scope gate in approve.sh.

Plans scope-template-check (the first 21 tests) and scope-check-fixes (the tests after the marker below).

Each test builds a throwaway git repo in tmp_path, copies the real loop scripts and the real scope
template into it, and runs the scripts there. test_template_change_changes_rules proves that a change
to the template changes what the check requires.

Output convention the tests pin:
- scope-check.sh <file> exits 0 and prints "PASS <file>", or exits 1 and prints "FAIL <file>" followed
  by one line per broken check, each naming its check ID (V-1 to V-7).
- scope-check.sh with no argument exits 2.
- approve.sh exits 4 when the plan's scope_doc is missing, not a file, the template itself, not
  `ready for plan`, or fails the scope check.
- scope-check.sh --all prints "WARN ..." for a plan whose scope_doc is not a file, and still exits 0.
"""

import shutil
import subprocess
from pathlib import Path

import pytest

REAL = Path(__file__).resolve().parents[3]
LOOP_FILES = ["planlib.py", "approve.sh", "mark-done.sh", "scope-check.sh"]
TEMPLATE = "docs/scopes/template.scope.md"

GOOD = """---
doc: scope
scope: 01-sample
spec_outcomes: []
status: ready for plan
version: 0.1
date: 2026-11-28
---

# Scope 01-sample — Sample

> A sample scope used by the tests.

## 1. What this scope delivers

A sample deliverable.

## 2. Rows it covers

| Record | Row ID |
|---|---|
| docs/specs/standards.md | INV-1 |

## 3. Success criteria

| ID | Criterion | Checked by |
|---|---|---|
| SC-1 | It works | `poetry run pytest` |
| SC-2 | It reads well | human |

## 4. Deliverables

| ID | Deliverable | Description |
|---|---|---|
| D-1 | A thing | The thing itself |

## 5. Not in this scope

| ID | Left out | Why |
|---|---|---|
| NG-1 | Another thing | Later |

## 6. Open items

| ID | Item | Why it is still open | What it blocks |
|---|---|---|---|
"""

PLAN = """---
plan: {stub}
scope_doc: {scope_doc}
status: draft
round_limit: 3
---

# Plan {stub}

## Tasks

| ID | Task | Depends on | Check | Round limit | Status |
|---|---|---|---|---|---|
| T-1 | Do it | — | `bash harness/plans/{stub}/{stub}.check.sh T-1` | 3 | todo |
"""


def git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=True)


@pytest.fixture
def repo(tmp_path):
    """A git repo with the real loop scripts, the real template and a standards record."""
    (tmp_path / "harness" / "loop").mkdir(parents=True)
    (tmp_path / "harness" / "plans").mkdir()
    (tmp_path / "harness" / "drafts").mkdir()
    for name in LOOP_FILES:
        src = REAL / "harness" / "loop" / name
        if src.exists():  # scope-check.sh does not exist until T-2, so its tests fail until then
            shutil.copy(src, tmp_path / "harness" / "loop" / name)
    (tmp_path / "docs" / "scopes").mkdir(parents=True)
    shutil.copy(REAL / TEMPLATE, tmp_path / TEMPLATE)
    (tmp_path / "docs" / "specs").mkdir()
    (tmp_path / "docs" / "specs" / "standards.md").write_text("| INV-1 | A rule |\n", encoding="utf-8")
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "test@example.com")
    git(tmp_path, "config", "user.name", "test")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-qm", "init")
    return tmp_path


def write(repo, rel, text):
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return rel


def scope_check(repo, *args):
    r = subprocess.run(["bash", "harness/loop/scope-check.sh", *args], cwd=repo, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def assert_fails(repo, text, check_id):
    rel = write(repo, "docs/scopes/01-sample.scope.md", text)
    code, out = scope_check(repo, rel)
    assert code == 1, out
    assert f"FAIL {rel}" in out, out
    assert check_id in out, out


def approve(repo, stub, scope_doc, task="Do it"):
    plan = PLAN.format(stub=stub, scope_doc=scope_doc).replace("| T-1 | Do it |", f"| T-1 | {task} |")
    write(repo, f"harness/drafts/{stub}/{stub}.plan.md", plan)
    write(repo, f"harness/drafts/{stub}/{stub}.check.sh", "#!/usr/bin/env bash\nexit 0\n")
    write(repo, f"harness/drafts/{stub}/{stub}.gate.yaml", "gate: []\n")
    r = subprocess.run(["bash", "harness/loop/approve.sh", stub], cwd=repo, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


# --- single file: V-1 to V-8 ----------------------------------------------------------------------


def test_good_scope_passes(repo):
    rel = write(repo, "docs/scopes/01-sample.scope.md", GOOD)
    code, out = scope_check(repo, rel)
    assert code == 0, out
    assert f"PASS {rel}" in out


def test_missing_frontmatter_key_fails(repo):
    assert_fails(repo, GOOD.replace("version: 0.1\n", ""), "V-1")


def test_wrong_doc_type_fails(repo):
    assert_fails(repo, GOOD.replace("doc: scope", "doc: plan"), "V-1")


def test_bad_status_fails(repo):
    assert_fails(repo, GOOD.replace("status: ready for plan", "status: done"), "V-1")


def test_bad_stub_fails(repo):
    assert_fails(repo, GOOD.replace("scope: 01-sample", "scope: 01_Sample"), "V-1")


def test_missing_section_fails(repo):
    start = GOOD.index("## 5. Not in this scope")
    end = GOOD.index("## 6. Open items")
    assert_fails(repo, GOOD[:start] + GOOD[end:], "V-2")


def test_sections_out_of_order_fail(repo):
    s3 = GOOD.index("## 3. Success criteria")
    s4 = GOOD.index("## 4. Deliverables")
    s5 = GOOD.index("## 5. Not in this scope")
    swapped = GOOD[:s3] + GOOD[s4:s5] + GOOD[s3:s4] + GOOD[s5:]
    assert_fails(repo, swapped, "V-2")


def test_extra_section_fails(repo):
    assert_fails(repo, GOOD + "\n## 7. Extra\n\nMore.\n", "V-2")


def test_wrong_table_columns_fail(repo):
    assert_fails(repo, GOOD.replace("| ID | Criterion | Checked by |", "| ID | Criterion | Owner |"), "V-3")


def test_no_success_criterion_fails(repo):
    text = GOOD.replace("| SC-1 | It works | `poetry run pytest` |\n", "").replace(
        "| SC-2 | It reads well | human |\n", ""
    )
    assert_fails(repo, text, "V-4")


def test_no_deliverable_fails(repo):
    assert_fails(repo, GOOD.replace("| D-1 | A thing | The thing itself |\n", ""), "V-4")


def test_empty_checked_by_fails(repo):
    assert_fails(repo, GOOD.replace("| SC-2 | It reads well | human |", "| SC-2 | It reads well | |"), "V-5")


def test_duplicate_id_fails(repo):
    assert_fails(repo, GOOD.replace("| SC-2 | It reads well |", "| SC-1 | It reads well |"), "V-6")


def test_bad_id_prefix_fails(repo):
    assert_fails(repo, GOOD.replace("| D-1 | A thing |", "| DL-1 | A thing |"), "V-6")


def test_row_id_missing_from_record_fails(repo):
    assert_fails(
        repo, GOOD.replace("| docs/specs/standards.md | INV-1 |", "| docs/specs/standards.md | INV-99 |"), "V-7"
    )


def test_template_is_skipped(repo):
    code, out = scope_check(repo, TEMPLATE)
    assert code == 0, out


# --- --all discovery ------------------------------------------------------------------------------


def test_all_finds_scope_by_frontmatter(repo):
    # A broken scope outside docs/scopes/ is found by its frontmatter, not its folder.
    rel = write(
        repo, "docs/specs/phase-x/some-scope.md", GOOD.replace("| SC-2 | It reads well | human |", "| SC-2 | x | |")
    )
    git(repo, "add", "-A")
    code, out = scope_check(repo, "--all")
    assert code == 1, out
    assert rel in out, out


def test_all_checks_plan_scope_doc(repo):
    # A plan's scope_doc is checked even when the file has no scope frontmatter.
    rel = write(repo, "docs/specs/old-scope.md", "# An old free-form scope\n\n- a bullet\n")
    write(repo, "harness/plans/old-plan/old-plan.plan.md", PLAN.format(stub="old-plan", scope_doc=rel))
    git(repo, "add", "-A")
    code, out = scope_check(repo, "--all")
    assert code == 1, out
    assert rel in out, out


# --- approve.sh gate ------------------------------------------------------------------------------


def test_approve_refuses_missing_scope_doc(repo):
    code, out = approve(repo, "no-scope", "none yet")
    assert code == 4, out
    assert (repo / "harness" / "drafts" / "no-scope").exists(), "nothing may move on refusal"


def test_approve_refuses_failing_scope(repo):
    bad = GOOD.replace("| D-1 | A thing | The thing itself |\n", "")
    rel = write(repo, "docs/scopes/01-sample.scope.md", bad)
    code, out = approve(repo, "bad-scope", rel)
    assert code == 4, out
    assert "V-4" in out, out
    assert (repo / "harness" / "drafts" / "bad-scope").exists(), "nothing may move on refusal"


def test_approve_accepts_good_scope(repo):
    rel = write(repo, "docs/scopes/01-sample.scope.md", GOOD)
    code, out = approve(repo, "good-scope", rel)
    assert code == 0, out
    assert f"PASS {rel}" in out, out
    assert (repo / "harness" / "plans" / "good-scope" / "good-scope.approved.sha").exists()


# --- plan scope-check-fixes: tests written before the fixes --------------------------------------


def test_approve_refuses_template_scope(repo):
    code, out = approve(repo, "tpl-scope", TEMPLATE)
    assert code == 4, out
    assert (repo / "harness" / "drafts" / "tpl-scope").exists(), "nothing may move on refusal"


def test_approve_refuses_draft_scope(repo):
    rel = write(repo, "docs/scopes/01-sample.scope.md", GOOD.replace("status: ready for plan", "status: draft"))
    code, out = approve(repo, "draft-scope", rel)
    assert code == 4, out
    assert "ready for plan" in out, out
    assert (repo / "harness" / "drafts" / "draft-scope").exists(), "nothing may move on refusal"


def test_escaped_pipe_in_scope_cell_is_text(repo):
    # An escaped pipe inside a cell is text, not a cell border.
    rel = write(repo, "docs/scopes/01-sample.scope.md", GOOD.replace("| SC-2 | It reads well |", r"| SC-2 | a \| b |"))
    code, out = scope_check(repo, rel)
    assert code == 0, out
    # So an empty Checked by cell after it is still caught (P-6).
    assert_fails(repo, GOOD.replace("| SC-2 | It reads well | human |", r"| SC-2 | a \| b | |"), "V-5")


def test_escaped_pipe_in_task_row_is_text(repo):
    rel = write(repo, "docs/scopes/01-sample.scope.md", GOOD)
    code, out = approve(repo, "pipe-plan", rel, task=r"Do a \| b")
    assert code == 0, out
    r = subprocess.run(
        ["bash", "harness/loop/mark-done.sh", "pipe-plan", "T-1"], cwd=repo, capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr
    plan = (repo / "harness" / "plans" / "pipe-plan" / "pipe-plan.plan.md").read_text(encoding="utf-8")
    row = next(line for line in plan.splitlines() if line.startswith("| T-1 |"))
    assert row.rstrip().endswith("| 3 | done |"), row


def test_short_row_fails(repo):
    assert_fails(repo, GOOD.replace("| SC-2 | It reads well | human |", "| SC-2 | It reads well |"), "V-3")


def test_empty_row_id_fails(repo):
    assert_fails(repo, GOOD.replace("| docs/specs/standards.md | INV-1 |", "| docs/specs/standards.md | |"), "V-7")


def test_record_outside_repo_fails(repo, tmp_path):
    outside = tmp_path.parent / f"{tmp_path.name}-outside.md"
    outside.write_text("| X-1 | A row outside the repo |\n", encoding="utf-8")
    assert_fails(repo, GOOD.replace("| docs/specs/standards.md | INV-1 |", f"| {outside} | X-1 |"), "V-7")


def test_row_id_only_in_prose_fails(repo):
    (repo / "docs" / "specs" / "standards.md").write_text(
        "| INV-1 | A rule |\n\nINV-2 is only mentioned in prose.\n", encoding="utf-8"
    )
    assert_fails(
        repo, GOOD.replace("| docs/specs/standards.md | INV-1 |", "| docs/specs/standards.md | INV-2 |"), "V-7"
    )


def test_id_only_criterion_does_not_count(repo):
    text = GOOD.replace("| SC-1 | It works | `poetry run pytest` |\n", "").replace(
        "| SC-2 | It reads well | human |", "| SC-1 | | human |"
    )
    assert_fails(repo, text, "V-4")


def test_open_item_bad_prefix_fails(repo):
    row = "| X-1 | Something | Because | Nothing |\n"
    assert_fails(repo, GOOD.rstrip("\n") + "\n" + row, "V-6")


def test_all_fails_scope_doc_outside_repo(repo, tmp_path):
    outside = tmp_path.parent / f"{tmp_path.name}-outside-scope.md"
    outside.write_text(GOOD, encoding="utf-8")
    write(repo, "harness/plans/out-plan/out-plan.plan.md", PLAN.format(stub="out-plan", scope_doc=f"../{outside.name}"))
    git(repo, "add", "-A")
    code, out = scope_check(repo, "--all")
    assert code == 1, out
    assert "outside the repo" in out, out


def test_all_draft_without_scope(repo):
    write(repo, "harness/drafts/no-scope/no-scope.plan.md", PLAN.format(stub="no-scope", scope_doc="none yet"))
    git(repo, "add", "-A")
    code, out = scope_check(repo, "--all")
    assert code == 0, out
    assert "WARN" in out, out
    assert "no-scope" in out, out


def test_template_change_changes_rules(repo):
    # Add a required section to the repo's template. A scope without it must now fail.
    template = repo / TEMPLATE
    template.write_text(
        template.read_text(encoding="utf-8") + "\n## 7. Risks\n\n| ID | Risk |\n|---|---|\n", encoding="utf-8"
    )
    assert_fails(repo, GOOD, "V-2")
