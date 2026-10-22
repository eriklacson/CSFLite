# Plan — Phase 4 Spec Consistency Remediation

**Status:** Applied — W1–W10 done 2026-10-22 (see §7)
**Date:** 2026-10-19
**Baseline:** `master` @ `6e97166` (synced with `origin/master`)
**Branch:** `review/minimax`
**Scope:** `docs/specs/csflite-spec-brief.md`, `docs/specs/phase-4/web-interface-scope.md`,
`docs/specs/design/phase-4-web-interface.md`, `docs/development_roadmap.md`,
`docs/GETTING_STARTED.md`, `templates/soc2-supplement-questionnaire.csv`

---

## 1. Context

A consistency review was run across the spec brief (§1–§12) and the two Phase 4 web interface
specs (the scope summary and the full solution design), cross-checked against the code, the
reference data, the golden fixtures, and the Claude Design prototype.

The first pass ran against a stale branch (`chore/prep-scafold-web-build` @ `cdd8bcc`). Upstream
commits `9280f8e` and `9a91335` ("fix stale paths and factual drift across non-code docs",
"finish the doc consistency pass") landed afterwards and closed four of the fourteen findings,
plus half of one data defect. Everything below was re-verified against `master` @ `6e97166`.

**Verdict:** the substance is consistent. Every locked decision in spec brief §10 traces into the
design, the §3 interface contracts are honoured, and the reference-data merge described in design
§8 is real and complete. What remains is ten documentation defects and one data defect, all
individually small, and all of the same species: a rule stated in one document that the document
next door contradicts or omits.

None of these require a decision. Each has one correct answer that follows from a decision already
locked. The work is editing, not design.

---

## 2. Baseline — verified consistent, do not touch

Recorded so the implementer knows what has already been checked and needs no re-litigation.

| Claim | Verification |
|---|---|
| Design §8: three reference files collapsed into one | `data/csf_lookup.csv` (25 rows) vs `templates/governance_checks_template.csv` vs `tests/fixtures/golden/governance_assessment.csv` — **0 mismatches** on subcategory IDs, `csf_subcategory_name`, `csf_function`, and `weight`. `heat_map_lookup.csv` is gone as stated. |
| Design §5: view must sort rows descending by `csf_subcategory_id` | Correctly derived from the code; pinned by `test_generate_governance_assessement_preserves_input_order` (`tests/test_assess_helpers.py:219`). |
| Design §16: six prototype divergences | **All six verified true** in `docs/specs/design/ux/CSFLite Assessment.dc.html` — unanswered → `"No"` (line 342), `low` for a covered control, severity from the weighted `assessment_score`, JS-only scoring, `recommendation` absent from the export head (line 468), no notes field. |
| Design §16 / §6: prototype shape | Core 25, SOC 2 = 28, HIPAA = 9 — extracted from the prototype, exact match. `oneQuestionPerScreen` false, `showEvidence` true, `supplementWeight` 1.0, "N questions · M screens" footer — all confirmed. |
| Spec §3 severity model | `none` / `medium` / `high` derived from coverage alone; weight enters only via the `gap_score` sort. Matches `score_to_sev()` in `tools/assess_helpers.py` and the CHK-0001 #2 / CHK-0002 resolution. |
| Spec §3 scoring semantics | `Yes=1.0 / Partial=0.5 / No=0.0`; `assessment_score = score × weight`; `gap_score = weight − assessment_score`; 2-decimal string formatting; gap computed from unformatted values. Matches the code. |
| Evidence upload | Scoring ignores evidence, consistently across spec §3, scope doc, design §8, design §17. |
| Supplements | Core 25 only in Phase 4; SOC 2 and HIPAA collected-not-scored in Phase 5. Consistent across spec §12, scope doc, design §16, ADR-0008, roadmap, `CLAUDE.md`. |
| `CSFLITE_BIND` removal | Consistent across design §9/§10/§12/§18, CHK-0004, and ADR-0007. |
| Golden parity gate | `poetry run pytest` → **28 passed** on `master`. `tests/test_golden_pipeline.py` compares serialised bytes, not dicts. |
| Published examples | New `test_published_examples_match_recording` ties `input/examples/` and `output/examples/` to the golden recording. |

