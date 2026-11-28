---
doc: scope
scope: phase4-web-interface
spec_outcomes: []
status: ready for plan
version: 0.2
date: 2026-11-28
---

# Scope phase4-web-interface — Phase 4 Web Interface

> **Source:** `docs/specs/csflite-spec-brief.md` §12, read against §2, §6, §7, §9, §10, §11.
> **Full design:** `docs/specs/design/phase-4-web-interface.md` — stack, data model, routes, container, retirement sequence.
> **Scope change:** [ADR-0011](../adr/ADR-0011-phase4-ships-container-only.md) — Phase 4 ships the container only. Hosted profiles move to Phase 7.
> **Status:** Scoped, not built.
>
> This is a scope summary, not a second contract. Where this document and the spec brief disagree, the spec brief wins.
> It follows `docs/scopes/template.scope.md`. Earlier versions used the headings "In scope", "Out of scope for Phase 4", "What carries over unchanged", "What is retired" and "Acceptance". Their content is now in §3, §4 and §5.

## 1. What this scope delivers

Replace the CSFLite CLI with a web application. After Phase 4, CSFLite is not operable from a terminal.

Ships as one container image the operator runs themselves. The local `docker compose` profile is the only profile CSFLite ships. An operator may also run the container on a network or in a cloud account they control. CSFLite supports that but ships no template or provisioning for it. The operator owns the infrastructure either way, so organization data never leaves an environment they control. This is what resolves the §7 local-first conflict rather than deferring it (§10).

## 2. Rows it covers

Every CO and INV row in `docs/specs/standards.md`, except INV-16 (deferred to Phase 7 by ADR-0011) and CO-2 (no rule yet, G-8). `standards.md` states its scope as the Phase 4 web application.

| Record | Row ID |
|---|---|
| `docs/specs/standards.md` | CO-1 |
| `docs/specs/standards.md` | CO-3 |
| `docs/specs/standards.md` | CO-4 |
| `docs/specs/standards.md` | CO-5 |
| `docs/specs/standards.md` | CO-6 |
| `docs/specs/standards.md` | CO-7 |
| `docs/specs/standards.md` | CO-8 |
| `docs/specs/standards.md` | CO-9 |
| `docs/specs/standards.md` | CO-10 |
| `docs/specs/standards.md` | CO-11 |
| `docs/specs/standards.md` | CO-12 |
| `docs/specs/standards.md` | CO-13 |
| `docs/specs/standards.md` | CO-14 |
| `docs/specs/standards.md` | CO-15 |
| `docs/specs/standards.md` | CO-16 |
| `docs/specs/standards.md` | CO-17 |
| `docs/specs/standards.md` | CO-18 |
| `docs/specs/standards.md` | CO-19 |
| `docs/specs/standards.md` | CO-20 |
| `docs/specs/standards.md` | INV-1 |
| `docs/specs/standards.md` | INV-2 |
| `docs/specs/standards.md` | INV-3 |
| `docs/specs/standards.md` | INV-4 |
| `docs/specs/standards.md` | INV-5 |
| `docs/specs/standards.md` | INV-6 |
| `docs/specs/standards.md` | INV-7 |
| `docs/specs/standards.md` | INV-8 |
| `docs/specs/standards.md` | INV-9 |
| `docs/specs/standards.md` | INV-10 |
| `docs/specs/standards.md` | INV-27 |
| `docs/specs/standards.md` | INV-11 |
| `docs/specs/standards.md` | INV-12 |
| `docs/specs/standards.md` | INV-13 |
| `docs/specs/standards.md` | INV-14 |
| `docs/specs/standards.md` | INV-15 |
| `docs/specs/standards.md` | INV-17 |
| `docs/specs/standards.md` | INV-18 |
| `docs/specs/standards.md` | INV-19 |
| `docs/specs/standards.md` | INV-20 |
| `docs/specs/standards.md` | INV-30 |
| `docs/specs/standards.md` | INV-21 |
| `docs/specs/standards.md` | INV-22 |
| `docs/specs/standards.md` | INV-23 |
| `docs/specs/standards.md` | INV-24 |
| `docs/specs/standards.md` | INV-25 |
| `docs/specs/standards.md` | INV-26 |
| `docs/specs/standards.md` | INV-28 |
| `docs/specs/standards.md` | INV-29 |

