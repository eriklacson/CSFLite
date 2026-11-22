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


def die(code, msg):
    print(msg, file=sys.stderr)
    sys.exit(code)


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True)  # noqa: S603, S607


ROOT = Path(git("rev-parse", "--show-toplevel").stdout.strip() or ".")
PLANS = ROOT / "harness" / "plans"
DRAFTS = ROOT / "harness" / "drafts"


def files(stub):
    d = PLANS / stub
    return d, d / f"{stub}.plan.md", d / f"{stub}.check.sh", d / f"{stub}.approved.sha"


def check_stub(stub):
    if not STUB_RE.match(stub):
        die(2, f"bad stub '{stub}': use lowercase letters, digits and hyphens")


# --- the tasks table -------------------------------------------------------------------------


def split_row(line):
    """Raw segments between pipes, so a row can be rebuilt with only one cell changed."""
    return line.rstrip("\n").split("|")


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
    else:
        die(2, "usage: approve.sh <stub> | mark-done.sh <stub> <task-id>")


if __name__ == "__main__":
    main(sys.argv[1:])