---

## 3. Findings register

| ID | Severity | Finding | Where |
|---|---|---|---|
| B1 | High | Display name never reaches the scoring call in the web design | design §5 / §8 |
| B2 | High | `PORT` and the compose container port disagree | design §9 / §11 / §12 |
| B3 | High | `CSFLITE_ALLOWED_HOSTS` default breaks the local profile; guard 2 blocks the fix | design §9 / §10 / §11 |
| B4 | Medium | §3 Path Configuration contract missing from two of three rewrite lists | design §15, scope doc |
| B5 | Medium | JSON download promised in two documents, specified in neither | scope doc, roadmap, design §13 |
| B6 | Medium | Byte-identical export writer never named; `global_helpers.py` orphaned | design §2 / §13 / §15 |
| B7 | Medium | Reference-data path has no configuration | design §8 / §9 |
| B8 | Medium | §14 CSV import points at the wrong validation set | design §14 |
| B9 | Low | Export filenames diverge from the contract and golden names | design §6 / §13 |
| B10 | Low | `DATABASE_URL` and `CSFLITE_MEDIA_ROOT` disagree about where state lives | design §9 / §11 |
| B11 | Low | Design §8 and §16 cite the superseded wording of the `notes` contract | design §8 / §16 |
| C1 | Low | SOC 2 supplement template has ragged rows | `templates/soc2-supplement-questionnaire.csv` |

---

## 4. Work items

Ordered so that each step leaves the tree consistent. W1–W4 are independent and can be done in any
order; W5 depends on nothing; W6–W8 are independent of each other.

### W1 — Amend design §5 to require the display name (B1)

**Problem.** Design §8 defines `Response` as `assessment, csf_subcategory_id, response, notes` — no
name. Design §5 says the view builds the checklist list from `Response` rows and must order them
descending by `csf_subcategory_id`. But `generate_governance_assessement()` reads
`csf_subcategory_name` from the **input frame**, not the lookup — the merge selects only
`csf_subcategory_id`, `weight`, `recommendation` (`tools/assess_helpers.py:88`) — and then selects
the name into the output columns. Verified on `master`:

```
generate_governance_assessement([{csf_subcategory_id, response, notes}], lookup)
→ KeyError: "['csf_subcategory_name'] not in index"
```

§5 mandates the sort and says nothing about the name. This is the same class of defect CHK-0003
found: a contract the view silently misses, which passes §17's acceptance criteria while the
export crashes.

**Fix.** In design §5, extend the requirement so the view supplies both the ordering *and* the
display name, and state where the name comes from. Suggested wording, to sit alongside the existing
paragraph at line 82:

> The checklist list the view builds must carry the same four fields the CLI's intake produced:
> `csf_function`, `csf_subcategory_id`, `csf_subcategory_name`, and `response`.
> `csf_subcategory_name` is not a column on `Response` — the view takes it from the loaded
> `csf_lookup.csv`, the same file the questionnaire view renders from (§8). The name is part of
> the scored output (`generate_governance_assessement()` selects it from the input frame, not from
> the lookup, so a row without it raises `KeyError`).

**Also add to §17 acceptance criteria**, next to the existing row-order criterion at line 356:

> - The view supplies `csf_subcategory_name` from the loaded reference data when it builds the
>   checklist list, not only the row ordering — see §5

**Verification.** The KeyError reproduction above must be cited in the doc, so an implementer
recognises the failure mode. No code changes.

---

### W2 — Reconcile `PORT` with the compose container port (B2)

**Problem.** Three statements that cannot all hold:

- design §9 (line 197): gunicorn "always binds `0.0.0.0:$PORT` inside the container"
- design §12 (line 260): "Gunicorn binds `0.0.0.0:$PORT` unconditionally"
- design §11 (line 239): `ports: ["127.0.0.1:${PORT:-8000}:8000"]` — host side from `$PORT`,
  **container side hardcoded to 8000**

