#!/usr/bin/env bash
# Check script for plan scope-check-fixes. Usage: check.sh T-1 ... T-6
# Exit 0 only if the named task's check passes. Run from anywhere inside the repo.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2
TASK="${1:-}"

python3 -I - "$TASK" <<'PY'
import re, subprocess, sys
from pathlib import Path

task = sys.argv[1]
TESTS = Path("harness/loop/tests/test_scope_check.py")
TEMPLATE = "docs/scopes/template.scope.md"
DOCS_ALLOWED = {TEMPLATE, "docs/scopes/scope-check-fixes.scope.md"}
NEW_TESTS = [
    "test_approve_refuses_template_scope",
    "test_approve_refuses_draft_scope",
    "test_escaped_pipe_in_scope_cell_is_text",
    "test_escaped_pipe_in_task_row_is_text",
    "test_short_row_fails",
    "test_empty_row_id_fails",
    "test_record_outside_repo_fails",
    "test_row_id_only_in_prose_fails",
    "test_id_only_criterion_does_not_count",
    "test_open_item_bad_prefix_fails",
    "test_all_fails_scope_doc_outside_repo",
    "test_all_draft_without_scope",
    "test_template_change_changes_rules",
]
T3_TESTS = "short_row or empty_row_id or record_outside_repo or only_in_prose or id_only_criterion or open_item_bad_prefix or all_fails_scope_doc or all_draft_without_scope or template_change"


def fail(msg):
    print(f"FAIL {task}: {msg}")
    sys.exit(1)


def run(*cmd):
    return subprocess.run(list(cmd), capture_output=True, text=True)


def read(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"{path} not found")


def base():
    for ref in ("origin/harness/scope-template-check", "origin/master"):
        r = run("git", "merge-base", "HEAD", ref)
        if r.returncode == 0:
            return r.stdout.strip()
    fail("cannot find a merge base")


def pytest(*extra):
    r = run("poetry", "run", "python", "-m", "pytest", "-q", "harness/loop/tests", *extra)
    if r.returncode != 0:
        fail("harness tests failed:\n" + (r.stdout + r.stderr)[-2000:])


def docs_changed_only_allowed():
    changed = set(run("git", "diff", "--name-only", base(), "--", "docs/").stdout.split())
    changed |= set(run("git", "diff", "--name-only", "--", "docs/").stdout.split())
    changed |= set(run("git", "ls-files", "--others", "--exclude-standard", "docs/").stdout.split())
    extra = sorted(changed - DOCS_ALLOWED)
    if extra:
        fail("files in docs/ changed that this plan does not list: " + ", ".join(extra))


def scopes_row():
    return next((l for l in read("AGENTS.md").splitlines() if l.startswith("| scopes |")), "")


if task == "T-1":
    body = read(TESTS)
    missing = [t for t in NEW_TESTS if not re.search(rf"^def {t}\(", body, re.M)]
    if missing:
        fail("missing tests: " + ", ".join(missing))

elif task == "T-2":
    pytest("-k", "escaped_pipe")

elif task == "T-3":
    pytest("-k", T3_TESTS)
    if not re.search(r"^\| OI-1 \|", read(TEMPLATE), re.M):
        fail("the template's Open items table has no OI-1 example row")
    r = run("bash", "harness/loop/scope-check.sh", "--all")
    if r.returncode != 0:
        fail("scope-check.sh --all failed:\n" + r.stdout + r.stderr)
    docs_changed_only_allowed()

elif task == "T-4":
    # Selecting by name: pytest exits non-zero if these tests do not exist yet.
    pytest("-k", "approve_refuses_template_scope or approve_refuses_draft_scope")
    pytest()

elif task == "T-5":
    row = scopes_row()
    if not row:
        fail("AGENTS.md has no scopes row")
    if "`harness/loop/scope-check.sh` checks this" in row:
        fail("AGENTS.md still says scope-check.sh checks that every plan names a scope")
    for want in ("`approve.sh`", "ready for plan"):
        if want not in row:
            fail(f"AGENTS.md scopes row does not mention {want}")
    readme = read("harness/loop/README.md")
    for want in ("template itself", "ready for plan"):
        if want not in readme:
            fail(f"harness/loop/README.md does not mention '{want}'")
    p11 = next((l for l in read("harness/rules.md").splitlines() if l.startswith("| P-11 |")), "")
    if "ready for plan" not in p11:
        fail("harness/rules.md P-11 does not mention 'ready for plan'")
    docs_changed_only_allowed()

elif task == "T-6":
    code = """
import sys
sys.path.insert(0, "harness/loop")
import planlib
stub = "scope-template-check"
_d, plan, _c, _s = planlib.files(stub)
lines = plan.read_text(encoding="utf-8").splitlines(keepends=True)
for _i, cols, cells, s in planlib.task_rows(lines):
    if cells[cols.index("ID")] == "T-2":
        rl, st = cells[cols.index("Round limit")], cells[s]
        if (rl, st) != ("3", "done"):
            print(f"T-2 reads Round limit {rl!r}, Status {st!r}; expected '3', 'done'")
            sys.exit(1)
        break
else:
    print("no T-2 row found")
    sys.exit(1)
planlib.verify_sha(stub)
"""
    r = run("python3", "-c", code)
    if r.returncode != 0:
        fail((r.stdout + r.stderr).strip())

else:
    print("usage: check.sh T-1 ... T-6")
    sys.exit(2)

print(f"PASS {task}")
PY
