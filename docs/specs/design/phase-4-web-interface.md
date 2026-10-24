# Phase 4 Solution Design — Web Interface

**Status:** Draft — not built
**Supersedes on completion:** spec brief §2, the §3 Path Configuration contract, §4, §5, §6, §7
**Binding:** No. The spec brief (`docs/specs/csflite-spec-brief.md`) is the contract-binding document. This design records intent for work not yet done.

**UX source:** `docs/specs/design/ux/` — a Claude Design prototype and wireframes. The prototype defines the flow and screens in §6. Where it disagrees with the interface contracts, §16 records which one wins.

This document owns only what does not exist yet: stack, data model, configuration, deployment, container, routes, and the retirement sequence. It does not restate the interface contracts, the 25 subcategories, or the scoring rules. Those live in the spec brief and are cited from here.

---

## 1. Purpose

Replace the CSFLite CLI with a containerised web application. After Phase 4 the tool is not operable from a terminal.

The application ships as a container image. The operator runs it on their own machine or in their own cloud account. CSFLite is not offered as a hosted service.

---

## 2. What carries over unchanged

| Carried over | Why it survives |
|---|---|
| The 25 subcategories, `data/csf_lookup.csv` as their single source of truth — weights, recommendations, **and** the questionnaire content (`csf_function`, `csf_subcategory_name`, `question`, `evidence`) | Reference data, not application state. Previously split across `csf_lookup.csv`, the retired `heat_map_lookup.csv`, and `templates/governance_checks_template.csv`, which disagreed with each other on most display names (§8 notes the merge) |
| `tools/assess_helpers.py` | Pure functions over dicts, no I/O, callable from a view |
| `write_to_csv()` in `tools/global_helpers.py` | The export writer. It wrote the golden recordings, so byte-identical parity depends on it (§8). `write_to_json()` also stays. `get_paths()` does not carry over; it is deleted with `config/path_config.json` (§15) |
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
   └──► Rendered report + CSV download
