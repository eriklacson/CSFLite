# ADR-0005: Replace the CLI with a Web Application

## Status

Accepted

## Date

2026-08-29

## Context

The CLI requires the assessor to edit a CSV by hand, run Python, and read CSV output. That limits
who can run an assessment and makes the questionnaire hard to complete well.

The scoring core, `tools/assess_helpers.py`, is pure functions with no I/O. It can be called from a
web view without change.

## Decision

Phase 4 replaces the CLI with a server-rendered Django application. The CLI is retired, not kept
alongside it.

`assess_helpers.py` carries over unchanged, verified by diff. Web output must be byte-identical to
the golden recordings in `tests/fixtures/golden/` before the CLI is deleted.

Full design: `docs/specs/design/phase-4-web-interface.md`.

## Consequences

**Positive:**
- One front end to maintain.
- The scoring rules cannot drift, because the same module runs.

**Negative / trade-offs:**
- After Phase 4, CSFLite cannot run from a terminal.
- Known CLI defects that the web app resolves are not fixed in the CLI (for example CHK-0001 #4).

## Alternatives Considered

**Keep the CLI alongside the web app.** Rejected. Two front ends double the maintenance for no
user who needs both.

**Rewrite scoring in the web layer or in JavaScript.** Rejected. It would break parity with the
recorded output and create a second scoring implementation.
