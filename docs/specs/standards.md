---
doc: standards
mode: design
system: CSFLite
version: 0.1
date: 2026-10-24
source: docs/specs/architecture.md v0.1, docs/specs/schema.md v0.1
stack_ref: docs/specs/architecture.md §3
---

# Standards — CSFLite

> **Mode.** `design` = rules to enforce. The Phase 4 web application is not built yet.
> **Status vocabulary.** `CONFIRMED` · `PARTIAL` · `ABSENT` · `UNSPECIFIED` · `UNVERIFIED`
> **Status in this file.** `CONFIRMED` = the sources state the rule and how it is checked. `PARTIAL` = the sources state the rule, but not how it is checked, or part of it is open. `UNSPECIFIED` = the sources say nothing. `UNVERIFIED` = stated, but it cannot be checked from the repository.
> **Install status.** `unbuilt` → `installed` → `proven` (fired on a real regression and held). Only `proven` validates the control.
> **Locus.** `[G]` generator governance · `[P]` pipeline gate · `[R]` assisted remediation. A rule with no locus does not survive regeneration.
> **Strength.** **MUST** = required. A violation fails review. **SHOULD** = expected. A deviation needs a written reason. **MAY** = allowed.
> **Derivation.** Every rule cites its source in Evidence. A rule no source contains is marked **Proposed (not derived)** with a one-line reason. Once the architect approves it, it is marked **Approved (not derived, architect 2026-10-24)** and keeps its reason. A check no source names is marked *mechanism proposed*.
> **Imperative voice.** Invariants are written as rules, not observations.

This file is authoritative for the rules of this system. Rules are stack-dependent, so they are written against the stack recorded in `architecture.md` §3. A rule carried over from another system is re-stated here against this stack or it does not apply.

**Scope.** The Phase 4 web application: Assessment, Response, Evidence and Result, the local profile, and the DigitalOcean proof of concept.

**Out of scope: tenancy.** Tenancy belongs to a later phase (architect direction, 2026-10-24). This file writes no rules for:
- the `organization_id` tenant key and the composite foreign keys that carry it
- `current_organization(request)`
- the Organization model (M-1) and models M-6 to M-10
- the `org/<organization_id>/` evidence path prefix

ADR-0009 and `schema.md` put some of these in the Phase 4 tables. That conflict is G-1.

**Precedence.** The spec brief is the contract-binding document (`architecture.md` header, design header). Scope says the brief wins where the two disagree. The brief itself says `docs/assessment_philosophy.md` wins methodology conflicts. That file was not reviewed (G-6). The sources set no order among the rest. Where they disagree, the rule says which source it follows, and the conflict is recorded in `standards-gaps.md`.

**Short names.** *arch* = `docs/specs/architecture.md`. *schema* = `docs/specs/schema.md`. *design* = `docs/specs/design/phase-4-web-interface.md`. *brief* = `docs/specs/csflite-spec-brief.md`. *scope* = `docs/specs/phase-4/web-interface-scope.md`. *G-n* = a gap in `standards-gaps.md`.

---

## 1. Code organization

How the codebase is arranged. `architecture.md` §3 records what the stack is. This records how it must be laid out.