```

There is no HTTP boundary between the web layer and the scoring core, and no service abstraction. The view imports the module.

### Row order is the view's responsibility

`generate_governance_assessement()` does not sort. It returns rows in whatever order the input list arrives in (`assess_helpers.py` — the merge preserves left-frame order). The CLI's order comes entirely from `get_governance_checklist_results()`, which sorts the intake rows descending by `csf_subcategory_id` before scoring. That sort is what the golden fixtures in `tests/fixtures/golden/` encode.

The web view does not call `get_governance_checklist_results()` — it builds the checklist list from `Response` rows in the database. Before calling `generate_governance_assessement()`, the view must order those rows the same way: descending by `csf_subcategory_id`. Skipping this reproduces every score correctly but breaks the byte-identical parity check in §15, because `governance_assessment.csv` and `governance_heatmap.csv` row order would no longer match the recordings. Pinned by `test_generate_governance_assessement_preserves_input_order` in `tests/test_assess_helpers.py`.

### The view supplies the display name

The checklist list the view builds must carry the same four fields the CLI's intake produced: `csf_function`, `csf_subcategory_id`, `csf_subcategory_name`, and `response`. `csf_subcategory_name` is not a column on `Response`. The view takes it from the loaded `csf_lookup.csv`, the same file the questionnaire view renders from (§8).

The name is part of the scored output. `generate_governance_assessement()` selects it from the input list, not from the lookup (`assess_helpers.py:88` merges only `csf_subcategory_id`, `weight`, and `recommendation`). A row without it fails:

```
generate_governance_assessement([{csf_subcategory_id, response, notes}], lookup)
→ KeyError: "['csf_subcategory_name'] not in index"
```

---

## 6. User flow and screens

Source: `docs/specs/design/ux/`. `CSFLite Assessment.dc.html` is the interactive prototype; `Wireframes.dc.html` holds the three structural options that preceded it.

Three steps: **Scope → Questionnaire → Results.**

### Scope

Organisation name and a preview of the path. The preview lists every section with its question count, and the footer gives totals as "N questions · M screens".

Phase 4 ships the baseline track only. The prototype's optional SOC 2 and HIPAA tracks arrive in Phase 5. See §16.

### Questionnaire

Sectioned by CSF Function group, not one question per screen. The header names the track and the section position. Two progress indicators: a bar for answered-of-total, and a clickable segment strip that jumps between sections.

Each question shows the subcategory ID, the subcategory name, the question text, an evidence prompt, the weight, and Yes / Partial / No. An optional file upload sits beside the evidence prompt, and files already attached are listed with download and remove actions. See §8. The footer carries Back, a per-screen answered count, and Next.

### Results

Weighted coverage as a percentage, the weighted-point detail behind it, severity counts, coverage-by-group bars, and a gap heatmap sorted by gap descending then subcategory ID. Exports for `governance_assessment.csv` and `governance_heatmap.csv`. Start over.

### Prototype configuration left open

| Prop | Prototype default | Note |
|---|---|---|
| `oneQuestionPerScreen` | `false` | Grouped screens were chosen over one-at-a-time |
| `showEvidence` | `true` | Evidence prompt visible under each question |
| `supplementWeight` | `1.0` | Not adopted. Supplements are collected, not scored. See §16 |

### Explored and not taken

`Wireframes.dc.html` explored an admin workspace listing multiple organisation engagements, with a "create + send link" flow to a separate organisation-facing questionnaire. The built prototype did not take it and is labelled single tenant.

Phase 4 follows the prototype. The admin/organisation split stays a non-goal under §3, because it needs accounts, invitation links, and a second trust boundary — none of which a single operator assessing their own organisations requires.

---

## 7. Stack

| Concern | Choice | Rationale |
|---|---|---|
| Framework | Django | ORM, migrations, sessions, CSRF, file handling, forms in one dependency |
| Rendering | Server-rendered templates | No build step, no `node_modules` in the image |
| Interactivity | htmx, if needed | One script tag; not adopted until a page needs it |
| Database | SQLite locally, Postgres hosted | Selected by `DATABASE_URL`; no code difference |
| File storage | Django `STORAGES` | `FileSystemStorage` local, `django-storages` against S3-compatible object storage hosted. Selected by `CSFLITE_STORAGE_BACKEND` (§9) |
| Static files | WhiteNoise | Removes the need for a CDN or a second service |
| Server | Gunicorn | Handles SIGTERM correctly, which disposability requires |
| Scoring | `tools/assess_helpers.py` | Unchanged |

Django is chosen because the portability seam this design needs is its default. `DATABASE_URL` and `STORAGES` are the two seams that carry the application from a laptop to DigitalOcean to AWS without an application code change. `DATABASE_URL` is a single setting; storage takes a backend selector and, for object storage, its bucket and credentials (§9). Building the same seam over FastAPI would mean owning it.

---

## 8. Data model

Reference data stays in version-controlled files and is loaded once at boot, from the path in `CSFLITE_CSF_LOOKUP` (§9). It does not move into the database. Spec brief §8 holds: reweighting a subcategory means editing `csf_lookup.csv`, with no code change. Because the file ships in the image (§12) and is read at boot, the edit takes effect on the next image build and restart.

### Reference data source for the questionnaire

The questionnaire view renders `csf_function`, `csf_subcategory_name`, `question`, and `evidence` per subcategory. These now live in `csf_lookup.csv` alongside `weight` and `recommendation` — the same file the scoring functions read.

Before this merge the 25 subcategories were defined redundantly across three files (`csf_lookup.csv`, `heat_map_lookup.csv`, and `templates/governance_checks_template.csv`), and the files disagreed: `csf_lookup.csv`'s display name matched the template on only 3 of 25 rows. Nothing read `heat_map_lookup.csv` or the long-form name in `csf_lookup.csv` — the template's name was the one that actually reached scored output, undocumented. Decided 2026-10-16: collapse to one file. `heat_map_lookup.csv` is retired; its columns added nothing `csf_lookup.csv` didn't already have once merged. The long-form NIST text survives as `csf_outcome`, kept for CSWP 29 traceability but not read by scoring or the questionnaire. `templates/governance_checks_template.csv` is regenerated from the merged file once and then frozen — it is still the CLI's input and the §14 import format, and the CLI has weeks left to live.

`assess_helpers.py` is unaffected: `generate_governance_assessement()` already selects `csf_subcategory_id`, `weight`, and `recommendation` from the lookup explicitly (`assess_helpers.py:88`), so the extra columns are inert to scoring. Golden parity holds unchanged.

Only assessment data is persisted.

| Model | Fields | Notes |
|---|---|---|
| `Assessment` | id, label, created_at, completed_at, status | One engagement |
| `Response` | assessment, csf_subcategory_id, response, notes | 25 rows per assessment |
| `Evidence` | response, file, original_filename, uploaded_at | Zero or more per response |
| `Result` | assessment, generated_at, assessment_json, heatmap_json, lookup_digest | Immutable snapshot |

`Result` exists because scoring is deterministic from responses **and** `csf_lookup.csv`, and that file changes over time. Without a snapshot, reweighting a subcategory would silently rewrite the history of every past assessment. `lookup_digest` records which version of the reference data produced the result. It is a SHA-256 hash of the file's bytes as loaded at boot.

The model covers the core 25 only. Phase 4 adds no track field. Supplement persistence is designed with Phase 5.

`Response.notes` resolves CHK-0001 #4. Spec brief §3 says notes are kept with the assessment record from Phase 4, and are not consumed by scoring or the CSV exports. The web form persists them. The CSV exports carry no `notes` column, so byte-identical parity holds.

### Evidence files

Evidence upload is optional. A response can have zero or more files. The evidence prompt stays on every question, so the assessor still sees what would substantiate a Yes.

**Scoring ignores evidence.** A Yes with no file still scores 1.0. Attaching a file never changes a response. Spec brief §3 says evidence is not consumed by scoring, and the parity gate in §15 depends on that. Applying the "evidence required for Yes" rule stays the assessor's judgement. The upload records what they sighted.

**Accepted files.** An extension allowlist: `pdf`, `png`, `jpg`, `jpeg`, `docx`, `xlsx`, `pptx`, `csv`, `txt`. Everything else is rejected, including HTML, SVG, and archives. HTML and SVG can run script when opened from the application's own origin.

**Size.** 25 MB per file. A rejected file shows a form error, and the section keeps its answers.

**Storage.** Files are written through Django `STORAGES` as `<assessment id>/<random name>.<ext>`. The local profile uses `FileSystemStorage` under `CSFLITE_MEDIA_ROOT`. The hosted profile uses `django-storages` against S3-compatible object storage, selected by `CSFLITE_STORAGE_BACKEND` (§9). No host volume holds organisation data in the hosted profile. The original filename is kept only in the `Evidence` row. It is never used to build a path.

**Serving.** Files download only through an application view, behind the same access control as every other page. The view streams the file with `Content-Disposition: attachment`. There is no public media URL, and WhiteNoise never serves the evidence directory. The view streams from storage rather than redirecting to a storage URL, so this holds for object storage as well as the local filesystem. No object storage URL, signed or otherwise, ever reaches the browser.

**Removal.** Removing a file deletes the stored file as well as the row.

**Exports.** The CSV exports do not include evidence. The spec brief §3 contracts have no evidence column, and adding one would break byte-identical parity.

The exports are written by `write_to_csv()` in `tools/global_helpers.py`, the same function that wrote the golden recordings. It uses `csv.DictWriter` with `QUOTE_MINIMAL` and takes the field names from the first row. A different writer, such as Django's `csv.writer` over an `HttpResponse`, can differ in quoting and line endings, and would fail the parity gate in a way that looks like a scoring bug. `write_to_csv()` writes to a file path, so the export view writes to a temporary file and streams that file back.

---

## 9. Configuration

All configuration comes from the environment. There is no per-environment settings file.

| Variable | Default | Notes |
|---|---|---|
| `CSFLITE_SECRET_KEY` | none | Required. Application refuses to start without it |
| `CSFLITE_PUBLIC` | `false` | Declares this deployment is reachable beyond the operator's own machine. See §10 |
| `CSFLITE_PASSWORD` | none | Required when `CSFLITE_PUBLIC` is `true`. Application refuses to start otherwise |
| `PORT` | `8000` | Not `CSFLITE_`-prefixed — the platform convention DigitalOcean App Platform and similar hosts use. Gunicorn binds `0.0.0.0:$PORT` inside the container; see §10 for why. The local compose file forwards `PORT` into the container and publishes the same number on the host (§11) |
| `DATABASE_URL` | `sqlite:////data/csflite.db` | Absolute path, so the SQLite file lands in `/data` alongside the evidence directory whatever the working directory |
| `CSFLITE_MEDIA_ROOT` | `/data/evidence` | Filesystem storage path. Read only when `CSFLITE_STORAGE_BACKEND` is `filesystem` |
| `CSFLITE_STORAGE_BACKEND` | `filesystem` | `filesystem` or `s3`. Selects the Django `STORAGES` backend (§7) |
| `CSFLITE_S3_BUCKET` | none | Required when the backend is `s3` |
| `CSFLITE_S3_ENDPOINT` | none | S3-compatible endpoint. Set for DigitalOcean Spaces; left unset for AWS S3 |
| `CSFLITE_S3_ACCESS_KEY` | none | Required when the backend is `s3` |
| `CSFLITE_S3_SECRET_KEY` | none | Required when the backend is `s3` |
| `CSFLITE_CSF_LOOKUP` | `/app/data/csf_lookup.csv` | Path to the reference data. The image ships this file (§12). `lookup_digest` (§8) is computed over its bytes |
| `CSFLITE_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Loopback names only. Widening this beyond the loopback defaults requires `CSFLITE_PUBLIC=true`. See §10 |
| `CSFLITE_DEBUG` | off | |

`CSFLITE_BIND` does not exist. An earlier draft of this design used it to toggle loopback vs. public binding, and used that address to decide whether `CSFLITE_PASSWORD` was required. It doesn't work in a container: Docker's published ports reach the container through its internal network namespace, not `127.0.0.1`, so gunicorn must always bind `0.0.0.0:$PORT` inside the container just for `docker compose up` to work at all — including for the local profile. An address the app can only ever see as `0.0.0.0` carries no usable signal about whether traffic is reaching it from the operator's own machine or from the internet. §10 replaces it.

**Storage startup guard.** The application exits with an error when `CSFLITE_STORAGE_BACKEND` is `s3` and any of `CSFLITE_S3_BUCKET`, `CSFLITE_S3_ACCESS_KEY`, or `CSFLITE_S3_SECRET_KEY` is unset. A declared configuration that cannot work is a startup error, not a runtime surprise when the first evidence file is uploaded. This is a configuration guard, not one of the authentication guards in §10, and ADR-0007 does not cover it.

`config/path_config.json` is deleted. It solved path resolution for a CLI reading fixed project paths, which no longer exists. `get_paths()` in `tools/global_helpers.py`, which reads it, is deleted with it (§15).

---

## 10. Authentication

The application cannot tell, from inside the container, whether it is reachable only from the operator's own machine or from the internet. Binding address carries no such signal in a container (§9), and there is no other runtime-observable fact that does — the real control is outside the process, in whatever decides which network traffic reaches the published port. So authentication is not derived from anything the application observes. It is declared by the operator through `CSFLITE_PUBLIC`, and enforced by the deployment profile that ships alongside the declaration.

**Local:** `CSFLITE_PUBLIC` unset (`false`). No login. A login screen adds nothing when the real boundary is Docker's own port publishing, not the application.

**Hosted:** `CSFLITE_PUBLIC=true`, one operator password from `CSFLITE_PASSWORD`, Django session cookie, no user table, no roles, no password reset.

**Startup guards:** the application exits with an error, not a warning, when:

1. `CSFLITE_PUBLIC` is `true` and `CSFLITE_PASSWORD` is unset.
2. `CSFLITE_ALLOWED_HOSTS` is widened beyond the loopback defaults (`localhost`, `127.0.0.1`) and `CSFLITE_PUBLIC` is not `true`.

Guard 1 is a backstop against deploying with `CSFLITE_PUBLIC=true` and forgetting the password. Guard 2 closes the gap guard 1 leaves open: ties widening `ALLOWED_HOSTS` — the one change that lets Django accept requests from anything other than a loopback name — to the same declaration, so a host can't be added to the allowlist without also turning on the password requirement. Neither guard is a substitute for the network-level control below, which the declaration is supposed to match.

**The network-level control, concretely:**

- Local profile: the shipped `docker-compose.yml` publishes the port as `127.0.0.1:${PORT:-8000}:${PORT:-8000}` — bound to the host's loopback only. This, not the application, is what keeps a default local deployment unreachable from the network.
- DigitalOcean profile: App Platform assigns a public domain to every app — there is no loopback-only option. The committed environment template ships with `CSFLITE_ALLOWED_HOSTS` set to that domain and `CSFLITE_PUBLIC=true`, so both the password requirement and the host allowlist are correct from the first deploy.

**Why editing only the port mapping isn't enough.** An operator who edits the local compose file's port mapping to `0.0.0.0:8000:8000`, without touching any environment variable, has made the port reachable from their network — but `CSFLITE_ALLOWED_HOSTS` still holds only the loopback names. Django rejects any request whose `Host` header doesn't match the allowlist with a 400, before the request reaches a view. A request from a LAN or public address arrives with that address as its `Host` header, not a loopback name, and gets rejected. The application still can't detect the edited port mapping — but the mapping alone no longer produces a working, unauthenticated deployment. Making it one requires widening `CSFLITE_ALLOWED_HOSTS`, which guard 2 ties to `CSFLITE_PUBLIC` and `CSFLITE_PASSWORD`. See §18.

---

## 11. Deployment profiles

### Local — Phase 4

Container. `docker compose up`, one service, the host's `./var` directory bind-mounted at `/data` in the container, holding the SQLite file and evidence uploads. `./var`, not `./data`: the repository's `data/` holds the version-controlled `csf_lookup.csv`, and organisation data must not land beside it. `var/` is already in `.gitignore`. Compose rather than a long `docker run` because the volume mount and environment are the part users get wrong.

`ports: ["127.0.0.1:${PORT:-8000}:${PORT:-8000}"]` in the shipped compose file, not `"8000:8000"`. This is the actual enforcement of "local means local" — see §10. `CSFLITE_PUBLIC` is left unset.

The compose file passes `PORT` into the container environment. Gunicorn listens on the same port the host publishes, so setting `PORT=9000` moves both sides together. Left unset, both sides are 8000.

Browse to `http://localhost:$PORT` or `http://127.0.0.1:$PORT` (8000 when `PORT` is unset). Both are in the default `CSFLITE_ALLOWED_HOSTS`. Any other host in the allowlist requires the public profile (§10).

