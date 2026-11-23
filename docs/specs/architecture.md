---
doc: architecture
mode: build
system: CSFLite
version: 0.1
date: 2026-10-24
source: docs/specs/design/phase-4-web-interface.md
---

# Architecture — CSFLite

> **Mode.** `build` = this describes what is to be built: the Phase 4 web application, which is not built yet.
> **Status vocabulary.** `CONFIRMED` · `PARTIAL` · `ABSENT` · `UNSPECIFIED` (not yet decided) · `UNVERIFIED` (claimed, not confirmed)
> **Evidence column.** A design section or an ADR.
> **Binding.** No. The spec brief (`docs/specs/csflite-spec-brief.md`) remains the contract-binding document. This records the architecture of work not yet done and cites the design and ADRs it draws from.

---

## 1. Purpose

CSFLite is a self-hosted web application that records whether each of 25 NIST CSF v2.0 controls exists in an organization, for the single operator who does the assessment. It measures coverage, not maturity. Evidence: ADR-0002, ADR-0003, ADR-0005.

---

## 2. System context

**Actors.** One operator. There are no organization logins, no roles and no tenants (design §3, ADR-0007).

**Talks to.**

- Local profile: a SQLite file and the host filesystem, both mounted into the container.
- Network run: the same SQLite file and evidence directory, on a persistent volume the operator mounts, behind the operator's TLS proxy (design §11, ADR-0011).
- Hosted profiles, Phase 7 (ADR-0011): DigitalOcean Managed PostgreSQL and Spaces as a proof of concept, then AWS S3, Azure Blob and Google Cloud Storage.

**Not responsible for.**

- Compliance claims. CSFLite does not claim an organization is compliant.
- Maturity scoring. It scores existence only (ADR-0003).
- Scoring SOC 2 and HIPAA supplements. They are collected, not scored (ADR-0008).
- Hosting organization data. The operator runs the container in their own account (ADR-0006).

---

## 3. Stack

In build mode, CONFIRMED means decided in the design or an ADR, with an exact version. Exact versions are held in `poetry.lock` once the application skeleton exists (AD-11). Package versions were checked on 2026-10-24 against PyPI and npm. Python 3.12.15 comes from search results for python.org and was not checked at the source. PostgreSQL 18, recorded for Phase 7, came from DigitalOcean documentation the same way. One row is UNVERIFIED and one is PARTIAL; see section 8.

| Layer | Component | Version | Status | Evidence |
| --- | --- | --- | --- | --- |
| Language / runtime | Python | 3.12.15 | CONFIRMED | `pyproject.toml`, design §12 |
| Application framework | Django 5.2 LTS, server-rendered, no build step | 5.2.18 | CONFIRMED | design §7, AD-11 |
| Scoring | `tools/assess_helpers.py` on pandas and numpy | pandas 2.3.1, numpy 2.3.2 | CONFIRMED | ADR-0005, `poetry.lock` |
| Data layer / ORM | Django ORM, migrations as a release step | 5.2.18, ships with Django | CONFIRMED | design §7, §12 |
| Database | SQLite at the fixed path `/data/csflite.db`. PostgreSQL through `DATABASE_URL` in Phase 7 (ADR-0011) | SQLite is the build bundled in the Python image. PostgreSQL 18 recorded for Phase 7 | CONFIRMED | design §7, §9 |
| Database driver | `psycopg` with the binary extra, PostgreSQL only. Phase 7 (ADR-0011) | 3.3.6 | CONFIRMED | AD-11. Not in the Phase 4 image |
| File storage | Django `STORAGES` with `FileSystemStorage`. `django-storages` over `boto3` in Phase 7 (ADR-0011) | 5.2.18, built into Django. django-storages 1.14.6 and boto3 1.43.118 recorded for Phase 7 | CONFIRMED | design §7, §8. OI-11 |
| Static files | WhiteNoise | 6.12.0 | CONFIRMED | design §7 |
| Application server | Gunicorn, one worker | 26.2.0 | CONFIRMED | design §4, §7 |
| Interactivity | htmx, only if a page needs it | 2.0.11 | CONFIRMED | design §7 |
| Auth | Django session cookie, one operator password from `CSFLITE_PASSWORD`, public mode only (`CSFLITE_PUBLIC=true`) | 5.2.18, built into Django | CONFIRMED | design §10, ADR-0007 |
| Container | `python:3.12.15-slim`, multi-stage, non-root; Docker Compose locally | 3.12.15 | UNVERIFIED | design §11, §12. Confirm the image tag exists when the image is first built |
| Hosting / deploy target | The operator's own machine (local profile), or a network or cloud account they control (network run, no template). Hosted profiles in Phase 7 (ADR-0011) | Run by the operator | CONFIRMED | ADR-0011 |
| CI | GitHub Actions on Python 3.12: `actions/checkout` v4, `actions/setup-python` v5, Poetry, Black, Ruff, Bandit, pytest | Black 26.3.1, Ruff 0.12.8, Bandit 1.8.6, pytest 9.0.3. Poetry is not pinned | PARTIAL | `AGENTS.md`, `.github/workflows/python-lint.yaml`, `poetry.lock`. See OI-13 |

