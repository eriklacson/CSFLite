#!/usr/bin/env python3
"""Shared logic for the jig loop scripts. Called by approve.sh and mark-done.sh, not directly.

approve <stub>
    Run by the architect at plan approval. Moves harness/drafts/<stub>/ to harness/plans/<stub>/
    (if it is still a draft), sets the front matter to `status: approved`, writes
    <stub>.approved.sha and points harness/plans/CURRENT at the stub.

mark-done <stub> <task-id>
    Refuses if the plan or check script differs from <stub>.approved.sha (rule P-2), or if a task
    it depends on is not done. Runs the task's check. Writes `done` in the Status column only if
    the check exits 0 (rule P-1).

scope-check <file> | --all
    Checks that a scope file follows docs/scopes/template.scope.md (rule P-11, with P-4, P-5, P-6).
    The rules are read from the template itself. --all checks every tracked file whose frontmatter says
    `doc: scope`, and every draft or approved plan's scope_doc that is a file.

The approval hash ignores the Status column, so mark-done can write status without breaking it.

Exit codes: 0 ok, 1 check failed, 2 usage error, 3 approval hash mismatch, 4 task cannot run.
"""

import hashlib
import re
import subprocess
import sys
from pathlib import Path

STUB_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SEP_RE = re.compile(r"^\|[\s:|-]+\|\s*$")
UNESCAPED_PIPE_RE = re.compile(r"(?<!\\)\|")


def die(code, msg):
    print(msg, file=sys.stderr)
    sys.exit(code)


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True)  # noqa: S603, S607


ROOT = Path(git("rev-parse", "--show-toplevel").stdout.strip() or ".")
PLANS = ROOT / "harness" / "plans"
DRAFTS = ROOT / "harness" / "drafts"
TEMPLATE = ROOT / "docs" / "scopes" / "template.scope.md"


def files(stub):
    d = PLANS / stub
    return d, d / f"{stub}.plan.md", d / f"{stub}.check.sh", d / f"{stub}.approved.sha"


def check_stub(stub):
    if not STUB_RE.match(stub):
        die(2, f"bad stub '{stub}': use lowercase letters, digits and hyphens")


# --- the tasks table -------------------------------------------------------------------------


def split_row(line):
    """Raw segments between pipes, so a row can be rebuilt with only one cell changed.

    A pipe with a backslash before it (an escaped pipe, as Markdown tables write one) is text inside a
    cell, not a border. Rebuilding with "|".join() restores the row exactly.
    """
    return UNESCAPED_PIPE_RE.split(line.rstrip("\n"))


def task_rows(lines):
    """Yield (line index, cells, status index) for each row of the tasks table.

    The tasks table is any table whose header has both an ID and a Status column.
    """
    i = 0
    while i < len(lines) - 1:
        header = lines[i]
        if header.startswith("|") and SEP_RE.match(lines[i + 1]):
            cols = [c.strip() for c in split_row(header)[1:-1]]
            i += 2
            if "ID" in cols and "Status" in cols:
                status = cols.index("Status")
                while i < len(lines) and lines[i].startswith("|"):
                    cells = [c.strip() for c in split_row(lines[i])[1:-1]]
                    yield i, cols, cells, status
                    i += 1
            continue
        i += 1


def set_status(line, status_idx, value):
    seg = split_row(line)
    seg[status_idx + 1] = f" {value} "
    return "|".join(seg) + "\n"


def normalized(plan_text):
    """The plan with every Status cell blanked, so status changes do not alter the hash."""
    lines = plan_text.splitlines(keepends=True)
    for i, _cols, _cells, s in list(task_rows(lines)):
        lines[i] = set_status(lines[i], s, "")
    return "".join(lines)


def sha(data):
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def expected_hashes(stub):
    _d, plan, check, _s = files(stub)
    return {
        plan.name: sha(normalized(plan.read_text(encoding="utf-8"))),
        check.name: sha(check.read_text(encoding="utf-8")),
    }


def write_sha(stub):
    _d, _p, _c, shafile = files(stub)
    body = "# Approval hash. The plan hash ignores the Status column.\n"
    body += "".join(f"{h}  {name}\n" for name, h in expected_hashes(stub).items())
    shafile.write_text(body, encoding="utf-8")