### DigitalOcean — Phase 4, proof of concept

The first hosted profile, and a proof of concept rather than a supported platform. Its job is to prove the container runs unchanged off the operator's laptop, on the same three building blocks AWS, Azure, and GCP use.

Same image. Three managed pieces:

| Piece | Service | Setting |
|---|---|---|
| Compute | App Platform, always-on, one instance | Platform sets `PORT` |
| Database | Managed Postgres | `DATABASE_URL` |
| Evidence files | Spaces, S3-compatible | `CSFLITE_STORAGE_BACKEND=s3` plus the `CSFLITE_S3_*` settings (§9) |

No volume, and no host filesystem holding organisation data. The export view's temporary file (§8) lives on the container's own ephemeral filesystem and does not survive a restart. Spaces speaks the S3 API, so `django-storages` runs the same code path AWS S3 will. This is why DigitalOcean is the proof of concept: the seam that carries the app to the three big clouds is exercised here rather than deferred.

App Platform sets `PORT` itself; gunicorn binds `0.0.0.0:$PORT`, as it does in every profile (§9). The committed environment template sets `CSFLITE_PUBLIC=true`, so the §10 startup guards are live by default and a deploy with no `CSFLITE_PASSWORD` set fails immediately rather than going live unauthenticated.

DigitalOcean has no free tier for this shape. App Platform's free tier covers static sites only, and neither Managed Postgres nor Spaces has one. Checked 2026-10-22 against third-party pricing summaries, not the official pages — confirm current prices before deploying.