---

## 4. Runtime topology

There is one application runtime. No edge runtime, no second language, no client-side execution and no HTTP boundary between the web layer and the scoring code. The only trust split is the browser against the server.

| Runtime | What runs there | Trust properties | Status | Evidence |
| --- | --- | --- | --- | --- |
| Gunicorn, one worker, in the container | Django views, forms, upload handling, and `assess_helpers.py` called in-process | Holds every secret, read from the environment. Does all validation and all scoring | CONFIRMED | design §4, §5 |
| Operator's browser | Server-rendered HTML, htmx if adopted | Untrusted. No scoring and no build step run here | CONFIRMED | design §3, §16 |
| Database | SQLite file at `/data/csflite.db`, on the host mount or the operator's persistent volume | State lives outside the process | CONFIRMED | design §4, §7, §9 |
| Evidence store | Filesystem under `CSFLITE_MEDIA_ROOT`, on the same mount as the database | Reached only through the application, never by a public URL | CONFIRMED | design §8 |
| Release command | Database migrations, run explicitly and never on app boot | Runs before traffic, against the same SQLite file under `/data` as the app | CONFIRMED | design §12 |

---

## 5. Trust boundaries

TB-1 differs by profile, and that is the main finding: the local profile has no login, so its boundary is a network setting, not application code. Enforcement location is the field that matters most.

| ID | Boundary | From → To | Enforcement mechanism | Enforcement location | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| TB-1 | Unauthenticated → authenticated | Anyone → operator | Local: no login. The compose file publishes `127.0.0.1` only, and `CSFLITE_ALLOWED_HOSTS` holds loopback names. Public mode: one password, a Django session cookie, and HTTPS required (INV-30) | Local: compose file and Django Host check. Public mode: middleware, for now (OI-2) | PARTIAL | design §10, ADR-0007 |
| TB-2 | Tenant A → tenant B | n/a | n/a. One operator, no tenants | n/a | CONFIRMED | design §3 |
| TB-3 | User role → elevated action | n/a | n/a. No user table, no roles | n/a | CONFIRMED | design §10, ADR-0007 |
| TB-4 | Application → external service | n/a in Phase 4 | n/a. The database and evidence store are local files. Object storage and Postgres credentials arrive in Phase 7 (ADR-0011) | n/a | CONFIRMED | design §9, ADR-0011 |
| TB-5 | Browser → evidence file | Operator → stored file | Download only through an application view, streamed from storage as an attachment. No public URL and no signed URL. WhiteNoise never serves the evidence directory | Route handler (view) | CONFIRMED | design §8, §17 |
| TB-6 | Uploaded file → application | Operator's file → storage | Extension allowlist of nine types, 25 MB cap, random stored filename. The original name stays in the database row only | Form validation | PARTIAL | design §8 |
| TB-7 | Reference data → scoring | `csf_lookup.csv` → scores | Loaded once at boot from the image. A SHA-256 `lookup_digest` is stored with each result. `tests/test_csf_lookup_data.py` validates the file | Application boot and test suite | CONFIRMED | design §8, ADR-0004 |
| TB-8 | Imported CSV → scoring | Operator's CSV → assessment | Form rules, all 25 subcategories present once, then the scoring guards for invalid responses and unknown IDs. A rejected import creates no assessment | Import view, then `generate_governance_assessement()` | CONFIRMED | design §14 |