## 3. Success criteria

| ID | Criterion | Checked by |
|---|---|---|
| SC-1 | An assessment completes end to end in the browser | Browser acceptance test (design §17). Test path open: G-8 |
| SC-2 | Web output is byte-identical to `tests/fixtures/golden/` for the same responses | INV-9: `tests/test_golden_pipeline.py`, web extension |
| SC-3 | The container starts from `docker compose up` with no host Python | INV-15 and INV-26: compose acceptance test |
| SC-4 | A past assessment's result does not change when `csf_lookup.csv` is reweighted | INV-8: reweighting acceptance test |
| SC-5 | Evidence files are reachable only through the application, never a public URL, and attaching one never changes a score | INV-11: download test. INV-6: golden test with evidence attached |
| SC-6 | With `CSFLITE_PUBLIC=true`, the app refuses to start without `CSFLITE_PASSWORD`, and plain HTTP requests are redirected to HTTPS (except `/healthz`) | INV-14 (b): startup test. INV-30: redirect test |

## 4. Deliverables

| ID | Deliverable | Description |
|---|---|---|
| D-1 | Web questionnaire | Web questionnaire replacing the governance checklist CSV, covering the core 25 subcategories only |
| D-2 | Evidence upload | Optional per-question evidence upload, alongside the existing evidence prompt — scoring ignores it (§16 of the design doc) |
| D-3 | Report and heatmap | Web-rendered report and heatmap, plus CSV download matching the §3 output contracts exactly |
| D-4 | Persistence | Database persistence: assessments, responses, evidence, and an immutable result snapshot per assessment. SQLite at a fixed path under `/data`, evidence files on disk under `/data` |
| D-5 | CSV import | CSV import for assessments already completed with the CLI |
| D-6 | Container and local profile | Container image and a local `docker compose` profile, published on `127.0.0.1` only |
| D-7 | Network runs | Network runs, operator-deployed: the operator puts a TLS proxy in front, mounts `/data` on a persistent volume, and declares public mode |
| D-8 | Public mode | Public mode (`CSFLITE_PUBLIC=true`): operator password guard, both startup guards, and HTTPS required (redirect, `Secure` cookies, HSTS) |
| D-9 | Retire the CLI | Retired: `governance_check.py` |
| D-10 | Retire path config | Retired: `config/path_config.json`, replaced by environment variables where an operator needs to change a value |
| D-11 | Rewrite spec brief sections | Retired: §2, the §3 Path Configuration contract, §4, §5, §6, §7, and the §5 boundary rules are rewritten once Phase 4 ships |

## 5. Not in this scope

| ID | Left out | Why |
|---|---|---|
| NG-1 | SOC 2 and HIPAA supplement tracks — move to Phase 5, collected and exported but not scored, so the §10 crosswalk decision and §11 boundary don't move | Phase 5 |
| NG-2 | Multi-user accounts, roles, organizations, tenancy | Out of scope for Phase 4. Tenancy is a later phase (G-1) |
| NG-3 | Hosted deployment profiles and provisioning — Phase 7 (ADR-0011): the DigitalOcean proof of concept (App Platform, Managed Postgres, Spaces), object storage through `django-storages` and `boto3`, Postgres and `DATABASE_URL`, and the AWS, Azure and GCP profiles | Phase 7 (ADR-0011) |
| NG-4 | Hosts with no persistent disk — later releases | Later releases |
| NG-5 | A public or third-party API | Out of scope for Phase 4 |
| NG-6 | Any JavaScript framework or build step | Out of scope for Phase 4 |
| NG-7 | The 25 curated subcategories and `csf_lookup.csv` as their source of truth | Carries over unchanged |
| NG-8 | `assess_helpers.py` — unchanged, verified by diff | Carries over unchanged |
| NG-9 | The §3 interface contracts — a web form producing the same records satisfies the same contracts | Carries over unchanged |

## 6. Open items

| ID | Item | Why it is still open | What it blocks |
|---|---|---|---|
