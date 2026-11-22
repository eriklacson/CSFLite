#!/usr/bin/env bash
# Check script for plan spec-brief-components. Usage: check.sh T-1|T-2|T-3|T-4
# Exit 0 only if the named task's check passes.
set -u
BRIEF="docs/specs/csflite-spec-brief.md"
TASK="${1:-}"

python3 -I - "$TASK" "$BRIEF" <<'PY'
import re, subprocess, sys

task, path = sys.argv[1], sys.argv[2]
text = open(path, encoding="utf-8").read()
lines = text.splitlines()
VALID = {"Control Set", "Assessment Method", "Toolkit", "Framework-wide"}

def fail(msg):
    print(f"FAIL {task}: {msg}")
    sys.exit(1)

def section(num):
    start = next((i for i, l in enumerate(lines) if l.startswith(f"## {num}. ")), None)
    if start is None:
        return []
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return lines[start:end]

if task == "T-1":
    s1 = "\n".join(section(1))
    for term in ("Control Set", "Assessment Method", "Toolkit"):
        if f"**{term}**" not in s1:
            fail(f"section 1 does not define **{term}**")
    if "engineer governance into systems" not in s1.lower():
        fail("section 1 does not state the principle")
    if "Method wins" not in s1 and "method wins" not in s1:
        fail("section 1 does not state that the Method wins on disagreement")
    if "may not add controls, weights or scoring rules" not in s1:
        fail("section 1 does not state the Toolkit limit")
    print("PASS T-1")

elif task == "T-2":
    in3 = False
    missing = []
    for i, l in enumerate(lines):
        m = re.match(r"(##|###) ", l)
        if not m:
            continue
        if l.startswith("## "):
            n = re.match(r"## (\d+)\.", l)
            in3 = bool(n and n.group(1) == "3")
            if not n or int(n.group(1)) < 2:
                continue
        elif not in3:
            continue
        nxt = [x for x in lines[i + 1 : i + 4] if x.strip()]
        ok = False
        if nxt:
            c = re.match(r"\*\*Component:\*\* (.+)$", nxt[0].strip())
            ok = bool(c and c.group(1).strip() in VALID)
        if not ok:
            missing.append(l)
    if missing:
        fail("no valid Component line under: " + "; ".join(missing))
    print("PASS T-2")

elif task == "T-3":
    for num, name in ((9, "milestones"), (10, "decisions")):
        rows = [l for l in section(num) if l.startswith("|")]
        # find the table with a Component column
        tbl = []
        grab = False
        for l in section(num):
            if l.startswith("|"):
                tbl.append(l)
            elif tbl and not grab:
                if any("Component" in t for t in tbl):
                    break
                tbl = []
        hdr = next((t for t in tbl if "Component" in t), None)
        if not hdr:
            fail(f"section {num} {name} table has no Component column")
        cols = [c.strip() for c in hdr.strip("|").split("|")]
        idx = cols.index("Component")
        for t in tbl[2:]:
            cells = [c.strip() for c in t.strip("|").split("|")]
            if len(cells) != len(cols) or cells[idx] not in VALID:
                fail(f"section {num} row has bad Component value: {t[:60]}")
    print("PASS T-3")

elif task == "T-4":
    head = subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True, text=True)
    if head.returncode != 0:
        fail("cannot read original brief from git HEAD")
    orig = head.stdout.splitlines()
    oh = [l for l in orig if l.startswith("#")]
    nh = [l for l in lines if l.startswith("#")]
    if oh != nh:
        fail("headings differ from the original")
    # removed lines must be in section 1 or table rows
    o1 = set(next((orig[i:j] for i, j in [(
        next(k for k, l in enumerate(orig) if l.startswith("## 1. ")),
        next(k for k, l in enumerate(orig) if l.startswith("## 2. ")))]), []))
    new = set(lines)
    bad = [l for l in orig if l not in new and l not in o1 and not l.startswith("|")]
    if bad:
        fail("removed lines outside section 1 and tables: " + "; ".join(b[:50] for b in bad[:3]))
    ch = subprocess.run(["git", "diff", "--name-only", "HEAD", "--", "docs/"], capture_output=True, text=True).stdout.split()
    extra = [f for f in ch if f != path]
    if extra:
        fail("other docs changed: " + ", ".join(extra))
    print("PASS T-4")

else:
    print("usage: check.sh T-1|T-2|T-3|T-4")
    sys.exit(2)
PY