| ID | Convention | Applies to | Enforcement mechanism | Locus | Install status | Status | Evidence |
|---|---|---|---|---|---|---|---|
| CO-1 | Organization data (the SQLite file and evidence) **MUST** live under the host's `./var`, mounted at `/data`. It **MUST NOT** be written under the repository's `data/` | repo, local profile | The compose file bind-mounts `./var` at `/data`. `.gitignore` keeps `var/` out of git, but does not stop writes to `data/` | [P] | unbuilt | CONFIRMED | design §11 |
| CO-2 | Django project and app layout: where settings, apps, models, views, forms and templates live | repo | none | — | unbuilt | UNSPECIFIED | No source. G-8 |
| CO-3 | Scoring **MUST** live only in `tools/assess_helpers.py`. Views **MUST** import and call it in-process. There **MUST NOT** be an HTTP boundary, a service wrapper, or a second scoring implementation, including in JavaScript | all code | Acceptance test: exports generated server-side, no scoring in the browser | [P] | unbuilt | CONFIRMED | design §2, §5, §16, §17. ADR-0005. AD-1 |
| CO-4 | `tools/assess_helpers.py` **MUST NOT** change during Phase 4 | `tools/assess_helpers.py` | Diff against a baseline. No baseline commit is named | [P] | unbuilt | PARTIAL | design §17. scope "What carries over unchanged". ADR-0005. G-9 |
| CO-5 | Intake validation **MUST** live in the Django form and the import view. The unknown-subcategory check **MUST** stay in the scoring layer, not intake | views, forms | Import acceptance test | [P] | unbuilt | CONFIRMED | design §14, §17. arch TB-8 |
| CO-6 | Before calling `generate_governance_assessement()`, the view **MUST** sort rows descending by `csf_subcategory_id`. It **MUST** take `csf_subcategory_name` from the loaded `csf_lookup.csv` | results and export views | The web golden test. `test_generate_governance_assessement_preserves_input_order` pins the helper only. It cannot fail if the view skips the sort | [P] | unbuilt | CONFIRMED | design §5, §15, §17 |
| CO-7 | Reference data **MUST** be loaded once at boot from `CSFLITE_CSF_LOOKUP`. It **MUST NOT** be stored in the database | settings, boot | *mechanism proposed*: a test that no model holds weights or recommendations | [G] | unbuilt | PARTIAL | design §8. ADR-0004. AD-6 |
| CO-8 | **Approved (not derived, architect 2026-10-24).** Environment variables **MUST** use the `CSFLITE_` prefix. `PORT` and `DATABASE_URL` are the only exceptions | settings | *mechanism proposed*: reviewer check against the design §9 table | [G] | unbuilt | PARTIAL | Reason: every variable in design §9 follows this pattern, but no source states it as a rule. G-5 |
| CO-9 | Export files **MUST** be named `governance_assessment.csv` and `governance_heatmap.csv` | export route | Web golden test | [P] | unbuilt | CONFIRMED | design §13. brief §3 |
| CO-10 | Each `tools/x.py` **MUST** have a matching `tests/test_x.py` | `tools/`, `tests/` | *mechanism proposed*: reviewer check | [G] | unbuilt | PARTIAL | brief §5 Boundary Rules. Rewritten when Phase 4 ships (brief §12). G-8 |
| CO-11 | Code **MUST** pass Black (line length 120), Ruff (`E, F, B, I, S, PT`, `E501` ignored) and Bandit (HIGH severity) | repo | CI workflow and pre-commit hooks | [P] | installed | CONFIRMED | arch §3 CI row. `pyproject.toml`. `.github/workflows/python-lint.yaml` |
| CO-12 | Every runtime package **MUST** be pinned to an exact version in `poetry.lock`. The base image **MUST** be pinned to a patch version (`python:3.12.15-slim`). Poetry and CI tools **MUST** be pinned, never `latest`. Django **MUST** stay on the 5.2 LTS line | `pyproject.toml`, `poetry.lock`, Dockerfile, CI | `poetry.lock`, which is tracked but also listed in `.gitignore`. Pinned pre-commit revisions. Poetry in CI is not pinned | [P] | installed (in part) | PARTIAL | AD-11. arch §3, OI-13. G-4, G-7, G-24 |
| CO-13 | CSV exports **MUST** be written by `write_to_csv()` in `tools/global_helpers.py`. Another CSV writer **MUST NOT** be used | export view | Web golden test | [P] | unbuilt | CONFIRMED | AD-10. design §8 |
| CO-14 | Every schema change **MUST** be a Django migration. Manual schema changes **MUST NOT** happen | migrations | *mechanism proposed*: CI runs `manage.py makemigrations --check` | [P] | unbuilt | PARTIAL | schema §4 |
| CO-15 | `templates/governance_checks_template.csv` **MUST** stay frozen. It changes only by regeneration from `csf_lookup.csv` | `templates/` | `test_lookup_ids_match_the_checklist_template`. It checks IDs only | [P] | installed | PARTIAL | ADR-0004. design §8. Brief §8 says otherwise: G-23 |
| CO-16 | There **MUST NOT** be a JavaScript framework, a build step, a `package.json` or `node_modules`. htmx **MAY** be added as one script tag, only when a page needs it | repo, image | *mechanism proposed*: CI check that no `package.json` exists | [P] | unbuilt | PARTIAL | AD-9. design §3, §7. scope |
| CO-17 | Application code **MUST NOT** call a cloud provider API or branch on the provider. Cloud SDKs are reached only through `django-storages` | application code | *mechanism proposed*: Ruff `TID251` banning `boto3` imports in application code | [P] | unbuilt | PARTIAL | design §4, §11. ADR-0006 |
| CO-18 | There **MUST NOT** be background jobs, task queues, Redis or Celery | dependencies | *mechanism proposed*: reviewer check of `poetry.lock` | [G] | unbuilt | PARTIAL | design §3 |
| CO-19 | Until the CLI is deleted (design §15 step 3), `tools/` modules **MUST NOT** import from `tools/governance_check.py` | `tools/` | *mechanism proposed*: Ruff `TID251` banning that module | [P] | unbuilt | PARTIAL | brief §5 Boundary Rules |

