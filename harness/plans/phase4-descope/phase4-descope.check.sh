#!/usr/bin/env bash
# Check script for plan phase4-descope. Usage: check.sh T-1 ... T-9
# Exit 0 only if the named task's check passes.
set -u
TASK="${1:-}"

python3 -I - "$TASK" <<'PY'
import glob, re, subprocess, sys

task = sys.argv[1]

CUT = re.compile(r"DigitalOcean|App Platform|\bSpaces\b|Managed Postgres|CSFLITE_S3_|"
                 r"CSFLITE_STORAGE_BACKEND|django-storages|boto3|psycopg|DATABASE_URL")
COMMERCIAL = re.compile(r"Lean ?Security")  # the commercial product; jig's `lean-security` ruleset does not match
OK = re.compile(r"Phase 7|ADR-0011")

ADR11_GLOB = "docs/specs/adr/ADR-0011-*.md"
ALLOWED = {
    "docs/specs/adr/README.md",
    "docs/specs/adr/ADR-0006-self-hosted-container-delivery.md",
    "docs/specs/adr/ADR-0007-operator-declared-public-mode.md",
    "docs/specs/phase-4/web-interface-scope.md",
    "docs/specs/design/phase-4-web-interface.md",
    "docs/specs/csflite-spec-brief.md",
    "docs/development_roadmap.md",
    "docs/specs/architecture.md",
    "docs/specs/standards.md",
    "docs/specs/standards-gaps.md",
}


def fail(msg):
    print(f"FAIL {task}: {msg}")
    sys.exit(1)


def read(path):
    try:
        return open(path, encoding="utf-8").read()
    except FileNotFoundError:
        fail(f"{path} not found")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True)


def base():
    r = git("merge-base", "HEAD", "origin/master")
    if r.returncode != 0:
        fail("cannot find merge base with origin/master")
    return r.stdout.strip()


def cut_rule(path):
    """A line naming a moved item must say Phase 7 or ADR-0011, or sit under a heading that does."""
    heading = ""
    bad = []
    for n, line in enumerate(read(path).splitlines(), 1):
        if line.startswith("#"):
            heading = line
        if CUT.search(line) and not OK.search(line) and not OK.search(heading):
            bad.append(f"{path}:{n}: {line.strip()[:80]}")
    if bad:
        fail("moved items named outside Phase 7 context:\n  " + "\n  ".join(bad[:10]))


def section(text, start_pat):
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if re.match(start_pat, l)), None)
    if start is None:
        return ""
    level = len(lines[start]) - len(lines[start].lstrip("#"))
    end = next((i for i in range(start + 1, len(lines))
                if lines[i].startswith("#") and len(lines[i]) - len(lines[i].lstrip("#")) <= level), len(lines))
    return "\n".join(lines[start:end])


def need(text, pat, what):
    if not re.search(pat, text, re.M):
        fail(what)


if task == "T-1":
    files = glob.glob(ADR11_GLOB)
    if len(files) != 1:
        fail(f"expected one file matching {ADR11_GLOB}, found {len(files)}")
    t = read(files[0])
    need(t, r"^# ADR-0011:", "ADR-0011 has no title line")
    need(section(t, r"## Status"), r"^Accepted\s*$", "ADR-0011 status is not Accepted")
    need(section(t, r"## Date"), r"^\d{4}-\d{2}-\d{2}\s*$", "ADR-0011 has no date")
    for h in ("## Context", "## Decision", "## Consequences", "## Alternatives Considered"):
        need(t, "^" + re.escape(h), f"ADR-0011 missing {h}")
    need(section(t, r"## Decision"), r"Phase 7", "ADR-0011 decision does not name Phase 7")
    if re.search(r"(?i)starts when", t):
        fail("ADR-0011 records a Phase 7 start condition; it must not")
    need(section(t, r"## Decision"), r"CSFLITE_PUBLIC", "ADR-0011 does not keep public mode")
    need(section(t, r"## Decision"), r"HTTPS", "ADR-0011 does not require HTTPS in public mode")
    need(section(t, r"## Decision"), r"HSTS", "ADR-0011 does not name HSTS")
    need(read("docs/specs/adr/README.md"), r"\[0011\]\(ADR-0011-", "ADR index does not list ADR-0011")
    print("PASS T-1")

elif task == "T-2":
    b = base()
    for p in ("docs/specs/adr/ADR-0006-self-hosted-container-delivery.md",
              "docs/specs/adr/ADR-0007-operator-declared-public-mode.md"):
        stat = git("diff", "--numstat", b, "--", p).stdout.split()
        if not stat:
            fail(f"{p} not changed")
        if stat[1] != "0":
            fail(f"{p} has {stat[1]} deleted lines; amendments add text only")
        amend = section(read(p), r"## Amendments")
        if "ADR-0011" not in amend:
            fail(f"{p} has no amendment citing ADR-0011")
    print("PASS T-2")

elif task == "T-3":
    p = "docs/specs/phase-4/web-interface-scope.md"
    cut_rule(p)
    t = read(p)
    need(t, r"ADR-0011", "scope does not cite ADR-0011")
    need(section(t, r"## Out of scope"), r"Phase 7", "out-of-scope list does not name Phase 7")
    need(section(t, r"## In scope"), r"CSFLITE_PUBLIC", "public mode dropped from scope")
    need(section(t, r"## In scope"), r"(?i)network", "network runs not in scope")
    print("PASS T-3")

