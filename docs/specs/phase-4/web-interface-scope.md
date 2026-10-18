# Phase 4 Scope — Web Interface

**Source:** `.claude/docs/csflite-spec-brief.md` §12, read against §2, §6, §7, §9, §10, §11.
**Full design:** `docs/design/phase-4-web-interface.md` — stack, data model, routes, container, retirement sequence.
**Status:** Scoped, not built.

This is a scope summary, not a second contract. Where this document and the spec brief disagree, the spec brief wins.

---

## What Phase 4 is

Replace the CSFLite CLI with a web application. After Phase 4, CSFLite is not operable from a terminal.

Ships as a container image the operator runs themselves — locally first, then on Railway. The operator owns the infrastructure, so client data still never leaves an environment they control. This is what resolves the §7 local-first conflict rather than deferring it (§10).

## In scope

- Web questionnaire replacing the governance checklist CSV, covering the core 25 subcategories only
- Optional per-question evidence upload, alongside the existing evidence prompt — scoring ignores it (§16 of the design doc)
- Web-rendered report and heatmap, plus CSV/JSON download matching the §3 output contracts exactly
- Database persistence: assessments, responses, evidence, and an immutable result snapshot per assessment
- CSV import for assessments already completed with the CLI
- Container image; local `docker compose` profile and a Railway profile
- Operator password guard when bound to a non-loopback address

## Out of scope for Phase 4

- SOC 2 and HIPAA supplement tracks — move to Phase 5, collected and exported but not scored, so the §10 crosswalk decision and §11 boundary don't move
- Multi-user accounts, roles, organizations, tenancy
- AWS, Azure, GCP deployment profiles
- A public or third-party API
- Any JavaScript framework or build step

## What carries over unchanged

- The 25 curated subcategories and `csf_lookup.csv` as their source of truth
- `assess_helpers.py` — unchanged, verified by diff
- The §3 interface contracts — a web form producing the same records satisfies the same contracts

## What is retired

- `governance_check.py`
- `config/path_config.json`, replaced by environment variables
- §2, §4, §5, §6, §7, and the §5 boundary rules are rewritten once Phase 4 ships

## Acceptance

- An assessment completes end to end in the browser
- Web output is byte-identical to `tests/fixtures/golden/` for the same responses
- The container starts from `docker compose up` with no host Python
- A past assessment's result does not change when `csf_lookup.csv` is reweighted
- Evidence files are reachable only through the application, never a public URL, and attaching one never changes a score