def verify_sha(stub):
    _d, _p, _c, shafile = files(stub)
    if not shafile.exists():
        die(3, f"{shafile.relative_to(ROOT)} is missing. The plan was not approved with approve.sh.")
    recorded = {}
    for line in shafile.read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#"):
            h, name = line.split(None, 1)
            recorded[name.strip()] = h
    now = expected_hashes(stub)
    changed = [n for n in now if recorded.get(n) != now[n]]
    if changed or set(recorded) != set(now):
        die(3, "REFUSED: changed since approval (rule P-2): " + ", ".join(changed or sorted(set(recorded) ^ set(now))))


def deps(text):
    if text.strip() in ("", "—", "-"):
        return []
    out = []
    for a, b in re.findall(r"T-(\d+)\s+to\s+T-(\d+)", text):
        out += [f"T-{n}" for n in range(int(a), int(b) + 1)]
    text = re.sub(r"T-\d+\s+to\s+T-\d+", "", text)
    out += re.findall(r"T-\d+", text)
    return out


# --- scope files ---------------------------------------------------------------------------------


def frontmatter(text):
    """The frontmatter as a dict, with trailing `# comments` dropped. None if the text has none."""
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    out = {}
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if km:
            out[km.group(1)] = re.sub(r"\s+#.*$", "", km.group(2)).strip()
    return out


def sections(text):
    """[(heading, [lines])] for every `## ` heading, in order."""
    out = []
    for line in text.splitlines():
        if line.startswith("## "):
            out.append((line.strip(), []))
        elif out:
            out[-1][1].append(line)
    return out


def first_table(lines):
    """(columns, data rows) of the first table in lines. Rows with every cell empty are dropped."""
    for i in range(len(lines) - 1):
        if lines[i].startswith("|") and SEP_RE.match(lines[i + 1]):
            cols = [c.strip() for c in split_row(lines[i])[1:-1]]
            rows = []
            for line in lines[i + 2 :]:
                if not line.startswith("|"):
                    break
                cells = [c.strip() for c in split_row(line)[1:-1]]
                if any(cells):
                    rows.append(cells)
            return cols, rows
    return None, []


def template_rules():
    """What a scope must have, read from the template: keys, statuses, headings, columns, ID prefixes."""
    if not TEMPLATE.exists():
        die(2, f"scope template not found: {TEMPLATE.relative_to(ROOT)}")
    text = TEMPLATE.read_text(encoding="utf-8")
    keys = list(frontmatter(text) or {})
    statuses = ["draft", "ready for plan"]
    sm = re.search(r"^status:.*#\s*(.+)$", text, re.M)
    if sm:
        statuses = [x.strip() for x in sm.group(1).split("|") if x.strip()]
    heads, columns, prefixes = [], {}, {}
    for head, lines in sections(text):
        heads.append(head)
        cols, _rows = first_table(lines)
        columns[head] = cols
        # The template's example row (`| SC-1 | | |`) gives the section's ID prefix.
        for line in lines:
            pm = re.match(r"^\|\s*([A-Z]+)-1\s*\|", line)
            if pm:
                prefixes[head] = pm.group(1)
                break
    return keys, statuses, heads, columns, prefixes


