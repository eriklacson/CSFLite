# Phase 4 Solution Design — Web Interface

**Status:** Draft — not built
**Supersedes on completion:** spec brief §2, §4, §5, §6, §7
**Binding:** No. The spec brief (`.claude/docs/csflite-spec-brief.md`) is the contract-binding document. This design records intent for work not yet done.

This document owns only what does not exist yet: stack, data model, configuration, deployment, container, routes, and the retirement sequence. It does not restate the interface contracts, the 25 subcategories, or the scoring rules. Those live in the spec brief and are cited from here.

---

## 1. Purpose

Replace the CSFLite CLI with a containerised web application. After Phase 4 the tool is not operable from a terminal.

The application ships as a container image. The operator runs it on their own machine or in their own cloud account. CSFLite is not offered as a hosted service.

---

## 2. What carries over unchanged

| Carried over | Why it survives |
|---|---|
| The 25 subcategories, `data/csf_lookup.csv` as their source of truth | Reference data, not application state |
| `tools/assess_helpers.py` | Pure functions over dicts, no I/O, callable from a view |
| The output contracts in spec brief §3 | A form producing the same records satisfies the same contracts |
| Golden fixtures in `tests/fixtures/golden/` | Become the parity gate between CLI and web output |

The scoring layer is not rewritten, re-implemented, or wrapped in a service. A view builds the same list of dicts the CLI built and calls the same function.

---

## 3. Non-goals

Explicitly not built in Phase 4:

- Multi-user accounts, roles, organisations, tenancy
- A public or third-party API
- Background jobs, task queues, Redis, Celery
- Horizontal scaling, autoscaling, scale-to-zero
- A JavaScript framework or any build step
- AWS, Azure, or GCP deployment profiles

---

## 4. What "cloud-native" means here

It means portable and operable. It does not mean elastic.

**Adopted:** config from environment, state outside the process, logs to stdout, disposable containers, health endpoint, migrations as an explicit release step, no provider-specific code.

**Deliberately rejected:** scale-to-zero and autoscaling. pandas costs roughly a second of import time, which a cold start pays on every request. The application runs always-on with a single worker process. There is no load to scale for — one operator, a 25-question form.

This is recorded so that a later contributor does not "fix" the application into a serverless deployment and regress its latency.

---

## 5. Architecture

The three layers in spec brief §2 survive. Only intake and output change.

```
Browser
   │
   ▼
Django view  ── intake: form validation, evidence upload
   │
   ▼
assess_helpers  ── scoring: unchanged, in-process call
   │
   ├──► Result snapshot (database)
   └──► Rendered report + CSV/JSON download
```

There is no HTTP boundary between the web layer and the scoring core, and no service abstraction. The view imports the module.

---

## 6. Stack

| Concern | Choice | Rationale |
|---|---|---|
| Framework | Django | ORM, migrations, sessions, CSRF, file handling, forms in one dependency |
| Rendering | Server-rendered templates | No build step, no `node_modules` in the image |
| Interactivity | htmx, if needed | One script tag; not adopted until a page needs it |
| Database | SQLite locally, Postgres hosted | Selected by `DATABASE_URL`; no code difference |
| File storage | Django `STORAGES` | `FileSystemStorage` local, `django-storages` in cloud; one setting |
| Static files | WhiteNoise | Removes the need for a CDN or a second service |
| Server | Gunicorn | Handles SIGTERM correctly, which disposability requires |
| Scoring | `tools/assess_helpers.py` | Unchanged |

Django is chosen because the portability seam this design needs is its default. `DATABASE_URL` and `STORAGES` are the two switches that carry the application from a laptop to Railway to AWS without a code change. Building the same seam over FastAPI would mean owning it.

---

## 7. Data model

Reference data stays in version-controlled files and is loaded at boot. It does not move into the database. Spec brief §8 holds: reweighting a subcategory means editing `csf_lookup.csv`, nothing more.

Only assessment data is persisted.

| Model | Fields | Notes |
|---|---|---|
| `Assessment` | id, label, created_at, completed_at, status | One engagement |
| `Response` | assessment, csf_subcategory_id, response, notes | 25 rows per assessment |
| `Evidence` | response, file, original_filename, uploaded_at | Zero or more per response |
| `Result` | assessment, generated_at, assessment_json, heatmap_json, lookup_digest | Immutable snapshot |

`Result` exists because scoring is deterministic from responses **and** `csf_lookup.csv`, and that file changes over time. Without a snapshot, reweighting a subcategory would silently rewrite the history of every past assessment. `lookup_digest` records which version of the reference data produced the result.

`Response.notes` resolves CHK-0001 #4. The spec says notes are preserved in output; the CLI's four-column projection dropped them. The web form persists them.

---

## 8. Configuration

All configuration comes from the environment. There is no per-environment settings file.