---

## 2. Invariants

Rules the system must not violate. Each needs a mechanism and a locus, or it is a wish.

The template's tenant rows (tenant identity from the session, tenant scoping in the query layer) are left out. Tenancy is a later phase. See Scope.

### Input at the boundary

| ID | Invariant | Scope | Enforcement mechanism | Locus | Install status | Status | Evidence |
|---|---|---|---|---|---|---|---|
| INV-1 | A response **MUST** be exactly `Yes`, `Partial` or `No`. Case-sensitive, no synonyms. The questionnaire **MUST NOT** complete with an unanswered question. A response **MUST NOT** be defaulted | questionnaire, import | `test_generate_governance_assessement_rejects_blank_response`. Form acceptance test | [P] | installed (scoring guard). Form test unbuilt | CONFIRMED | brief §3 Design Rules. design §14, §16, §17 |
| INV-2 | An import **MUST** contain each of the 25 subcategories exactly once. An unknown ID **MUST** be rejected by the scoring guard. A rejected import **MUST** leave no assessment row. Its error **MUST** name the offending subcategories | `/assessments/import` | `test_generate_governance_assessement_rejects_unknown_subcategory`. Import acceptance test | [P] | installed (scoring guard). Import test unbuilt | CONFIRMED | design §14, §17. arch TB-8. G-11 |
| INV-3 | An evidence file **MUST** have one of nine extensions: `pdf`, `png`, `jpg`, `jpeg`, `docx`, `xlsx`, `pptx`, `csv`, `txt`. It **MUST NOT** exceed 25 MB (26,214,400 bytes). A rejected file **MUST** leave the section's answers in place | evidence upload | Upload acceptance test | [P] | unbuilt | PARTIAL | design §8, §17. arch TB-6. schema M-4. Checks beyond the extension are open: OI-6 |
| INV-4 | `Response.csf_subcategory_id` **MUST** be validated against `csf_lookup.csv` by the application | Response | *mechanism proposed*: a model or form test with an unknown ID | [P] | unbuilt | PARTIAL | schema M-3 |

### Scoring and results