elif task == "T-4":
    p = "docs/specs/design/phase-4-web-interface.md"
    cut_rule(p)
    t = read(p)
    need(t, r"^### Network run", "§11 has no Network run subsection")
    need(t, r"^### Hosted profiles .*Phase 7", "§11 has no 'Hosted profiles ... Phase 7' subsection")
    need(section(t, r"## 9\."), r"/data/csflite\.db", "§9 does not state the fixed SQLite path")
    if "Storage startup guard" in t:
        fail("storage startup guard still in the design")
    need(t, r"^\| `/login` \|.*CSFLITE_PUBLIC", "/login row does not say public mode")
    s17 = section(t, r"## 17\.")
    need(s17, r"CSFLITE_PUBLIC=true` and no `CSFLITE_PASSWORD", "§17 lost the password guard")
    need(s17, r"widened beyond", "§17 lost the allowed-hosts guard")
    s10 = section(t, r"## 10\.")
    for term in ("HTTPS", "HSTS", "Secure", "X-Forwarded-Proto", "/healthz"):
        need(s10, re.escape(term), f"§10 does not cover {term}")
    need(s17, r"(?i)redirect.*HTTPS", "§17 has no HTTPS redirect criterion")
    need(s17, r"HSTS", "§17 has no HSTS criterion")
    need(section(t, r"## 18\."), r"X-Forwarded-Proto", "§18 does not record the proxy header risk")
    need(section(t, r"## 18\."), r"(?i)persistent volume", "§18 does not record the volume risk")
    need(t, r"ADR-0011", "design does not cite ADR-0011")
    print("PASS T-4")

elif task == "T-5":
    p = "docs/specs/csflite-spec-brief.md"
    cut_rule(p)
    s12 = section(read(p), r"## 12\.")
    need(s12, r"ADR-0011", "brief §12 does not cite ADR-0011")
    need(s12, r"Phase 7", "brief §12 does not name Phase 7")
    print("PASS T-5")

elif task == "T-6":
    p = "docs/development_roadmap.md"
    cut_rule(p)
    t = read(p)
    need(t, r"^\| 7 \| Multi-Cloud Deployment Profiles \|", "Phase 7 renamed in status table; it keeps its name")
    need(t, r"^## ⬚ Phase 5: Release Hardening", "Phase 5 heading changed")
    need(t, r"^## ⬚ Phase 6: Community & Iteration", "Phase 6 heading changed")
    s7 = section(t, r"## ⬚ Phase 7: Multi-Cloud Deployment Profiles")
    if not s7:
        fail("Phase 7 heading changed; it keeps its name")
    need(s7, r"DigitalOcean", "Phase 7 does not hold the DigitalOcean proof of concept")
    if re.search(r"(?i)starts when|start condition|trigger", s7):
        fail("Phase 7 records a start condition; it must not")
    need(s7, r"ADR-0011", "Phase 7 does not cite ADR-0011")
    s4 = section(t, r"## ⬚ Phase 4:")
    need(s4, r"(?i)network", "Phase 4 does not mention network runs")
    print("PASS T-6")

elif task == "T-7":
    p = "docs/specs/architecture.md"
    cut_rule(p)
    t = read(p)
    need(t, r"^\| AD-4 \|.*(Phase 7|ADR-0011)", "AD-4 not moved to Phase 7")
    need(t, r"^\| OI-11 \|.*(Phase 7|ADR-0011)", "OI-11 not moved to Phase 7")
    need(t, r"^\| OI-12 \|.*(Phase 7|ADR-0011)", "OI-12 not moved to Phase 7")
    print("PASS T-7")

elif task == "T-8":
    s, g = "docs/specs/standards.md", "docs/specs/standards-gaps.md"
    cut_rule(s)
    cut_rule(g)
    st, gt = read(s), read(g)
    need(st, r"^\| INV-16 \|.*ADR-0011", "INV-16 not marked deferred")
    need(st, r"^\| F-3 \|.*(Phase 7|ADR-0011)", "F-3 not marked deferred")
    need(st, r"^\| INV-17 \|", "INV-17 removed; public mode stays")
    need(st, r"^\| INV-20 \|", "INV-20 removed; public mode stays")
    need(st, r"^\| network run", "environment matrix has no network run row")
    need(gt, r"^\| G-25 \|.*TLS.*RESOLVED", "G-25 (TLS) not added as resolved")
    need(st, r"^\| INV-30 \|.*HTTPS.*HSTS", "INV-30 (HTTPS in public mode) not added")
    print("PASS T-8")

elif task == "T-9":
    b = base()
    changed = set(git("diff", "--name-only", b, "--", "docs/").stdout.split())
    changed |= set(git("ls-files", "--others", "--exclude-standard", "docs/").stdout.split())
    new_adr = set(glob.glob(ADR11_GLOB))
    extra = sorted(changed - ALLOWED - new_adr)
    if extra:
        fail("files changed outside the plan: " + ", ".join(extra))
    for p in sorted(changed | new_adr):
        try:
            if COMMERCIAL.search(open(p, encoding="utf-8").read()):
                fail(f"{p} names the commercial product")
        except FileNotFoundError:
            pass
    for p in sorted(glob.glob("docs/**/*.md", recursive=True)):
        if p.startswith(("docs/specs/adr/", "docs/specs/checks/")):
            continue
        cut_rule(p)
    print("PASS T-9")

else:
    print("usage: check.sh T-1 ... T-9")
    sys.exit(2)
PY
