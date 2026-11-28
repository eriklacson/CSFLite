#!/usr/bin/env bash
# Check script for plan scope-template-check. Usage: check.sh T-1 ... T-6
# Exit 0 only if the named task's check passes. Run from anywhere inside the repo.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2
TASK="${1:-}"

python3 -I - "$TASK" <<'PY'
import re, subprocess, sys
from pathlib import Path

task = sys.argv[1]
SCOPE = "docs/specs/phase-4/web-interface-scope.md"
TESTS = Path("harness/loop/tests/test_scope_check.py")
WRAPPER = Path("harness/loop/scope-check.sh")
DOCS_ALLOWED = {SCOPE}
REQUIRED_TESTS = [
    "test_good_scope_passes",
    "test_missing_frontmatter_key_fails",
    "test_wrong_doc_type_fails",
    "test_bad_status_fails",
    "test_bad_stub_fails",
    "test_missing_section_fails",
    "test_sections_out_of_order_fail",
    "test_extra_section_fails",
    "test_wrong_table_columns_fail",
    "test_no_success_criterion_fails",
    "test_no_deliverable_fails",
    "test_empty_checked_by_fails",
    "test_duplicate_id_fails",
    "test_bad_id_prefix_fails",
    "test_row_id_missing_from_record_fails",
    "test_template_is_skipped",
    "test_all_finds_scope_by_frontmatter",
    "test_all_checks_plan_scope_doc",
    "test_approve_refuses_missing_scope_doc",
    "test_approve_refuses_failing_scope",
    "test_approve_accepts_good_scope",
]


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
    r = run("git", "merge-base", "HEAD", "origin/master")
    if r.returncode != 0:
        fail("cannot find merge base with origin/master")
    return r.stdout.strip()


def pytest(*extra):
    r = run("poetry", "run", "python", "-m", "pytest", "-q", "harness/loop/tests", *extra)
    if r.returncode != 0:
        fail("harness tests failed:\n" + (r.stdout + r.stderr)[-2000:])


def docs_changed_only_allowed():
    changed = set(run("git", "diff", "--name-only", base(), "--", "docs/").stdout.split())
    changed |= set(run("git", "diff", "--name-only", "--", "docs/").stdout.split())
    extra = sorted(changed - DOCS_ALLOWED)
    if extra:
        fail("files in docs/ changed that this plan does not list: " + ", ".join(extra))


def table_rows(text, heading_pat):
    """Data rows of the first table under the heading that matches heading_pat."""
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if re.match(heading_pat, l)), None)
    if start is None:
        fail(f"no heading matching {heading_pat!r} in {SCOPE}")
    rows, seen_sep = [], False
    for l in lines[start + 1:]:
        if l.startswith("## "):
            break
        if l.startswith("|"):
            if re.match(r"^\|[\s:|-]+\|\s*$", l):
                seen_sep = True
            elif seen_sep:
                rows.append([c.strip() for c in l.strip().strip("|").split("|")])
    return rows


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


if task == "T-1":
    if not TESTS.exists():
        fail(f"{TESTS} not found")
    body = TESTS.read_text(encoding="utf-8")
    missing = [t for t in REQUIRED_TESTS if not re.search(rf"^def {t}\(", body, re.M)]
    if missing:
        fail("missing tests: " + ", ".join(missing))
    if "harness/" not in read("pyproject.toml").split("per-file-ignores", 1)[-1]:
        fail("pyproject.toml per-file-ignores does not cover the harness tests")

elif task == "T-2":
    if not WRAPPER.exists():
        fail(f"{WRAPPER} not found")
    if run("bash", str(WRAPPER)).returncode != 2:
        fail("scope-check.sh with no argument should exit 2 (usage)")
    if run("bash", str(WRAPPER), "docs/scopes/template.scope.md").returncode != 0:
        fail("the template must be skipped and pass")
    pytest("-k", "not approve")

elif task == "T-3":
    pytest()
    if "scope_doc" not in read("harness/loop/planlib.py"):
        fail("planlib.py approve does not read scope_doc")

elif task == "T-4":
    r = run("bash", str(WRAPPER), SCOPE)
    if r.returncode != 0:
        fail("scope-check failed on the Phase 4 scope:\n" + r.stdout + r.stderr)
    old = run("git", "show", f"{base()}:{SCOPE}").stdout
    new = norm(read(SCOPE))
    lost = [norm(l[2:]) for l in old.splitlines() if l.startswith("- ") and norm(l[2:]) not in new]
    if lost:
        fail("bullet text lost:\n  " + "\n  ".join(x[:90] for x in lost))
    text = read(SCOPE)
    counts = {
        "success criteria": (len(table_rows(text, r"^## 3\. ")), 6),
        "deliverables": (len(table_rows(text, r"^## 4\. ")), 11),
        "not in this scope": (len(table_rows(text, r"^## 5\. ")), 9),
    }
    wrong = [f"{k}: {got}, expected {want}" for k, (got, want) in counts.items() if got != want]
    if wrong:
        fail("; ".join(wrong))
    docs_changed_only_allowed()

elif task == "T-5":
    pc = read(".pre-commit-config.yaml")
    if "id: scope-check" not in pc or "harness/loop/scope-check.sh --all" not in pc:
        fail("pre-commit has no scope-check hook running scope-check.sh --all")
    ci = read(".github/workflows/python-lint.yaml")
    if "harness/loop/scope-check.sh --all" not in ci:
        fail("CI does not run scope-check.sh --all")
    if "harness/loop/tests" not in ci:
        fail("CI does not run the harness tests")
    r = run("bash", str(WRAPPER), "--all")
    if r.returncode != 0:
        fail("scope-check.sh --all failed:\n" + r.stdout + r.stderr)

elif task == "T-6":
    rules = read("harness/rules.md")
    for rid in ("P-5", "P-6", "P-11"):
        row = next((l for l in rules.splitlines() if l.startswith(f"| {rid} |")), None)
        if row is None:
            fail(f"no {rid} row in harness/rules.md")
        if "| installed |" not in row:
            fail(f"{rid} is not marked installed")
    if "scope-check.sh" not in read("harness/loop/README.md"):
        fail("harness/loop/README.md does not list scope-check.sh")
    if "doc: scope" not in read("AGENTS.md"):
        fail("AGENTS.md does not say scope files are found by doc: scope")
    docs_changed_only_allowed()

else:
    print("usage: check.sh T-1 ... T-6")
    sys.exit(2)

print(f"PASS {task}")
PY