| ID | Invariant | Scope | Enforcement mechanism | Locus | Install status | Status | Evidence |
|---|---|---|---|---|---|---|---|
| INV-5 | Weights **MUST** come only from `csf_lookup.csv`. Severity **MUST** come from coverage alone. Gap **MUST** be computed from unformatted `score` and `weight`. Decimal outputs **MUST** be strings with 2 decimal places | scoring | `tests/test_assess_helpers.py` | [P] | installed | CONFIRMED | brief §3 Design Rules. ADR-0003. AD-7 |
| INV-6 | Evidence **MUST NOT** affect scoring. Attaching or removing a file **MUST NOT** change a score or a response | scoring, evidence | Web golden test run with evidence attached | [P] | unbuilt | CONFIRMED | ADR-0003. design §8, §17 |
| INV-7 | A Result **MUST** require all 25 responses answered | Result | Scoring guard for blank responses. Missing rows are not caught by it | [P] | installed (in part) | PARTIAL | schema M-3. design §14. G-19 |
| INV-8 | A `Result` row **MUST NOT** be updated after it is written. It **MUST** store `lookup_digest`, the SHA-256 of `csf_lookup.csv` as loaded at boot. A past result **MUST NOT** change when the lookup is reweighted | Result | Reweighting acceptance test. *mechanism proposed*: model code that refuses an update | [P] | unbuilt | PARTIAL | design §8, §17. schema M-5. arch TB-7. G-3, G-12 |
| INV-9 | Web CSV exports **MUST** be byte-identical to `tests/fixtures/golden/` for the same responses. They **MUST NOT** carry `notes` or evidence columns. This match gates deleting the CLI | export route | `tests/test_golden_pipeline.py` | [P] | installed (CLI only). Web extension unbuilt | CONFIRMED | AD-10. design §8, §15, §17 |
| INV-10 | `data/csf_lookup.csv` **MUST** pass `tests/test_csf_lookup_data.py` | `data/csf_lookup.csv` | `tests/test_csf_lookup_data.py` | [P] | installed | CONFIRMED | arch TB-7. Behavior on a bad file at boot is open: G-18 |
| INV-27 | Every `csf_subcategory_id` in reference data **MUST** be validated against NIST CSWP 29 before it is added | `data/csf_lookup.csv` | `tests/test_csf_lookup_data.py` checks the ID format (`ID_PATTERN`) only, not that the ID exists in CSWP 29 | [P] | installed (in part) | PARTIAL | brief §3 Design Rules |

### Evidence files

| ID | Invariant | Scope | Enforcement mechanism | Locus | Install status | Status | Evidence |
|---|---|---|---|---|---|---|---|
| INV-11 | Evidence **MUST** download only through the application view, streamed with `Content-Disposition: attachment`. There **MUST NOT** be a public media URL, a signed URL, or a redirect to storage. WhiteNoise **MUST NOT** serve the evidence directory | `/assessments/<id>/evidence/<evidence_id>` | Download acceptance test | [P] | unbuilt | CONFIRMED | design §8, §17. arch TB-5 |
| INV-12 | A stored evidence key **MUST** use a random name. The original filename **MUST NOT** appear in the key. It is stored only in `Evidence.original_filename` | evidence storage | *mechanism proposed*: a test on the key format | [P] | unbuilt | PARTIAL | design §8. schema M-4. The two disagree on the rest of the path: G-2 |
| INV-13 | Removing evidence **MUST** be a POST. It **MUST** delete the stored file and the row | `/assessments/<id>/evidence/<evidence_id>/delete` | *mechanism proposed*: a test that the file is gone from storage | [P] | unbuilt | PARTIAL | design §8, §13. schema M-4. G-11 |

### Configuration and access

