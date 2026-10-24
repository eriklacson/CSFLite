---
doc: standards-gaps
mode: design
system: CSFLite
version: 0.1
date: 2026-10-24
source: docs/specs/architecture.md v0.1, docs/specs/schema.md v0.1
stack_ref: docs/specs/architecture.md §3
---

# Standards gaps — CSFLite

> **Purpose.** Records where the sources are silent, disagree, or leave an item open. `standards.md` writes no rule for these. Each gap names the standards rows it affects.
> **Status vocabulary.** `CONFIRMED` · `PARTIAL` · `ABSENT` · `UNSPECIFIED` · `UNVERIFIED`
> **Type vocabulary.** `CONFLICT` = two sources disagree. `UNRECORDED` = decided, but not in an ADR. `SILENT` = no source covers it. `UNVERIFIED` = cannot be checked from the repository. `OPEN` = a source already lists it as an open item.
> **Owner.** A placeholder for you to assign, as in `architecture.md` §8.

Same scope as `standards.md`: Phase 4, tenancy excluded. Section numbers in "Affects" refer to `standards.md`.

**Short names.** *arch* = `docs/specs/architecture.md`. *schema* = `docs/specs/schema.md`. *design* = `docs/specs/design/phase-4-web-interface.md`. *brief* = `docs/specs/csflite-spec-brief.md`. *scope* = `docs/specs/phase-4/web-interface-scope.md`.

---

## 1. Conflicts between sources

| ID | Type | Gap | Sources | What `standards.md` does now | Owner | Affects |
|---|---|---|---|---|---|---|
| G-1 | CONFLICT | Tenancy timing. You directed that tenancy is a later phase. ADR-0009 and schema put `organization_id`, composite foreign keys, a seeded Organization row and `current_organization(request)` into the Phase 4 tables. Scope and design §3 say organizations and tenancy are out of Phase 4. `CLAUDE.md` says there are no tenants. arch TB-2 says n/a | ADR-0009. schema §1 to §4, §6. scope "Out of scope". design §3. `CLAUDE.md` "Doc templates". arch §5 TB-2 | Writes no tenancy rules. Data model rules cover Assessment, Response, Evidence and Result only. ADR-0009 and schema need amending, or the direction needs revisiting | Architect | Scope, §2 Data model, INV-12 |
| G-2 | CONFLICT | Evidence storage path. Design: `<assessment id>/<random name>.<ext>`. Schema: `org/<organization_id>/<random>`, with no extension shown. The `org/` prefix is a tenancy feature (G-1) | design §8. schema M-4. ADR-0009 | INV-12 requires only a random name and no original filename. The path prefix and the extension are not decided | Architect | INV-12 |
| G-3 | CONFLICT | The design's data model is stale. Design §8 lists `Evidence.file` and one snapshot per assessment. Schema has `file_key`, UUID keys and many Results per assessment. Scope says "an immutable result snapshot per assessment" | design §8. schema M-4, M-5. scope "In scope" | Follows schema for Result count and field names | Architect | INV-8 |
| G-4 | CONFLICT | Base image tag. Design: `python:3.12-slim`. AD-11 and arch §3: `python:3.12.15-slim`, pinned to a patch | design §12. arch §3, AD-11 | Follows AD-11 | Architect | CO-12 |
| G-5 | CONFLICT | Path configuration while Phase 4 is built. The binding brief says paths resolve through `path_config.json`. Design §9 replaces it with environment variables. Brief §12 says those sections are rewritten only once Phase 4 ships. Until then, new web code that follows design §9 breaks the binding brief | brief §3 Design Rules, §5 Boundary Rules, §12. design §9, §15 | Follows design §9 for web code. The brief rule stays in force for CLI code | Architect | CO-8 |
| G-6 | CONFLICT | Document precedence. Brief §5 and §10 say `docs/assessment_philosophy.md` overrides all other docs. Arch, schema and design say the brief is the binding document. The two claims are not reconciled. `assessment_philosophy.md` was not reviewed for this pass | brief §5, §10. arch header. design header | Treats the brief as binding | Architect | Precedence note |

---

## 2. Decisions without an ADR

| ID | Type | Gap | Sources | What `standards.md` does now | Owner | Affects |
|---|---|---|---|---|---|---|
| G-7 | UNRECORDED | AD-11 (pin every dependency) and AD-12 (hosted login in middleware) are marked "Not yet in an ADR" | arch §7 | Cites arch alone for both | Architect | CO-12, INV-17 |

---

## 3. Silent sources

### Code organization

| ID | Type | Gap | Sources | What `standards.md` does now | Owner | Affects |
|---|---|---|---|---|---|---|
| G-8 | SILENT | Django project and app layout. Where settings, models, views, forms and templates live. Where web tests go once brief §5 is retired. Python naming rules beyond Black and Ruff | brief §5, §12 | CO-2 left UNSPECIFIED | Architect | CO-2, CO-10 |
| G-9 | SILENT | "`assess_helpers.py` unchanged, verified by diff" names no baseline commit or tag | design §17. scope | CO-4 has no reference point | Architect | CO-4 |

### Invariants

