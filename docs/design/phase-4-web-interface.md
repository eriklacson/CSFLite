# Phase 4 Solution Design — Web Interface

**Status:** Draft — not built
**Supersedes on completion:** spec brief §2, §4, §5, §6, §7
**Binding:** No. The spec brief (`.claude/docs/csflite-spec-brief.md`) is the contract-binding document. This design records intent for work not yet done.

**UX source:** `docs/design/ux/` — a Claude Design prototype and wireframes. The prototype defines the flow and screens in §6. Where it disagrees with the interface contracts, §16 records which one wins.

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

## 6. User flow and screens

Source: `docs/design/ux/`. `CSFLite Assessment.dc.html` is the interactive prototype; `Wireframes.dc.html` holds the three structural options that preceded it.

Three steps: **Scope → Questionnaire → Results.**

### Scope

Organisation name and a preview of the path. The preview lists every section with its question count, and the footer gives totals as "N questions · M screens".

Phase 4 ships the baseline track only. The prototype's optional SOC 2 and HIPAA tracks arrive in Phase 5. See §16.

### Questionnaire

Sectioned by CSF Function group, not one question per screen. The header names the track and the section position. Two progress indicators: a bar for answered-of-total, and a clickable segment strip that jumps between sections.

Each question shows the subcategory ID, the subcategory name, the question text, an evidence prompt, the weight, and Yes / Partial / No. An optional file upload sits beside the evidence prompt, and files already attached are listed with download and remove actions. See §8. The footer carries Back, a per-screen answered count, and Next.

### Results

Weighted coverage as a percentage, the weighted-point detail behind it, severity counts, coverage-by-group bars, and a gap heatmap sorted by gap descending then subcategory ID. Exports for `assessment.csv` and `heatmap.csv`. Start over.

### Prototype configuration left open

| Prop | Prototype default | Note |
|---|---|---|
| `oneQuestionPerScreen` | `false` | Grouped screens were chosen over one-at-a-time |
| `showEvidence` | `true` | Evidence prompt visible under each question |
| `supplementWeight` | `1.0` | Not adopted. Supplements are collected, not scored. See §16 |

### Explored and not taken

`Wireframes.dc.html` explored an admin workspace listing multiple client engagements, with a "create + send link" flow to a separate client-facing questionnaire. The built prototype did not take it and is labelled single tenant.

Phase 4 follows the prototype. The admin/client split stays a non-goal under §3, because it needs accounts, invitation links, and a second trust boundary — none of which a single operator assessing their own clients requires.

---

## 7. Stack

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

## 8. Data model

Reference data stays in version-controlled files and is loaded at boot. It does not move into the database. Spec brief §8 holds: reweighting a subcategory means editing `csf_lookup.csv`, nothing more.

Only assessment data is persisted.

| Model | Fields | Notes |
|---|---|---|
| `Assessment` | id, label, created_at, completed_at, status | One engagement |
| `Response` | assessment, csf_subcategory_id, response, notes | 25 rows per assessment |
| `Evidence` | response, file, original_filename, uploaded_at | Zero or more per response |
| `Result` | assessment, generated_at, assessment_json, heatmap_json, lookup_digest | Immutable snapshot |

`Result` exists because scoring is deterministic from responses **and** `csf_lookup.csv`, and that file changes over time. Without a snapshot, reweighting a subcategory would silently rewrite the history of every past assessment. `lookup_digest` records which version of the reference data produced the result.

The model covers the core 25 only. Phase 4 adds no track field. Supplement persistence is designed with Phase 5.

`Response.notes` resolves CHK-0001 #4. The spec says notes are preserved in output; the CLI's four-column projection dropped them. The web form persists them.

### Evidence files

Evidence upload is optional. A response can have zero or more files. The evidence prompt stays on every question, so the assessor still sees what would substantiate a Yes.

**Scoring ignores evidence.** A Yes with no file still scores 1.0. Attaching a file never changes a response. Spec brief §3 says evidence is not consumed by scoring, and the parity gate in §15 depends on that. Applying the "evidence required for Yes" rule stays the assessor's judgement. The upload records what they sighted.

**Accepted files.** An extension allowlist: `pdf`, `png`, `jpg`, `jpeg`, `docx`, `xlsx`, `pptx`, `csv`, `txt`. Everything else is rejected, including HTML, SVG, and archives. HTML and SVG can run script when opened from the application's own origin.

**Size.** 25 MB per file. A rejected file shows a form error, and the section keeps its answers.

**Storage.** Files are written through Django `STORAGES` as `<assessment id>/<random name>.<ext>`. The original filename is kept only in the `Evidence` row. It is never used to build a path.

**Serving.** Files download only through an application view, behind the same access control as every other page. The view streams the file with `Content-Disposition: attachment`. There is no public media URL, and WhiteNoise never serves the evidence directory. The view streams from storage rather than redirecting to a storage URL, so this holds when object storage replaces the volume.

**Removal.** Removing a file deletes the stored file as well as the row.

**Exports.** The CSV exports do not include evidence. The spec brief §3 contracts have no evidence column, and adding one would break byte-identical parity.