---

## 6. Data classes

Evidence files are the most sensitive data and the least protected. The application does not encrypt them or scan them. This table holds names and locations only, never values.

| Data class | Location | Sensitivity | At-rest handling | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| Organization responses (Yes, Partial, No) | `Response` model, database | Confidential. Shows an organization's control gaps | Database default. Encryption at rest depends on the operator's host | PARTIAL | design §8, §18 |
| Assessor notes | `Response.notes`, database | Confidential. Free text, so it can hold anything | Same as responses | PARTIAL | design §8 |
| Evidence files | Filesystem under `CSFLITE_MEDIA_ROOT` | Highest. Organization documents and screenshots | Not encrypted by the application, not malware scanned | ABSENT | design §8, §18 |
| Original evidence filenames | `Evidence` row, database | Confidential. Can name the organization | Database default | PARTIAL | design §8 |
| Engagement label | `Assessment.label`, database | Confidential. Identifies the organization | Database default | PARTIAL | design §8 |
| Result snapshots | `Result` model: assessment, heatmap, `lookup_digest` | Confidential. Immutable once written | Database default | CONFIRMED | design §8 |
| Reference data | `csf_lookup.csv` in the image | Not sensitive. Version-controlled | Version control | CONFIRMED | ADR-0004 |
| Operator password | `CSFLITE_PASSWORD`, environment | Secret | Environment only. How it is compared is UNSPECIFIED | UNSPECIFIED | design §9, §10 |
| Django secret key | `CSFLITE_SECRET_KEY`, environment | Secret | Environment only. The app refuses to start without it | CONFIRMED | design §9 |
| Storage credentials | `CSFLITE_S3_*` settings. Phase 7 (ADR-0011) | Secret | Environment only | CONFIRMED | design §11. Roadmap Phase 7 |
| Database credentials | `DATABASE_URL`. Phase 7 (ADR-0011). Phase 4 uses a local SQLite file with no credentials | Secret | Environment only | CONFIRMED | design §9 |

---

## 7. Decisions and rationale

In build mode this section is the contract. A coding agent reads it before changing anything above. Each row points at the ADR that records the full reasoning.

| ID | Decision | Rationale | Status | Evidence |
| --- | --- | --- | --- | --- |
| AD-1 | A web application replaces the CLI | One front end to maintain. The scoring core has no I/O, so the rewrite stays in intake and output | CONFIRMED | ADR-0005 |
| AD-2 | Ship a container image the operator runs. Never a hosted service | Organization data stays in an environment the operator controls | CONFIRMED | ADR-0006 |
| AD-3 | Portable, not elastic: always on, one worker | pandas adds about a second of import time to a cold start, and one operator creates no load | CONFIRMED | ADR-0006, design §4 |
| AD-4 | Moved to Phase 7 by ADR-0011. DigitalOcean App Platform is to be the first hosted profile, as a proof of concept, before AWS, Azure and GCP | Spaces speaks the S3 API, so the storage seam is tested before the big clouds. Railway had no object storage and needed a volume | CONFIRMED | ADR-0006 amendment, ADR-0011 |
| AD-5 | The operator declares public mode. A password is required only then | The bind address says nothing inside a container | CONFIRMED | ADR-0007 |
| AD-6 | `csf_lookup.csv` is the single reference file | Three files had disagreed on display names | CONFIRMED | ADR-0004 |
| AD-7 | Scope is fixed at 25 subcategories. Scoring is coverage only, and severity comes from coverage alone | Measures whether a control exists, not how mature it is | CONFIRMED | ADR-0002, ADR-0003 |
| AD-8 | SOC 2 and HIPAA supplements are collected, not scored, from Phase 5 | Keeps the crosswalk decision and the boundary where they are | CONFIRMED | ADR-0008 |
| AD-9 | Django, server-rendered, no JavaScript framework and no build step | The portability seam this design needs is Django's default | CONFIRMED | design §7 |
| AD-10 | Exports are written by `write_to_csv()` and must match the golden fixtures byte for byte. That match gates deleting the CLI | A different CSV writer can change quoting and line endings | CONFIRMED | design §8, §15 |
| AD-11 | Every dependency is pinned to an exact version. Runtime packages are held in poetry.lock. The container base image is pinned to a patch version. Poetry and the CI tools are pinned, never latest. Django stays on the 5.2 LTS line | A security assessment tool must build the same way twice. 5.2 LTS gets security fixes to April 2028 and changes least before 6.2 LTS arrives in April 2027 | CONFIRMED | This document. Not yet in an ADR |
| AD-12 | The public-mode login is enforced in middleware, for now | Closes OI-2 for now. Reopen it only if it blocks | CONFIRMED | This document, 2026-10-24. Not yet in an ADR |