| ID | Invariant | Scope | Enforcement mechanism | Locus | Install status | Status | Evidence |
|---|---|---|---|---|---|---|---|
| INV-14 | The app **MUST** exit with an error, not a warning, when: (a) `CSFLITE_SECRET_KEY` is unset; (b) `CSFLITE_PUBLIC=true` and `CSFLITE_PASSWORD` is unset; (c) `CSFLITE_ALLOWED_HOSTS` goes beyond `localhost,127.0.0.1` and `CSFLITE_PUBLIC` is not `true`; (d) `CSFLITE_STORAGE_BACKEND=s3` and any of `CSFLITE_S3_BUCKET`, `CSFLITE_S3_ACCESS_KEY`, `CSFLITE_S3_SECRET_KEY` is unset | startup | Startup acceptance tests for (b), (c), (d). *mechanism proposed* for (a): design §17 lists no test | [P] | unbuilt | PARTIAL | design §9, §10, §17. ADR-0007. arch TB-4 |
| INV-15 | The local compose file **MUST** publish the port on `127.0.0.1` only. The local profile **MUST** answer on `localhost` and `127.0.0.1`, with `PORT` unset and set. A request whose `Host` is not in `CSFLITE_ALLOWED_HOSTS` **MUST** get Django's 400 | local profile | Compose, host and port acceptance tests | [P] | unbuilt | CONFIRMED | design §10, §11, §17. ADR-0007. arch TB-1 |
| INV-16 | The DigitalOcean environment template **MUST** set `CSFLITE_PUBLIC=true` and `CSFLITE_ALLOWED_HOSTS` to the App Platform domain | hosted profile | Template acceptance test | [P] | unbuilt | CONFIRMED | design §10, §11, §17. ADR-0007 |
| INV-17 | With `CSFLITE_PUBLIC=true`, every page **MUST** require a signed-in session. Middleware checks it. **Approved (not derived, architect 2026-10-24):** `/login` is the only route exempt | hosted profile | *mechanism proposed*: a test that each design §13 route refuses a request with no session | [P] | unbuilt | PARTIAL | AD-12. design §8 ("the same access control as every other page"), §10. ADR-0007. Reason for the exemption: the login page cannot require a login, and no source lists exemptions. `/healthz` is open: G-10. Password check: OI-3. Cookie flags: OI-4. G-7 |
| INV-18 | Secret values **MUST** come only from the environment: `CSFLITE_SECRET_KEY`, `CSFLITE_PASSWORD`, `CSFLITE_S3_ACCESS_KEY`, `CSFLITE_S3_SECRET_KEY`, `DATABASE_URL`. **Approved (not derived, architect 2026-10-24):** they **MUST NOT** appear in git history | repo | Ruff `S105` to `S107`, through the `S` rule set. Source only. No history scan | [P] | installed (in part) | PARTIAL | arch §6 ("Environment only"). design §9. Reason for the history clause: a secret removed from source stays readable in history. G-15. Tracked as debt: TD-3 in `docs/development_roadmap.md` |
| INV-19 | **Approved (not derived, architect 2026-10-24).** `CsrfViewMiddleware` **MUST** stay enabled for every POST route | all POST routes | *mechanism proposed*: settings test | [P] | unbuilt | PARTIAL | Reason: design §7 picks Django partly for CSRF, but no source requires it, and the hosted profile is public with a session cookie. G-13 |
| INV-20 | **Approved (not derived, architect 2026-10-24).** The app **MUST** refuse to start when `CSFLITE_DEBUG` is on and `CSFLITE_PUBLIC=true` | startup | *mechanism proposed*: startup test | [P] | unbuilt | PARTIAL | Reason: debug pages show settings and stack traces on a public domain, and no source forbids the pairing. G-14 |

### Data model

| ID | Invariant | Scope | Enforcement mechanism | Locus | Install status | Status | Evidence |
|---|---|---|---|---|---|---|---|
| INV-21 | Primary keys **MUST** be UUIDs. Timestamps **MUST** be timezone-aware UTC | Assessment, Response, Evidence, Result | *mechanism proposed*: `USE_TZ = True` and a model test | [P] | unbuilt | PARTIAL | schema §2 |
| INV-22 | Deleting an Assessment **MUST** cascade to its Responses and Results. Deleting a Response **MUST** cascade to its Evidence rows, and the app **MUST** delete the stored files | Assessment, Response, Evidence, Result | *mechanism proposed*: a delete test per relation | [P] | unbuilt | PARTIAL | schema §2 (M-2, M-3, M-4 relations) |
| INV-23 | SQLite foreign key enforcement **MUST** be on | local profile | A test. Schema names it, nobody has written it | [P] | unbuilt | UNVERIFIED | schema §4 |

### Delivery

| ID | Invariant | Scope | Enforcement mechanism | Locus | Install status | Status | Evidence |
|---|---|---|---|---|---|---|---|
| INV-24 | A change **MUST** pass Black, Ruff, Bandit and pytest in CI before merge | pipeline | `.github/workflows/python-lint.yaml` runs on every PR. Whether a branch rule requires it is not visible in the repo | [P] | installed | UNVERIFIED | arch §3 CI row. `CLAUDE.md`. G-16 |
| INV-25 | Migrations **MUST** run as an explicit release command. They **MUST NOT** run on app boot | container, release | *mechanism proposed*: reviewer check that the entrypoint and `AppConfig.ready()` never call `migrate` | [G] | unbuilt | PARTIAL | design §4, §12. schema §4 |
| INV-26 | The container **MUST** be multi-stage, run as a non-root user, and leave Poetry out of the runtime layer. Gunicorn **MUST** bind `0.0.0.0:$PORT` with one worker. `HEALTHCHECK` **MUST** target `/healthz`. Logs **MUST** go unbuffered to stdout | Dockerfile | *mechanism proposed*: reviewer checklist against design §12 | [G] | unbuilt | PARTIAL | design §4, §12. AD-3. arch §3. What `/healthz` checks, and under which `Host`: G-10 |