### AWS, Azure, GCP — Phase 7

Not designed here. Owned by Phase 7 in `docs/development_roadmap.md`. The commitment Phase 4 makes to keep them cheap: no provider API is called from application code, and nothing branches on which provider it is running on. `DATABASE_URL` points at a managed Postgres, `STORAGES` points at object storage through `django-storages`, and nothing else moves.

This is not a claim that the image carries no cloud SDK. `django-storages` reaches S3-compatible storage through `boto3`, so the Phase 4 image carries it (§12). The commitment is about application code, not dependencies.

What each profile needs on top of the DigitalOcean settings:

| Provider | Storage | Carries over |
|---|---|---|
| AWS | S3 | Directly. Leave `CSFLITE_S3_ENDPOINT` unset |
| GCP | Cloud Storage | Partly. Its S3 compatibility is an interoperability mode needing HMAC keys and `CSFLITE_S3_ENDPOINT` set, or the native `django-storages` GCS backend and its dependency |
| Azure | Blob | No. Blob does not accept the S3 API, so it needs the `django-storages` Azure backend and its dependency |

None of these changes application code. GCP and Azure each add a dependency to the image, so a Phase 7 image is not byte-identical to the Phase 4 one.

---

## 12. Container

- Multi-stage build on `python:3.12-slim`
- Poetry exports to requirements in the build stage; Poetry is absent from the runtime layer
- Runs as a non-root user
- `data/csf_lookup.csv` is copied into the runtime image at `/app/data/csf_lookup.csv`. The local profile does not bind-mount it, so reweighting a subcategory means rebuilding the image. This keeps `lookup_digest` (§8) tied to a file that shipped with a known image
- Gunicorn binds `0.0.0.0:$PORT` unconditionally. Network exposure is controlled entirely by the deployment profile (§10, §11), never by the bind address
- Logs unbuffered to stdout. No log files, no rotation
- `HEALTHCHECK` against `/healthz`
- Migrations run as an explicit release command, never on application boot