With `PORT=9000`, the host publishes 9000 → container 8000, while gunicorn listens on 9000 inside
the container. Result: connection refused. The design never states whether `PORT` is passed into
the container's environment.

**Fix.** Pick one and make all three agree. The cheaper resolution, recommended: the container port
is fixed and the host port varies.

- §11 becomes `ports: ["127.0.0.1:${PORT:-8000}:8000"]` **with the container port pinned to
  8000**, and the compose file passes no `PORT` into the container environment. `PORT` is then
  documented as a *host-side* publishing port, not a bind port.
- §9 and §12 change "binds `0.0.0.0:$PORT`" → "binds `0.0.0.0:8000` inside the container".

Alternative, if `$PORT` inside the container is wanted (closer to the Railway convention where
Railway sets `PORT` itself): the compose mapping becomes
`"127.0.0.1:${PORT:-8000}:${PORT:-8000}"` and the container environment passes `PORT` through.

**Either way**, add one line to §11 stating whether `PORT` is forwarded into the container. This is
the part that is actually missing, and it is the part that breaks the documented workflow.

**Verification.** Write out both profiles and check the mapping is coherent when `PORT` is unset
and when it is set to a non-default value.

---

### W3 — Fix the local profile's `ALLOWED_HOSTS` behaviour (B3)

**Problem.** Default `CSFLITE_ALLOWED_HOSTS=localhost` (design §9, line 200) and the local compose
publishes `127.0.0.1:8000` (design §11, line 239). Django matches the `Host` header, so
`http://127.0.0.1:8000` returns a 400 — only `http://localhost:8000` works. The obvious operator
fix, `CSFLITE_ALLOWED_HOSTS=localhost,127.0.0.1`, trips startup guard 2 (design §10, line 220)
unless `CSFLITE_PUBLIC=true` and a password are set. So the only way to reach the local profile by
IP is to convert it into the public profile. Django's own default is
`["localhost", "127.0.0.1", "[::1]"]`.

ADR-0007 records the guard as accepted and lists "Django rejects requests whose `Host` is not
`localhost`" as a *positive* consequence. The decision is sound; what is missing is the
operational consequence for the operator.

**Fix.** Recommended: change the default rather than the guard.

- §9 `CSFLITE_ALLOWED_HOSTS` default becomes `localhost,127.0.0.1` — loopback addresses only, so
  it does not weaken the control, and it makes the documented `docker compose up` workflow work
  over both loopback spellings.
- §10 guard 2 rewords from "anything other than its default" to "widened beyond the loopback
  defaults" so the guard still trips on a real network host but not on `127.0.0.1`.
- §11 gains one sentence: browse `http://localhost:8000` or `http://127.0.0.1:8000`; any other
  host in the allowlist requires the public profile.

If the default must stay `localhost`, the alternative is for §11 to publish `localhost:${PORT:-8000}:8000`
and §9 to state that only the `localhost` spelling works locally. This is worse — it is a
surprising footgun in a container the operator runs on their own laptop.

**Also add a row to §18 Open risks** recording the current unstated consequence, whichever
resolution is chosen.

---

### W4 — Complete the retirement lists (B4)

**Problem.** Three lists of the spec sections Phase 4 rewrites. Two of them omit the §3 Path
Configuration contract:

- spec brief line 349: "§2, **the §3 Path Configuration contract**, §4, §5, §6, §7, and the §5
  Boundary Rules" ✅
- design line 4 (header): "§2, **the §3 Path Configuration contract**, §4, §5, §6, §7" ✅
- design line 303 (§15 step 4): "Rewrite spec brief §2, §4, §5, §6, §7, and the §5 boundary rules" ❌
- scope doc line 45: "§2, §4, §5, §6, §7, and the §5 boundary rules" ❌

Commit `d7844be` added it to the header only. The §15 list is the ordered sequence that gates the
CLI deletion, so it is the one that gets worked from. Following it deletes `path_config.json` while
§3 still publishes a contract for a file that no longer exists.