**Subtraction note.** INV-11 and CO-16 hold partly by absence. There is no media URL route and no `package.json`. A path that does not exist cannot regress. Keep it that way.

---

## 3. Failure semantics

What the system does when something breaks. Per-service failure behavior lives in `integrations.md`, which is not written yet. This is system-level.

| ID | Failure mode | Trigger | Detection | Behavior | User-visible result | Recovery | Status | Evidence |
|---|---|---|---|---|---|---|---|---|
| F-1 | Auth provider unreachable | n/a. Phase 4 has no external auth provider. The password comes from the environment | n/a | n/a | n/a | n/a | CONFIRMED | design §10 |
| F-2 | Database unreachable | | | UNSPECIFIED | | | UNSPECIFIED | No source. G-17 |
| F-3 | Object storage unreachable or slow (hosted) | | | UNSPECIFIED | | | UNSPECIFIED | No source. G-17 |
| F-4 | Unhandled exception in a view | | | UNSPECIFIED | Error page content not stated | | UNSPECIFIED | `CSFLITE_DEBUG` defaults off (design §9). G-17 |
| F-5 | Required setting missing, or settings contradict each other | Startup | Startup guard | fail-closed | Container does not start | Fix the environment and restart | CONFIRMED | design §9, §10. INV-14 |
| F-6 | Unanswered or invalid response | Form submit | Form validation | fail-closed | The form blocks progress. Nothing is defaulted | Answer the question | CONFIRMED | design §16, §17 |
| F-7 | Import fails validation | Import submit | Form rules, then scoring guards | fail-closed | Error names the offending subcategories. No assessment is created | Fix the CSV and import again | CONFIRMED | design §14 |
| F-8 | Evidence rejected (extension or size) | Upload | Form validation | fail-closed for the file | Form error. The section keeps its answers | Choose another file | CONFIRMED | design §8 |
| F-9 | `csf_lookup.csv` missing or invalid at boot | Boot | Test suite only, before build | UNSPECIFIED | | | UNSPECIFIED | arch TB-7. G-18 |
| F-10 | Container restarts during an export | Restart | none | degrade | The temporary export file is lost | Request the export again | CONFIRMED | design §11 |
| F-11 | Results requested with fewer than 25 answers | Results view | Scoring guard catches blanks. It does not catch missing rows (design §14) | fail-closed for blanks. UNSPECIFIED for missing rows | Not stated | | PARTIAL | schema M-3. design §14. G-19 |
| F-12 | Wrong password on `/login` | Login submit | | UNSPECIFIED | | | UNSPECIFIED | OI-3, OI-5 |

**Behavior vocabulary** — `fail-closed` / `fail-open` / `degrade` / `retry` / `queue` / `UNSPECIFIED`.

No security-relevant path is declared fail-open. The local profile has no login by decision (AD-5, ADR-0007). That is not a fail-open path.

---

## 4. Error and logging posture

| Concern | Rule | Enforcement | Status | Evidence |
|---|---|---|---|---|
| Error detail returned to client | A rejected import **MUST** name the offending subcategories. Other error detail is not stated | Import acceptance test | PARTIAL | design §14 |
| Stack traces in responses | `CSFLITE_DEBUG` **MUST** default to off | Settings default | PARTIAL | design §9. Debug on a public deployment: INV-20, G-14 |
| Secrets or tokens in logs | **Approved (not derived, architect 2026-10-24).** Logs **MUST NOT** contain the value of any secret listed in INV-18 | *mechanism proposed*: reviewer check | PARTIAL | Reason: arch §6 lists five secrets, and no rule keeps them out of stdout. G-20 |
| PII in logs | **Approved (not derived, architect 2026-10-24).** Logs **MUST NOT** contain response values, notes, assessment labels, organization names or original filenames | *mechanism proposed*: reviewer check | PARTIAL | Reason: arch §6 rates all of these confidential. G-20 |
| Tenant id in log context | n/a. Tenancy is a later phase | none | n/a | Scope |
| Log destination | Logs **MUST** go unbuffered to stdout. No log files, no rotation | INV-26, which has a proposed mechanism only | PARTIAL | design §4, §12. ADR-0006 |
| Log retention | Not stated. It depends on the operator's platform | none | UNSPECIFIED | G-20 |