| ID | Type | Gap | Sources | What `standards.md` does now | Owner | Affects |
|---|---|---|---|---|---|---|
| G-10 | SILENT | `/healthz` and the hosted login. The container health check targets `/healthz`. The login is checked in middleware. No source says `/healthz` skips the login, or what it checks | design §12, §13. AD-12 | INV-17 exempts only `/login` | Architect | INV-17, INV-26 |
| G-11 | SILENT | Transactions. A rejected import must leave no row. Removing evidence deletes a file and a row. No source says where transactions are used, or what happens when the file delete fails | design §8, §14, §17 | INV-2 and INV-13 state the outcome only | Architect | INV-2, INV-13 |
| G-12 | SILENT | Assessment lifecycle. `status` is `draft`, `in_progress` or `completed`. No rule says when it changes, whether a completed assessment can be edited, or when a new Result is generated | schema M-2, M-5 | No rule | Architect | INV-8 |
| G-13 | SILENT | CSRF. Design picks Django partly for CSRF. No source requires CSRF protection | design §7 | INV-19 is Proposed (not derived) | Architect | INV-19 |
| G-14 | SILENT | Debug mode on a public deployment. `CSFLITE_DEBUG` defaults off. No guard stops it being on with `CSFLITE_PUBLIC=true` | design §9, §10 | INV-20 is Proposed (not derived) | Architect | INV-20, §4 |
| G-15 | SILENT | Secrets in git history. Ruff `S105` to `S107` check source only. Bandit runs at HIGH, which skips its hardcoded-password checks (they are LOW). No history scan exists. Adding one means a tool outside the stated stack | arch §6. `pyproject.toml`. CI workflow | INV-18 is PARTIAL | Architect | INV-18 |
| G-16 | UNVERIFIED | Required merge check. CI runs on every pull request. Whether a branch rule makes it required is a GitHub setting, not visible in the repo | CI workflow | INV-24 is UNVERIFIED | Architect | INV-24 |

### Failure semantics

| ID | Type | Gap | Sources | What `standards.md` does now | Owner | Affects |
|---|---|---|---|---|---|---|
| G-17 | SILENT | No behavior is stated for an unreachable database, failing or slow object storage, or an unhandled exception. No error page rule | — | F-2, F-3, F-4 UNSPECIFIED | Architect | F-2, F-3, F-4 |
| G-18 | SILENT | Bad reference data at boot. `csf_lookup.csv` is checked by the test suite only. No source says what the app does if the file is missing or invalid at boot | arch TB-7. design §8 | F-9 UNSPECIFIED | Architect | F-9, INV-10 |
| G-19 | SILENT | Results with missing rows. The scoring guard catches blank responses, not missing rows. No source says what the results view does with fewer than 25 rows | design §14. schema M-3 | F-11 and INV-7 PARTIAL | Architect | INV-7, F-11 |

### Logging, environments, limits

| ID | Type | Gap | Sources | What `standards.md` does now | Owner | Affects |
|---|---|---|---|---|---|---|
| G-20 | SILENT | Log content and retention. Nothing on secrets or organization data in logs, or how long logs are kept | arch §6 | Two Proposed rules. Retention UNSPECIFIED | Architect | §4 |
| G-21 | SILENT | Environments. The hosted proof of concept is public, but its data class is not stated. arch OI-9 implies real data later. No deploy trigger is stated. No preview or staging environment is defined | design §11. arch OI-9 | §5 rows UNSPECIFIED | Architect | §5 |
| G-22 | SILENT | Limits. No rule for files per response, import CSV size, Django upload memory settings, request timeout, or pagination of `/` | design §8, §13 | §6 rows UNSPECIFIED or PARTIAL | Architect | §6 |

---

## 4. Open items already in the sources

These are recorded in the sources already. They are listed here only for the standards rows they hold open. Tenancy-only items (OI-S1, OI-S2, OI-S4 to OI-S9) are left out.

| Source ID | Item | Affects |
|---|---|---|
| arch OI-3 | How the operator password is stored and compared | INV-17, F-12 |
| arch OI-4 | Session cookie flags and lifetime | INV-17 |
| arch OI-5 | Rate limiting on `/login` | §6, F-12 |
| arch OI-6 | Upload checks beyond the extension | INV-3 |
| arch OI-7 | Evidence not encrypted or scanned by the app. Accepted in design §18 | none |
| arch OI-9 | No backup or restore procedure | §5 production row |
| arch OI-10 | Encryption in transit to PostgreSQL and Spaces not stated | No row. Needs a rule once decided |
| arch OI-11 | `django-storages` not confirmed on Django 5.2 | CO-12, INV-11 |
| arch OI-12 | No library chosen to read `DATABASE_URL` | CO-12 |
| arch OI-13 | Poetry unpinned in CI. Actions pinned by tag, not commit | CO-12 |
| arch OI-14 | Django 5.2 and Python 3.12 support end dates | CO-12 |
| arch OI-15 | pandas held at 2.3.1 | CO-4, INV-9 |
| schema OI-S3 | Weights and recommendations shared, not per organization | none in Phase 4 |

---

## 5. Sources not reviewed

| Source | Why it matters |
|---|---|
| `docs/assessment_philosophy.md` | Claims precedence over all docs (G-6) |
| `.claude/checks/CHK-0001` to `CHK-0004` | Cited by ADR-0003, ADR-0007 and design §16. Their findings were taken as summarized there |
| `docs/specs/design/ux/` | Prototype and wireframes. No engineering rules |

---

## 6. Coverage

| Measure | Count |
|---|---|
| Conflicts | 6 |
| Decisions without an ADR | 1 |
| Silent | 14 |
| Unverified | 1 |
| Source open items referenced | 13 |
| Proposed rules in `standards.md` that rest on a gap | 4 (INV-19, INV-20, two in §4) |