**Fix.** Add "the §3 Path Configuration contract" to design §15 step 4 and to the scope doc's
"What is retired" list, matching the spec brief and the design header verbatim.

**Verification.** All four lists must name the same set.

---

### W5 — Resolve the JSON export promise (B5)

**Problem.** JSON is promised twice and specified nowhere:

- scope doc line 21: "plus CSV/JSON download matching the §3 output contracts exactly"
- roadmap line 94: "Web-rendered report and heatmap, with CSV/JSON download"
- design line 73 (architecture diagram): "Rendered report + CSV/JSON download"

Against that: design §13 lists only `/assessments/<id>/export/<artifact>.csv`; design §8's
"Exports" section discusses CSV only; and spec brief §3 defines **no JSON output contract** — so
"matching the §3 output contracts exactly" is unsatisfiable for JSON as written.

Note `global_helpers.write_to_json()` already exists, so the capability is not the question; the
contract is.

**Fix.** Recommended: drop the JSON promise from Phase 4 and keep the scope tight. CSV parity is
the gate that retires the CLI; a second export format is not needed to prove parity, and adding
one means defining a contract that §3 does not have.

- scope doc line 21 → "plus CSV download matching the §3 output contracts exactly"
- roadmap line 94 → "Web-rendered report and heatmap, with CSV download"
- design line 73 → "Rendered report + CSV download"

If JSON is wanted in Phase 4 instead, the work is larger and belongs in its own item: define a
JSON output contract in spec §3 (field names, ordering, number formatting), add the route to
design §13, and add it to the §17 acceptance criteria. Do not ship the promise without the
contract.

---

### W6 — Name the export writer and retire `global_helpers.py` (B6)

**Problem.** The parity gate is byte-level. `global_helpers.write_to_csv()` — `csv.DictWriter`,
`QUOTE_MINIMAL`, fieldnames taken from row 0 — is what produced the recorded bytes, and
`tests/test_golden_pipeline.py` compares through that function. The design's §2 carries-over table
lists `assess_helpers.py` but not `global_helpers.py`, and nothing tells the implementer to use
`write_to_csv` for the export. A view that renders CSV with Django's `HttpResponse` plus
`csv.writer` will differ in quoting and line terminator from the recording, and the parity gate
will fail looking like a scoring bug.

Separately, design §15 step 3 deletes `config/path_config.json`. `global_helpers.get_paths()`
reads that file and will raise `FileNotFoundError` — and `get_paths()` appears on no retirement
list, leaving the module half-dead.

**Fix.**

- design §2 carries-over table: add a row for `tools/global_helpers.py` — `write_to_csv()` and
  `write_to_json()` carry over unchanged, and `write_to_csv()` **is** the export writer, required
  for byte-identical parity. `get_paths()` does not carry over; it is deleted with
  `config/path_config.json` (§15 step 3).
- design §15: extend step 3 to delete `get_paths()` from `tools/global_helpers.py`. Note that it has
  two call sites in the test suite — `tests/test_global_helpers.py:7` and
  `tests/test_assess_helpers.py:13` — and both tests must be removed or rewritten in the same
  step. `tools/governance_check.py:48` is the only production caller, and that file is deleted in
  the same step, so nothing survives the change. Add a step to point the web app at the reference
  data by path (see W7).
- design §13 (export route) and §8 (Exports): state that the export writes the same bytes the
  CLI wrote, via `write_to_csv()`.

**Verification.** `tools/global_helpers.py` must have no remaining reference to `path_config.json`
after step 3, and `tests/test_global_helpers.py` must still pass.

---

### W7 — Specify the reference-data path (B7)

**Problem.** Design §8 says "Reference data stays in version-controlled files and is loaded at
boot." Design §9's configuration table has no variable for it, and `assess_helpers.get_csf_lookup()`
takes a path argument. The design states neither the path nor that the container image carries
`data/csf_lookup.csv`. This matters more than a missing setting: `lookup_digest` (design §8,
model `Result` at line 160) makes the exact bytes of that file part of the result contract, and
the acceptance criterion "A past assessment's result does not change when `csf_lookup.csv` is
reweighted" depends on it.