---

## 5. Environment matrix

| Environment | Purpose | Data | Auth posture | Publicly reachable | Deploy trigger | Status | Evidence |
|---|---|---|---|---|---|---|---|
| local | The operator runs real assessments on their own machine | production (organization data) | No login. `CSFLITE_PUBLIC` unset | No. Port published on `127.0.0.1` only | The operator runs `docker compose up` | CONFIRMED | design §1, §10, §11. ADR-0007 |
| preview | Not defined | UNSPECIFIED | UNSPECIFIED | UNSPECIFIED | UNSPECIFIED | UNSPECIFIED | No source. G-21 |
| staging | Not defined | UNSPECIFIED | UNSPECIFIED | UNSPECIFIED | UNSPECIFIED | UNSPECIFIED | No source. G-21 |
| production (DigitalOcean proof of concept) | Prove the same container runs off the laptop | UNSPECIFIED | One password and a session. `CSFLITE_PUBLIC=true` | Yes. App Platform assigns a public domain | UNSPECIFIED. Migrations run as a release command | PARTIAL | design §11, §12. ADR-0006. G-21 |
| ci | Lint and tests | synthetic (golden fixtures, inline test data) | n/a | n/a | Every pull request and every push to `master` | CONFIRMED | `.github/workflows/python-lint.yaml`. `CLAUDE.md` |

**Data vocabulary** — `synthetic` / `anonymized` / `production-copy` / `production` / `UNSPECIFIED`.

The hosted proof of concept is publicly reachable, and its data class is not stated. That is the pairing to look for. See G-21.

---

## 6. Rate and resource limits

| Scope | Limit | Enforcement point | Status | Evidence |
|---|---|---|---|---|
| Unauthenticated endpoints | `/login` rate limit not stated | none | UNSPECIFIED | OI-5 |
| Authenticated endpoints | Not stated. One operator | none | UNSPECIFIED | No source |
| Expensive operations | One Gunicorn worker. Request timeout not stated | Gunicorn | PARTIAL | AD-3. design §4. G-22 |
| Upload size | 25 MB per evidence file. Files per response, import CSV size and Django upload memory settings are not stated | Form validation | PARTIAL | design §8. schema M-4. G-22 |
| Query result size / pagination | The assessment list at `/` has no pagination rule | none | UNSPECIFIED | design §13. G-22 |

`routes.md` is not written yet.

---

## 7. Coverage

| Measure | Count |
|---|---|
| Code conventions declared | 18 (17 derived, 1 approved but not derived: CO-8). CO-2 has no rule |
| With a named mechanism | 10 from the sources or the repo. 8 more with a mechanism proposed only |
| Invariants declared | 27 (25 derived, 2 approved but not derived: INV-19, INV-20). INV-17 and INV-18 also carry one approved clause each. 2 logging rules in §4 are approved too. Nothing is left Proposed |
| With a named mechanism | 17 from the sources or the repo. 10 more with a mechanism proposed only |
| With a locus assigned | 27 |
| Install status: installed | 12, most only in part (CO-11, CO-12, CO-15, INV-1, INV-2, INV-5, INV-7, INV-9, INV-10, INV-18, INV-24, INV-27) |
| Install status: proven | 0 |
| Failure modes with defined behavior | 5 of 12 (F-5 to F-8, F-10). F-11 in part. F-1 is n/a. 5 UNSPECIFIED |
| Security-relevant paths failing open | 0 declared. F-12 (login) is UNSPECIFIED |

Counts only. Coverage and sequencing stay on separate axes.

---

## 8. Open items

Recorded in `standards-gaps.md`: conflicts between sources, decisions without an ADR, silent areas, and the open items already listed in `architecture.md` §8 and `schema.md` §6.