- `boto3` ships in the image for the hosted profile's S3-compatible storage (§8). It is a dependency, not provider-specific application code, and it is inert under the local filesystem default

Known cost: pandas and numpy put roughly 100MB in the image. Accepted, because keeping `assess_helpers.py` unchanged is worth more than image size for an always-on single instance.

---

## 13. Routes

Follows the three-step flow in §6. The assessment list has no prototype screen — it exists because persistence does, and the prototype holds all state in the browser.

| Route | Purpose |
|---|---|
| `/` | Assessment list |
| `/assessments/new` | Scope — organisation name |
| `/assessments/<id>/section/<n>` | One CSF Function group per screen. Responses, notes, and evidence uploads post here |
| `/assessments/<id>/results` | Coverage, severity counts, group bars, gap heatmap |
| `/assessments/<id>/export/<artifact>.csv` | `governance_assessment.csv` and `governance_heatmap.csv`, the spec brief §3 output names. Generated server-side by `write_to_csv()` (§8) |
| `/assessments/<id>/evidence/<evidence_id>` | Download one evidence file, as an attachment |
| `/assessments/<id>/evidence/<evidence_id>/delete` | Remove one evidence file (POST) |
| `/assessments/import` | Upload an existing checklist CSV |
| `/login` | Hosted profile only |
| `/healthz` | Liveness |