**Fix.**

- design §9: add a configuration row, e.g.
  `CSFLITE_CSF_LOOKUP` | `/app/data/csf_lookup.csv` | Path to the reference data. The image ships
  this file; `lookup_digest` (§8) is computed over its bytes.
- design §8: state that the file is loaded once at boot, and that `lookup_digest` is a hash of the
  file's bytes as loaded.
- design §12 (Container): state that `data/csf_lookup.csv` is copied into the runtime image, and
  say whether the local profile bind-mounts it (if it does, an operator can reweight without
  rebuilding; if it does not, reweighting requires a new image — pick one and write it down).

**Verification.** `lookup_digest` must be computable from a path the operator can see.

---

### W8 — Correct §14 to point at the scoring-layer guards (B8)

**Problem.** Design §14 says the import "runs it through the same validation the web form uses."
The web form can only produce the 25 known subcategory IDs — it is a form over `csf_lookup.csv`.
The CLI's unknown-ID guard lives in the **scoring** layer, not in intake:
`generate_governance_assessement()` raises `ValueError("Subcategory not found in CSF lookup: …")`.
§14's own failure clause — "the error names the offending subcategories" — *is* that scoring-layer
error, so the spec points one layer away from where the check actually is. An import path that
validates only as the form does would accept a CSV naming a subcategory that does not exist, and
then fail at scoring time, after the assessment row was already created.

**Fix.** Rewrite §14 to name both validation sets:

> `/assessments/import` accepts the existing governance checklist CSV, validates it with the same
> rules the web form enforces (response present, exactly `Yes`, `Partial`, or `No` — case-sensitive,
> no synonyms), then persists it and scores it through `generate_governance_assessement()`, whose
> guards reject a `csf_subcategory_id` that is not in `csf_lookup.csv`.
>
> Rejected input fails the way it does today: the assessment is not created, and the error names
> the offending subcategories.

Also add to §17: an import naming an unknown subcategory ID is rejected, and no assessment row is
left behind.

**Verification.** The two guards in `tools/assess_helpers.py` (invalid response, unknown
subcategory) are the ones the import path must surface.

---

### W9 — Small consistency fixes (B9, B10, B11)

**B9 — export filenames.** Design §6 (line 106) and §13 (line 279) name the exports
`assessment.csv` and `heatmap.csv`. Spec §3 and `tests/fixtures/golden/` name them
`governance_assessment.csv` and `governance_heatmap.csv`. Harmless for byte parity, which compares
content, but it means the web app's artifacts are not the §3 output names. Either align the design
to `governance_assessment.csv` / `governance_heatmap.csv`, or add a line to §13 noting the web
export filenames differ from the CLI's and why.

**B10 — state location.** Design §9 line 198 gives `DATABASE_URL` a *relative* default
(`sqlite:///data/csflite.db`) while line 199 gives `CSFLITE_MEDIA_ROOT` an *absolute* one
(`/data/evidence`), and §11 bind-mounts `./data`. Unless the container `WORKDIR` is `/`, the SQLite
file and the evidence directory land in two different places and only one of them is the mount. The
Railway profile mounts a volume at `/data`, which only the absolute path matches. Make both
absolute (`sqlite:////data/csflite.db`) and state the `WORKDIR`, or make both relative and state
the mount target.

**B11 — stale contract citation.** Design §16 line 323 cites the contract as "CHK-0001 #4 — notes
are preserved in output". The spec brief §3 row now reads "kept with the assessment record from
Phase 4; not consumed by scoring or the CSV exports", and CHK-0001 #4 is `Won't Fix` with a dated
resolution. Design §8 line 166 has the same defect. Its first clause ("`Response.notes` resolves
CHK-0001 #4") is fine — the web form does persist them — but its next sentence says "The spec
says notes are preserved in output", which is the superseded wording. *(Corrected 2026-10-22: the
first pass marked line 166 as fine.)* Update both line 166 and the §16 row to the current §3
wording, and note that the CSV exports deliberately carry no `notes` column so byte-identical
parity holds.