---

## 9. Configuration

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

## 10. Authentication

Local: none. The application binds to `127.0.0.1`. A login screen on a loopback interface protects nothing.

Hosted: one operator password from `CSFLITE_PASSWORD`, Django session cookie, no user table, no roles, no password reset.

**Startup guard:** if `CSFLITE_BIND` is not loopback and `CSFLITE_PASSWORD` is unset, the application exits with an error. This is the control that prevents accidentally publishing client assessment data. It is a hard failure, not a warning.

---

## 11. Deployment profiles

### Local — Phase 4

Container. `docker compose up`, one service, a bind-mounted `./data` directory holding the SQLite file and evidence uploads. Compose rather than a long `docker run` because the volume mount and environment are the part users get wrong.

### Railway — Phase 4

Same image. A Postgres addon supplies `DATABASE_URL`. A Railway volume mounted at `/data` holds evidence files. Always-on, one instance.

The volume is the single deliberate deviation from statelessness. It is accepted because Railway offers no object storage, and the alternative is adding an external provider before it is needed. The trigger for removing it is the move off Railway.

### AWS, Azure, GCP — later phases

Not designed here. The commitment Phase 4 makes to keep them cheap: no cloud SDK, no provider API, no provider-specific code. `DATABASE_URL` points at a managed Postgres, `STORAGES` points at object storage through `django-storages`, and nothing else moves.

---

## 12. Container

- Multi-stage build on `python:3.12-slim`
- Poetry exports to requirements in the build stage; Poetry is absent from the runtime layer
- Runs as a non-root user
- Logs unbuffered to stdout. No log files, no rotation
- `HEALTHCHECK` against `/healthz`
- Migrations run as an explicit release command, never on application boot

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
| `/assessments/<id>/export/<artifact>.csv` | `assessment.csv` and `heatmap.csv`, generated server-side |
| `/assessments/<id>/evidence/<evidence_id>` | Download one evidence file, as an attachment |
| `/assessments/<id>/evidence/<evidence_id>/delete` | Remove one evidence file (POST) |
| `/assessments/import` | Upload an existing checklist CSV |
| `/login` | Hosted profile only |
| `/healthz` | Liveness |

---

## 14. Migration from CSV

`/assessments/import` accepts the existing governance checklist CSV, runs it through the same validation the web form uses, and persists it as a completed assessment. Existing client work is not stranded.

Rejected input fails the same way it does today: the assessment is not created, and the error names the offending subcategories.

---

## 15. CLI retirement

Ordered so that parity is provable before the CLI is deleted:

1. Build the web application alongside the CLI
2. Extend the golden test to assert web output is byte-identical to `tests/fixtures/golden/`
3. Delete `tools/governance_check.py`, `tests/test_governance_check.py`, and `config/path_config.json`
4. Rewrite spec brief §2, §4, §5, §6, §7, and the §5 boundary rules
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
| No notes field | CHK-0001 #4 — notes are preserved in output | The form persists notes per response |

### Decided — 2026-09-13

**Evidence.** The prototype renders evidence as a text prompt under each question, telling the assessor what would substantiate a Yes. It does not accept a file. The roadmap deliverable is evidence upload, and §8 models `Evidence` as an uploaded file.

These are not the same feature, and both are defensible. The prompt is what makes the "evidence required for Yes" rule in spec §10 legible at the moment of answering. The upload is what makes it auditable afterwards. Decision: ship both. The prompt stays, and an optional upload sits beside it. The upload is specified in §8.

**Supplement tracks.** The prototype scores SOC 2 (28 questions) and HIPAA (9 questions) as selectable tracks alongside the core 25, weighting every supplement question at a flat 1.0.

This conflicts with two locked decisions. Spec §10 stores crosswalks as reference documents "not consumed by the scoring engine". Spec §11 assigns readiness assessments to client delivery engagements rather than to CSFLite. Scoring the supplements moves both.

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
- No scoring runs in the browser — exports are generated server-side
- The questionnaire cannot be completed with an unanswered question, and no response is ever defaulted
- The container starts from `docker compose up` with no host Python
- The application refuses to start bound to a non-loopback address without `CSFLITE_PASSWORD`
- A past assessment's result does not change when `csf_lookup.csv` is reweighted
- Evidence files are reachable only through the application download view. None has a public URL
- A file with a disallowed extension or over 25 MB is rejected, and the section keeps its answers
- Attaching or removing evidence changes no score. Golden parity holds with evidence attached

---

## 18. Open risks

| Risk | Handling |
|---|---|
| Docker required on the assessor's laptop | Accepted. One artifact, and running locally exercises the deployment path |
| pandas image size and boot cost | Accepted. Always-on deployment pays it once |
| Railway volume is not stateless | Accepted and labelled. Removed on the move to object storage |
| Evidence files are unencrypted at rest | Depends on the host. An operator responsibility, not solved in the application |
| Evidence files are not scanned for malware | Operator responsibility. The application never opens or renders them, and serves them only as downloads |

---

*Last updated: 2026-09-13*