---

## 14. Migration from CSV

`/assessments/import` accepts the existing governance checklist CSV. It validates it with the same rules the web form enforces: every one of the 25 subcategories present exactly once, and each response present and exactly `Yes`, `Partial`, or `No`, case-sensitive, no synonyms. The scoring guards do not catch a missing or duplicated row, so the import must. It then scores it through `generate_governance_assessement()`, whose guards reject a `csf_subcategory_id` that is not in `csf_lookup.csv`. Only then is it persisted as a completed assessment. Existing organisation work is not stranded.

The web form cannot produce an unknown subcategory ID, but an imported file can. Validating only as the form does would miss it. The unknown-ID check lives in the scoring layer, not in intake.

Rejected input fails the same way it does today: the assessment is not created, and the error names the offending subcategories.

---

## 15. CLI retirement

Ordered so that parity is provable before the CLI is deleted:

1. Build the web application alongside the CLI
2. Extend the golden test to assert web output is byte-identical to `tests/fixtures/golden/`
3. Delete `tools/governance_check.py`, `tests/test_governance_check.py`, and `config/path_config.json`. Delete `get_paths()` from `tools/global_helpers.py` and its `__all__` in the same step, with its two tests (`test_get_paths` in `tests/test_global_helpers.py` and in `tests/test_assess_helpers.py`). `governance_check.py` is its only production caller
4. Rewrite spec brief §2, the §3 Path Configuration contract, §4, §5, §6, §7, and the §5 boundary rules
5. Rewrite `docs/GETTING_STARTED.md`

