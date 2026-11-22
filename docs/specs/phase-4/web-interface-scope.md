# Phase 4 Scope — Web Interface

**Source:** `docs/specs/csflite-spec-brief.md` §12, read against §2, §6, §7, §9, §10, §11.
**Full design:** `docs/specs/design/phase-4-web-interface.md` — stack, data model, routes, container, retirement sequence.
**Scope change:** [ADR-0011](../adr/ADR-0011-phase4-ships-container-only.md) — Phase 4 ships the container only. Hosted profiles move to Phase 7.
**Status:** Scoped, not built.

This is a scope summary, not a second contract. Where this document and the spec brief disagree, the spec brief wins.

---

## What Phase 4 is

Replace the CSFLite CLI with a web application. After Phase 4, CSFLite is not operable from a terminal.

Ships as one container image the operator runs themselves. The local `docker compose` profile is the only profile CSFLite ships. An operator may also run the container on a network or in a cloud account they control. CSFLite supports that but ships no template or provisioning for it. The operator owns the infrastructure either way, so organization data never leaves an environment they control. This is what resolves the §7 local-first conflict rather than deferring it (§10).

## In scope

- Web questionnaire replacing the governance checklist CSV, covering the core 25 subcategories only
- Optional per-question evidence upload, alongside the existing evidence prompt — scoring ignores it (§16 of the design doc)
- Web-rendered report and heatmap, plus CSV download matching the §3 output contracts exactly
- Database persistence: assessments, responses, evidence, and an immutable result snapshot per assessment. SQLite at a fixed path under `/data`, evidence files on disk under `/data`
- CSV import for assessments already completed with the CLI
- Container image and a local `docker compose` profile, published on `127.0.0.1` only
- Network runs, operator-deployed: the operator puts a TLS proxy in front, mounts `/data` on a persistent volume, and declares public mode
- Public mode (`CSFLITE_PUBLIC=true`): operator password guard, both startup guards, and HTTPS required (redirect, `Secure` cookies, HSTS)

## Out of scope for Phase 4

- SOC 2 and HIPAA supplement tracks — move to Phase 5, collected and exported but not scored, so the §10 crosswalk decision and §11 boundary don't move
- Multi-user accounts, roles, organizations, tenancy
- Hosted deployment profiles and provisioning — Phase 7 (ADR-0011): the DigitalOcean proof of concept (App Platform, Managed Postgres, Spaces), object storage through `django-storages` and `boto3`, Postgres and `DATABASE_URL`, and the AWS, Azure and GCP profiles
- Hosts with no persistent disk — later releases
- A public or third-party API
- Any JavaScript framework or build step

## What carries over unchanged

- The 25 curated subcategories and `csf_lookup.csv` as their source of truth
- `assess_helpers.py` — unchanged, verified by diff
- The §3 interface contracts — a web form producing the same records satisfies the same contracts

## What is retired

- `governance_check.py`
- `config/path_config.json`, replaced by environment variables where an operator needs to change a value
- §2, the §3 Path Configuration contract, §4, §5, §6, §7, and the §5 boundary rules are rewritten once Phase 4 ships

## Acceptance

- An assessment completes end to end in the browser
- Web output is byte-identical to `tests/fixtures/golden/` for the same responses
- The container starts from `docker compose up` with no host Python
- A past assessment's result does not change when `csf_lookup.csv` is reweighted
- Evidence files are reachable only through the application, never a public URL, and attaching one never changes a score
- With `CSFLITE_PUBLIC=true`, the app refuses to start without `CSFLITE_PASSWORD`, and plain HTTP requests are redirected to HTTPS (except `/healthz`)