---

## 8. Open items

Thirteen open gaps, carried forward from sections 3 to 6. OI-1 is resolved by the pins in section 3, and OI-2 is decided for now (AD-12). OI-3 to OI-7 and OI-10 are security-relevant. The Owner column is a placeholder for you to assign. Open items are dealt with just before they block.

| ID | Item | Why unresolved | Owner | Blocks |
| --- | --- | --- | --- | --- |
| OI-1 | RESOLVED 2026-10-24. Versions of Django, PostgreSQL, Gunicorn, WhiteNoise, htmx and `django-storages` (Phase 7, ADR-0011) are now pinned in section 3 | Pinned by AD-11 | Architect | none |
| OI-2 | Where the public-mode login is checked. Decided for now: in middleware (AD-12) | Design §10 says a session cookie but not the enforcement point. Middleware chosen 2026-10-24. Reopen only if it blocks | Architect | TB-1 |
| OI-3 | How the operator password is stored and compared | Design §9 says it comes from the environment, not how it is checked | Architect | TB-1 |
| OI-4 | Session cookie flags `HttpOnly` and `SameSite`, and session lifetime. `Secure` is decided: on in public mode (ADR-0011, INV-30) | Not specified. A password on a network needs them stated | Architect | TB-1, public mode |
| OI-5 | Rate limiting on the login route | Not specified. One password on a network is open to guessing | Architect | TB-1, public mode |
| OI-6 | Upload checks beyond the file extension | The allowlist is by extension only, so a renamed file passes | Architect | TB-6 |
| OI-7 | Evidence is not encrypted at rest by the application and not scanned for malware | Accepted in design §18 as an operator responsibility. Encryption at rest depends on the operator's host | Architect | none |
| OI-8 | No audit trail of who changed a response, or when | Not in the design | Architect | none |
| OI-9 | No backup or restore procedure for the database or the evidence store | Not in the design | Architect | Network runs with real organization data |
| OI-10 | Encryption in transit to PostgreSQL and Spaces is not stated. Narrowed by ADR-0011: Phase 4 has no network database or object storage, so this applies from Phase 7. Browser-to-app transit is decided: HTTPS in public mode (INV-30) | Design §9 gave connection settings but not transport requirements | Architect | Phase 7 |
| OI-11 | `django-storages` 1.14.6 lists Django support only up to 5.1, and its last release was April 2025. Nobody has declared it tested on Django 5.2 | It installs, because it only requires Django 3.2 or later, but that is not a support claim. Needs a smoke test of upload, download and delete against Django 5.2.18 | Architect | Phase 7 (ADR-0011). `django-storages` is not in the Phase 4 image |
| OI-12 | No library is chosen to read `DATABASE_URL`. Moved to Phase 7 by ADR-0011: Phase 4 uses a fixed SQLite path and no `DATABASE_URL` | Django does not parse that setting itself | Architect | Phase 7 |
| OI-13 | CI installs Poetry unpinned and pins GitHub Actions by major tag, not by commit. The lockfile was written by Poetry 2.4.3, and the latest is 2.5.1 | `.github/workflows/python-lint.yaml` runs the Poetry installer with no version | Architect | none |
| OI-14 | Django 5.2 security support ends April 2028 and Python 3.12 ends October 2028. Django 6.2 LTS is due April 2027 | No upgrade plan is recorded | Architect | none |
| OI-15 | pandas is held at 2.3.1 while 2.3.3 and 3.1.0 exist | `assess_helpers.py` must stay unchanged and byte-identical to the golden fixtures. Any bump needs the golden test run again | Architect | none |