| Variable | Default | Notes |
|---|---|---|
| `CSFLITE_SECRET_KEY` | none | Required. Application refuses to start without it |
| `CSFLITE_PASSWORD` | none | Required to bind anything other than loopback |
| `CSFLITE_BIND` | `127.0.0.1:8000` | |
| `DATABASE_URL` | `sqlite:///data/csflite.db` | |
| `CSFLITE_MEDIA_ROOT` | `/data/evidence` | Filesystem storage path |
| `CSFLITE_ALLOWED_HOSTS` | `localhost` | |
| `CSFLITE_DEBUG` | off | |

`config/path_config.json` is deleted. It solved path resolution for a CLI reading fixed project paths, which no longer exists.

---

## 9. Authentication

Local: none. The application binds to `127.0.0.1`. A login screen on a loopback interface protects nothing.

Hosted: one operator password from `CSFLITE_PASSWORD`, Django session cookie, no user table, no roles, no password reset.

**Startup guard:** if `CSFLITE_BIND` is not loopback and `CSFLITE_PASSWORD` is unset, the application exits with an error. This is the control that prevents accidentally publishing client assessment data. It is a hard failure, not a warning.

---

## 10. Deployment profiles

### Local — Phase 4

Container. `docker compose up`, one service, a bind-mounted `./data` directory holding the SQLite file and evidence uploads. Compose rather than a long `docker run` because the volume mount and environment are the part users get wrong.

### Railway — Phase 4

Same image. A Postgres addon supplies `DATABASE_URL`. A Railway volume mounted at `/data` holds evidence files. Always-on, one instance.

The volume is the single deliberate deviation from statelessness. It is accepted because Railway offers no object storage, and the alternative is adding an external provider before it is needed. The trigger for removing it is the move off Railway.

### AWS, Azure, GCP — later phases

Not designed here. The commitment Phase 4 makes to keep them cheap: no cloud SDK, no provider API, no provider-specific code. `DATABASE_URL` points at a managed Postgres, `STORAGES` points at object storage through `django-storages`, and nothing else moves.

---

## 11. Container

- Multi-stage build on `python:3.12-slim`
- Poetry exports to requirements in the build stage; Poetry is absent from the runtime layer
- Runs as a non-root user
- Logs unbuffered to stdout. No log files, no rotation
- `HEALTHCHECK` against `/healthz`
- Migrations run as an explicit release command, never on application boot

Known cost: pandas and numpy put roughly 100MB in the image. Accepted, because keeping `assess_helpers.py` unchanged is worth more than image size for an always-on single instance.

---

## 12. Routes

| Route | Purpose |
|---|---|
| `/` | Assessment list |
| `/assessments/new` | Create |
| `/assessments/<id>/questionnaire` | The 25 questions, evidence upload, notes |
| `/assessments/<id>/report` | Rendered report and heatmap |
| `/assessments/<id>/export/<format>` | CSV and JSON download |
| `/assessments/import` | Upload an existing checklist CSV |
| `/login` | Hosted profile only |
| `/healthz` | Liveness |

---

## 13. Migration from CSV

`/assessments/import` accepts the existing governance checklist CSV, runs it through the same validation the web form uses, and persists it as a completed assessment. Existing client work is not stranded.

Rejected input fails the same way it does today: the assessment is not created, and the error names the offending subcategories.

---

## 14. CLI retirement

Ordered so that parity is provable before the CLI is deleted:

1. Build the web application alongside the CLI
2. Extend the golden test to assert web output is byte-identical to `tests/fixtures/golden/`
3. Delete `tools/governance_check.py`, `tests/test_governance_check.py`, and `config/path_config.json`
4. Rewrite spec brief §2, §4, §5, §6, §7, and the §5 boundary rules
5. Rewrite `docs/GETTING_STARTED.md`

Step 2 gates step 3. The CLI is not deleted before the web application reproduces its output exactly.

---

## 15. Acceptance criteria

- An assessment completes end to end in the browser
- Web output is byte-identical to the golden fixtures for the same responses
- `tools/assess_helpers.py` is unchanged, verified by diff
- The container starts from `docker compose up` with no host Python
- The application refuses to start bound to a non-loopback address without `CSFLITE_PASSWORD`
- A past assessment's result does not change when `csf_lookup.csv` is reweighted

---

## 16. Open risks

| Risk | Handling |
|---|---|
| Docker required on the assessor's laptop | Accepted. One artifact, and running locally exercises the deployment path |
| pandas image size and boot cost | Accepted. Always-on deployment pays it once |
| Railway volume is not stateless | Accepted and labelled. Removed on the move to object storage |
| Evidence files are unencrypted at rest | Depends on the host. An operator responsibility, not solved in the application |

---

*Last updated: 2026-08-30*