def scope_problems(path):
    """A list of 'V-n: message' strings. Empty means the scope passes."""
    keys, statuses, heads, columns, prefixes = template_rules()
    text = path.read_text(encoding="utf-8")
    problems = []

    fm = frontmatter(text)
    if fm is None:
        problems.append("V-1: no frontmatter. A scope starts with the template's frontmatter")
        fm = {}
    else:
        missing = [k for k in keys if k not in fm]
        if missing:
            problems.append("V-1: frontmatter is missing " + ", ".join(missing))
        if fm.get("doc") != "scope":
            problems.append(f"V-1: doc is '{fm.get('doc', '')}', expected 'scope'")
        if "status" in fm and fm["status"] not in statuses:
            problems.append(f"V-1: status is '{fm['status']}', expected one of: " + ", ".join(statuses))
        if "scope" in fm and not STUB_RE.match(fm["scope"]):
            problems.append(f"V-1: scope '{fm['scope']}' is not a stub (lowercase letters, digits, hyphens)")

    secs = sections(text)
    found = [h for h, _l in secs]
    if found != heads:
        problems.append("V-2: section headings must be exactly, in order: " + " / ".join(heads))
    by_head = dict(secs)

    seen_ids = {}
    for head in heads:
        if head not in by_head:
            continue
        cols, rows = first_table(by_head[head])
        want = columns.get(head)
        if want and cols != want:
            problems.append(f"V-3: '{head}' table columns must be: " + " | ".join(want))
            continue
        if not want:
            continue
        prefix = prefixes.get(head)
        if prefix in ("SC", "D") and not rows:
            what = "success criterion" if prefix == "SC" else "deliverable"
            problems.append(f"V-4: '{head}' needs at least one {what}")
        for cells in rows:
            row = dict(zip(cols, cells, strict=False))
            rid = row.get("ID", "")
            if "Checked by" in row and not row["Checked by"]:
                problems.append(f"V-5: {rid or 'a criterion'} has an empty 'Checked by' cell")
            if "ID" in row:
                if prefix and not re.match(rf"^{prefix}-\d+$", rid):
                    problems.append(f"V-6: '{rid}' in '{head}' must look like {prefix}-1")
                if rid:
                    if rid in seen_ids:
                        problems.append(f"V-6: ID '{rid}' is used more than once")
                    seen_ids[rid] = head
            if "Record" in row and "Row ID" in row:
                record, row_id = row["Record"].strip("`"), row["Row ID"].strip("`")
                rec = ROOT / record
                if not rec.is_file():
                    problems.append(f"V-7: record '{record}' does not exist")
                elif not re.search(rf"(?<![\w-]){re.escape(row_id)}(?![\w-])", rec.read_text(encoding="utf-8")):
                    problems.append(f"V-7: row '{row_id}' is not in {record}")
    return problems


def rel(path):
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return str(path)


def check_scope_file(path):
    """Prints PASS or FAIL for one file. Returns True if it passes."""
    if path.resolve() == TEMPLATE.resolve():
        print(f"PASS {rel(path)} (the template itself is skipped)")
        return True
    if not path.is_file():
        print(f"FAIL {rel(path)}\n  file not found")
        return False
    problems = scope_problems(path)
    if problems:
        print(f"FAIL {rel(path)}")
        for p in problems:
            print(f"  {p}")
        return False
    print(f"PASS {rel(path)}")
    return True


def plan_scope_doc(plan_path):
    """The plan's scope_doc as a Path, or None if it names no file."""
    fm = frontmatter(plan_path.read_text(encoding="utf-8")) or {}
    value = fm.get("scope_doc", "")
    if not value:
        return None
    candidate = ROOT / value
    return candidate if candidate.is_file() else None


def all_scope_files():
    """Every tracked file with `doc: scope` frontmatter, plus every plan's scope_doc that is a file."""
    found = []
    for name in git("ls-files", "*.md").stdout.split():
        p = ROOT / name
        if p.resolve() == TEMPLATE.resolve() or not p.is_file():
            continue
        fm = frontmatter(p.read_text(encoding="utf-8"))
        if fm and fm.get("doc") == "scope":
            found.append(p)
    for plan in sorted([*PLANS.glob("*/*.plan.md"), *DRAFTS.glob("*/*.plan.md")]):
        doc = plan_scope_doc(plan)
        if doc and doc.resolve() not in {f.resolve() for f in found}:
            found.append(doc)
    return found


def scope_check(arg):
    if arg == "--all":
        targets = all_scope_files()
        if not targets:
            print("no scope files found")
            return
    else:
        p = Path(arg)
        targets = [p if p.is_absolute() else ROOT / p]
    results = [check_scope_file(t) for t in targets]
    if not all(results):
        sys.exit(1)


# --- commands --------------------------------------------------------------------------------