---

### W10 — Requote the SOC 2 supplement template (C1)

**Problem.** `templates/soc2-supplement-questionnaire.csv` has a 7-field header and three rows with
more fields than that: rows 7, 16 and 22 parse to 9, 8 and 9 fields. Cause: unquoted commas inside
the `question` value — for example row 7's question contains `"e.g. badge readers, keypads"`, and
row 22's contains `"systems, personnel, vendors"`.

Parsed, row 7 yields `evidence = " badges"`, `notes = " keypads)?"`, `response = "<the real
evidence text>"`, and the rest spills into an unnamed eighth column. The 9 HIPAA rows were fixed
upstream; the SOC 2 file was not.

This is a client-facing deliverable — a consultant fills it in — and it is the file the Phase 5
supplement import will read (design §16, option 2; ADR-0008).

**Fix.** Quote the `question` field on the three affected rows, exactly as the other 25 rows are
quoted. The HIPAA file shows the intended form.

**Verification.** After the edit, every row in all three templates must parse to exactly 7 fields:

```bash
python - <<'EOF'
import csv
for p in ("templates/soc2-supplement-questionnaire.csv",
          "templates/hipaa-supplement-questionnaire.csv",
          "templates/governance_checks_template.csv"):
    rows = list(csv.reader(open(p, encoding="utf-8")))
    bad = [(i, len(r)) for i, r in enumerate(rows) if len(r) != len(rows[0])]
    print(p, "->", bad or "clean")
EOF
```

Also re-read the three affected rows after quoting to confirm the `question` text is the full
sentence and the `evidence` / `notes` columns hold what they held before.

---

## 5. Out of scope

- **Any change to `tools/assess_helpers.py`.** It is the scoring core, carried over unchanged by
  ADR-0005, and pinned by the golden parity gate. Every finding above is a documentation defect
  fix, not a code fix.
- **Any change to `data/csf_lookup.csv` or the golden fixtures.** The merge is verified consistent;
  re-recording is not needed.
- **New ADRs.** W1–W10 apply decisions already locked in spec §10, ADR-0004 through ADR-0008, and
  CHK-0001/0002/0003/0004. Nothing here is a new decision. If W2, W3 or W5 turns out to require
  choosing between genuinely different options, record that choice as an ADR and link it from spec
  brief §10, as the existing rows do.
- **The Phase 4 build itself.** This plan only corrects the specifications it will be built from.

---

## 6. Verification

After every work item:

```bash
poetry run pytest                  # 28 passed, no regressions
poetry run black --check .
poetry run ruff check .
```

After all work items, a final consistency sweep:

1. **Every rewrite list names the same set** — spec brief §12, design §4 header, design §15 step 4,
   scope doc "What is retired". (W4)
2. **Every path reference resolves** — no `.claude/docs/…`, no `docs/design/…`, no
   `csflite-assessment-philosophy.md`. (already clean on `master`; re-check after edits)
3. **The design's §17 acceptance criteria are satisfiable** — walk each one and confirm the design
   states how. (W1, W3, W8 add criteria; W2, W5, W6, W7 remove ambiguity)
4. **`git grep` for the superseded contract wording** — "preserved in output" for `notes`,
   "largest weighted gaps" for severity, "non-loopback" for the auth guard. (W9)
5. **All three templates parse to 7 fields.** (W10)

---

## 7. Resolution — 2026-10-22

All ten work items applied on `review/minimax`. Where a work item offered a choice, the
recommended option was taken, except W2.