Step 2 gates step 3. The CLI is not deleted before the web application reproduces its output exactly.

---

## 16. Prototype divergences from the contracts

The prototype is a design artifact. It reimplemented scoring in JavaScript to render without a backend, and that reimplementation drifted from the contracts in several places. These are recorded so the implementation follows the contracts, not the prototype.

### Settled — the contract wins

| Prototype behaviour | Contract | Resolution |
|---|---|---|
| An unanswered question scores as `No` | Blank or invalid input is a hard error (CHK-0001 #1) | The form blocks progress past an unanswered question. Nothing is ever defaulted |
| Severity `low` for a covered control | Spec §3 defines `none` | Use `none` |
| Severity derived from the weighted `assessment_score` | Derived from `score` alone | Equivalent for positive weights, but it diverges at weight 0 and reintroduces the weight coupling CHK-0002 removed |
| Scoring and CSV generation in JavaScript | `assess_helpers.py` is the only scoring implementation | The server generates both exports. No scoring in the browser |
| `assessment.csv` omits `recommendation` | Spec §3 includes it | Add the column |
| No notes field | Spec §3 — notes are kept with the assessment record from Phase 4; not consumed by scoring or the CSV exports (CHK-0001 #4) | The form persists notes per response. The CSV exports carry no `notes` column |

### Decided — 2026-10-16

**Reference data consolidation.** §8 now sources the questionnaire's content from `csf_lookup.csv` rather than leaving it unspecified. The three files that previously defined the 25 subcategories (`csf_lookup.csv`, `heat_map_lookup.csv`, `templates/governance_checks_template.csv`) are collapsed to one, since they disagreed on display names and the design never named which file the questionnaire view should read. Full rationale in §8.

### Decided — 2026-09-13

**Evidence.** The prototype renders evidence as a text prompt under each question, telling the assessor what would substantiate a Yes. It does not accept a file. The roadmap deliverable is evidence upload, and §8 models `Evidence` as an uploaded file.

These are not the same feature, and both are defensible. The prompt is what makes the "evidence required for Yes" rule in spec §10 legible at the moment of answering. The upload is what makes it auditable afterwards. Decision: ship both. The prompt stays, and an optional upload sits beside it. The upload is specified in §8.

**Supplement tracks.** The prototype scores SOC 2 (28 questions) and HIPAA (9 questions) as selectable tracks alongside the core 25, weighting every supplement question at a flat 1.0.

This conflicts with two locked decisions. Spec §10 stores crosswalks as reference documents "not consumed by the scoring engine". Spec §11 assigns readiness assessments to organisation delivery engagements rather than to CSFLite. Scoring the supplements moves both.

It also has no reference data behind it. `csf_lookup.csv` holds weights for the core 25 only, so the flat 1.0 is invented at render time rather than derived, which contradicts spec §8.

Three ways out, in the order I would consider them:

1. **Cut the supplements from Phase 4.** Smallest scope, no locked decision moves, and the core 25 flow is what retires the CLI. The supplements stay CSV templates.
2. **Collect but do not score them.** The tracks appear, answers persist and export, and no weighted coverage is computed for them. Honest about CSFLite not claiming compliance, and it keeps the prototype's flow.
3. **Score them.** Requires weights per supplement question in reference data, and amending spec §10 and §11 first.

Decision: option 1 for Phase 4, and option 2 in Phase 5. The supplements are not what makes the CLI retirable. Option 2 collects answers without scoring them, so spec §10 and §11 do not move.

---

## 17. Acceptance criteria

- An assessment completes end to end in the browser
- Web output is byte-identical to the golden fixtures for the same responses
- `tools/assess_helpers.py` is unchanged, verified by diff
- The view orders `Response` rows descending by `csf_subcategory_id` before calling `generate_governance_assessement()` — see §5
- The view supplies `csf_subcategory_name` from the loaded reference data when it builds the checklist list, not only the row ordering — see §5
- No scoring runs in the browser — exports are generated server-side
- The questionnaire cannot be completed with an unanswered question, and no response is ever defaulted
- The container starts from `docker compose up` with no host Python
- The application refuses to start with `CSFLITE_PUBLIC=true` and no `CSFLITE_PASSWORD`
- The application refuses to start with `CSFLITE_ALLOWED_HOSTS` widened beyond `localhost,127.0.0.1` and `CSFLITE_PUBLIC` not `true`
- The local profile answers on both `http://localhost:$PORT` and `http://127.0.0.1:$PORT`, with `PORT` unset and set to a non-default value
- A request whose `Host` header is not in `CSFLITE_ALLOWED_HOSTS` gets Django's 400, regardless of which address the port is published on
- The shipped local `docker-compose.yml` publishes the port as `127.0.0.1:...`, not `0.0.0.0:...`
- The shipped DigitalOcean environment template sets `CSFLITE_PUBLIC=true` and `CSFLITE_ALLOWED_HOSTS` to the assigned App Platform domain
- The application refuses to start with `CSFLITE_STORAGE_BACKEND=s3` and any required `CSFLITE_S3_*` setting unset
- The hosted profile stores evidence in object storage. No host volume holds organisation data
- A past assessment's result does not change when `csf_lookup.csv` is reweighted
- Evidence files are reachable only through the application download view. None has a public URL
- A file with a disallowed extension or over 25 MB is rejected, and the section keeps its answers
- Attaching or removing evidence changes no score. Golden parity holds with evidence attached
- An import naming an unknown subcategory ID, or missing or repeating one of the 25, is rejected, and no assessment row is left behind

---

## 18. Open risks

| Risk | Handling |
|---|---|
| Docker required on the assessor's laptop | Accepted. One artifact, and running locally exercises the same container, entrypoint, and configuration model as a hosted deploy. Storage differs — see ADR-0006 |
| pandas image size and boot cost | Accepted. Always-on deployment pays it once |
| Object storage credentials are now part of hosted configuration | Accepted. They are environment settings like every other, and the §9 storage guard fails fast when they are incomplete |
| DigitalOcean is a proof of concept, not a supported platform | Stated in §11. Phase 7 adds the AWS, Azure, and GCP profiles. No application code branches on the provider, so each move is a settings change plus, for GCP and Azure, a storage dependency (§11) |
| Evidence files are unencrypted at rest | Depends on the host. An operator responsibility, not solved in the application |
| Evidence files are not scanned for malware | Operator responsibility. The application never opens or renders them, and serves them only as downloads |
| An operator edits the local compose file's port mapping to `0.0.0.0:8000:8000` without setting `CSFLITE_PUBLIC` | Not detectable from inside the container, but not sufficient on its own either (§10): `CSFLITE_ALLOWED_HOSTS` stays at the loopback names, so Django rejects any request whose Host header isn't one of them with a 400. Serving the app to anything else also requires widening `CSFLITE_ALLOWED_HOSTS`, which guard 2 in §10 ties to `CSFLITE_PUBLIC` and `CSFLITE_PASSWORD` |
| An operator browses the local profile by an address that is not a loopback name | Django returns 400. Only `localhost` and `127.0.0.1` work locally. Adding another host trips guard 2 and requires the public profile. Accepted: the local profile is for the operator's own machine |

---

*Last updated: 2026-10-22*