def approve(stub):
    check_stub(stub)
    draft, target = DRAFTS / stub, PLANS / stub
    if draft.exists() and target.exists():
        die(4, f"both {draft.relative_to(ROOT)} and {target.relative_to(ROOT)} exist")
    src = draft if draft.exists() else target
    if not src.exists():
        die(4, f"no draft or plan folder for '{stub}'")

    # Every check runs before anything moves or is written.
    plan, check, gate = (src / f"{stub}.{ext}" for ext in ("plan.md", "check.sh", "gate.yaml"))
    for f in (plan, check, gate):
        if not f.exists():
            die(4, f"missing {f.relative_to(ROOT)}")
    if (src / f"{stub}.approved.sha").exists():
        die(4, f"{stub}.approved.sha already exists. The plan is already approved.")
    text = plan.read_text(encoding="utf-8")
    # The plan's scope must exist and follow the scope template (P-11, with P-4, P-5, P-6).
    scope_value = (frontmatter(text) or {}).get("scope_doc", "")
    scope = plan_scope_doc(plan)
    if scope is None:
        die(4, f"REFUSED: the plan's scope_doc '{scope_value}' is not a file. Every plan needs a scope (P-11).")
    if not check_scope_file(scope):
        die(4, "REFUSED: the plan's scope does not follow docs/scopes/template.scope.md. Fix it, then approve.")
    if not list(task_rows(text.splitlines(keepends=True))):
        die(4, "the plan has no tasks table with ID and Status columns")
    current = PLANS / "CURRENT"
    if current.exists():
        other = current.read_text(encoding="utf-8").strip()
        other_plan = PLANS / other / f"{other}.plan.md"
        if other and other != stub and other_plan.exists():
            lines = other_plan.read_text(encoding="utf-8").splitlines(keepends=True)
            open_tasks = [c[cols.index("ID")] for _i, cols, c, s in task_rows(lines) if c[s] != "done"]
            if open_tasks:
                die(4, f"CURRENT is '{other}', which still has open tasks: {', '.join(open_tasks)}")

    if src is draft:
        if git("ls-files", str(draft)).stdout.strip():
            r = git("mv", str(draft), str(target))
            if r.returncode != 0:
                die(4, "git mv failed: " + r.stderr.strip())
        else:
            draft.rename(target)  # not tracked by git yet
        print(f"moved {draft.relative_to(ROOT)}/ -> {target.relative_to(ROOT)}/")

    _d, plan, _c, shafile = files(stub)
    text = re.sub(r"\A(---\n(?:.*\n)*?)status: draft\b", r"\1status: approved", text, count=1)
    plan.write_text(text, encoding="utf-8")
    write_sha(stub)
    current.write_text(stub + "\n", encoding="utf-8")
    print(f"wrote {shafile.relative_to(ROOT)}")
    print(f"CURRENT = {stub}")
    print("Commit these changes to record the approval.")


def mark_done(stub, task):
    check_stub(stub)
    d, plan, check, _s = files(stub)
    if not plan.exists():
        die(4, f"no approved plan at {plan.relative_to(ROOT)}")
    verify_sha(stub)

    lines = plan.read_text(encoding="utf-8").splitlines(keepends=True)
    rows = {c[cols.index("ID")]: (i, cols, c, s) for i, cols, c, s in task_rows(lines)}
    if task not in rows:
        die(4, f"no task {task} in the plan")
    i, cols, cells, s = rows[task]
    if cells[s] == "done":
        print(f"{task} is already done")
        return
    if "Depends on" in cols:
        open_deps = [
            t for t in deps(cells[cols.index("Depends on")]) if rows.get(t, (0, 0, {s: ""}, s))[2][s] != "done"
        ]
        if open_deps:
            die(4, f"{task} cannot run yet. Not done: {', '.join(open_deps)}")

    print(f"running: bash {check.relative_to(ROOT)} {task}", flush=True)
    r = subprocess.run(["bash", str(check.relative_to(ROOT)), task], cwd=ROOT)  # noqa: S603, S607
    if r.returncode != 0:
        print(f"NOT DONE: {task} check exited {r.returncode}. Status unchanged.")
        sys.exit(1)

    lines[i] = set_status(lines[i], s, "done")
    plan.write_text("".join(lines), encoding="utf-8")
    verify_sha(stub)  # the Status column is outside the hash, so this must still match
    left = [c[cols.index("ID")] for _i, cols, c, st in task_rows(lines) if c[st] != "done"]
    print(f"DONE: {task}. " + (f"Open: {', '.join(left)}" if left else "All tasks done."))


def main(argv):
    if len(argv) == 2 and argv[0] == "approve":
        approve(argv[1])
    elif len(argv) == 3 and argv[0] == "mark-done":
        mark_done(argv[1], argv[2])
    elif len(argv) == 2 and argv[0] == "scope-check":
        scope_check(argv[1])
    else:
        die(2, "usage: approve.sh <stub> | mark-done.sh <stub> <task-id> | scope-check.sh <file> | --all")


if __name__ == "__main__":
    main(sys.argv[1:])