| Item | What changed |
|---|---|
| W1 | Design §5 gains "The view supplies the display name", citing the KeyError. §17 gains the matching criterion |
| W2 | **Alternative taken, not the recommendation.** Compose maps `${PORT:-8000}:${PORT:-8000}` and forwards `PORT` into the container. Pinning the container to 8000 would contradict §11's Railway profile, where Railway sets `PORT` and gunicorn must bind it. The forwarding option keeps "gunicorn binds `0.0.0.0:$PORT` in every profile" true. §9, §10 and §11 state it; §17 gains a criterion |
| W3 | Default `CSFLITE_ALLOWED_HOSTS` is `localhost,127.0.0.1`. Guard 2 reworded in design §10 and ADR-0007. ADR-0007 gains a dated amendment. §11 names both URLs. §18 gains a row |
| W4 | Design §15 step 4 and the scope doc name the §3 Path Configuration contract |
| W5 | JSON dropped from the scope doc, roadmap, and design §5 diagram |
| W6 | Design §2 gains a `global_helpers.py` row. §8 names `write_to_csv()` as the export writer, via a temporary file. §9 and §15 step 3 delete `get_paths()`, its `__all__` entry, and its two tests. §13 cites the writer |
| W7 | Design §9 adds `CSFLITE_CSF_LOOKUP`. §8 defines `lookup_digest` as a SHA-256 of the file bytes. §12 ships the file in the image, not bind-mounted. §8 now says a reweight takes effect on the next build and restart |
| W8 | Design §14 names both validation sets, and adds the completeness check (all 25 rows, no repeats) that the scoring guards do not cover. §17 gains the import criterion |
| W9 | B9: design §6 and §13 use `governance_assessment.csv` / `governance_heatmap.csv`. B10: `DATABASE_URL` is `sqlite:////data/csflite.db`; §11 mounts the host's `./var` (already gitignored) at `/data`, so client data never lands in the tracked `data/` directory. B11: design §8 and §16 use the current §3 wording |
| W10 | The three SOC 2 `question` fields are quoted. All three templates parse to 7 fields |

Two corrections to this plan:

- **B11** missed design §8 line 166 (corrected in place above).
- **W10** says to quote the field "exactly as the other 25 rows are quoted". The other rows are
  not quoted. Their `question` text has no commas, so they need no quotes. Only the three rows with
  commas were quoted.

`CHK-0004` still states the old `localhost` default. It is a dated review record and was not edited.

---

## Appendix — reproducing each finding

```bash
# B1 — the name never reaches the scoring call
python -c "
import sys; sys.path.insert(0,'.')
from tools.assess_helpers import get_csf_lookup, generate_governance_assessement
generate_governance_assessement(
    [{'csf_subcategory_id':'GV.PO-01','response':'Yes','notes':''}],
    get_csf_lookup('data/csf_lookup.csv'))
"
# → KeyError: "['csf_subcategory_name'] not in index"

# B2 — PORT vs the compose container port
grep -n 'PORT' docs/specs/design/phase-4-web-interface.md

# B3 — the allowlist default vs the published port
grep -n 'CSFLITE_ALLOWED_HOSTS' docs/specs/design/phase-4-web-interface.md

# B4 — the three rewrite lists
grep -n 'Path Configuration' docs/specs/csflite-spec-brief.md docs/specs/design/phase-4-web-interface.md
grep -n 'are rewritten' docs/specs/phase-4/web-interface-scope.md
grep -n 'Rewrite spec brief' docs/specs/design/phase-4-web-interface.md

# B5 — JSON promised vs specified
grep -n 'JSON' docs/specs/phase-4/web-interface-scope.md docs/development_roadmap.md
grep -n 'export/' docs/specs/design/phase-4-web-interface.md

# B6 — the export writer and the orphaned helper
grep -n 'write_to_csv' tools/global_helpers.py tests/test_golden_pipeline.py
grep -rn --include='*.py' 'get_paths' tools/ tests/

# B7 — no path for the reference data
grep -n 'csf_lookup\|lookup_digest' docs/specs/design/phase-4-web-interface.md

# B8 — the import's validation set
sed -n '/^## 14\./,/^---/p' docs/specs/design/phase-4-web-interface.md
grep -n 'not found in CSF lookup' tools/assess_helpers.py

# C1 — the ragged SOC 2 rows
python -c "
import csv
rows=list(csv.reader(open('templates/soc2-supplement-questionnaire.csv', encoding='utf-8')))
print([(i,len(r)) for i,r in enumerate(rows) if len(r)!=len(rows[0])])
"
```
