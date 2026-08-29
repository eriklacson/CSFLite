# CHK-0001: Scoring Rubric Review

## Date

2026-08-29

## Scope

The coverage scoring rubric and heatmap classification, reviewed against spec brief §3, the §3
Design Rules, and `docs/assessment_philosophy.md`.

Reviewed: `tools/assess_helpers.py` — `generate_governance_assessement()` and
`generate_governance_heatmap()`. Reference data: `data/csf_lookup.csv`.

Prompted by Phase 4. A golden fixture recorded from the current CLI will lock this behavior in as
the reference the web rewrite is tested against, so the rubric was reviewed before recording.

## Findings

| # | Status | Finding |
|---|---|---|
| 1 | Fixed | Unanswered control classified as `low` severity |
| 2 | Accepted | Heatmap severity ignores subcategory weight |
| 3 | Fixed | Assessment and heatmap can report different `gap_score` |
| 4 | Open | `notes` dropped despite §3 saying preserved |

---

## 1. Unanswered control classified as low severity

**Status:** Fixed

**Location:** `generate_governance_assessement()`, response mapping

A blank or non-conforming `response` mapped to NaN. The NaN propagated into `assessment_score`, and
in `score_to_sev` both comparisons returned False, so the row fell through to `low`.

An unanswered control was reported as having no gap. The shipped
`templates/governance_checks_template.csv` has every response blank, so this was reachable with the
delivered template.

The same silent-`low` path was reachable a second way: a `csf_subcategory_id` absent from
`csf_lookup.csv` produced a NaN `weight` through the left join.

**Reproduction** (before the fix):

```
input:  response = ""
output: severity = "low", gap_score = "nan"
        json.dumps → "score": NaN     (invalid JSON)
```

**Why it matters.** The tool exists to surface gaps. Reporting an unanswered control as covered is
the worst available failure direction, and it is silent — no warning, and the output looks
well-formed. The invalid JSON is a second-order effect: `json.dump` emits a bare `NaN` literal,
which no conforming parser accepts.

**Resolution.** Two guards added after the merge, raising `ValueError` and naming the offending
subcategory IDs:

- response not exactly `Yes`, `Partial`, or `No`
- `csf_subcategory_id` not present in the CSF lookup

`main()` in `governance_check.py` already catches `ValueError`, so the CLI prints a clean message
with no traceback and writes no output files.

The score is now mapped from the post-merge frame rather than the pre-merge one. The previous line
relied on positional index alignment across a merge, which holds only while `csf_subcategory_id` is
unique in the lookup.

Regression tests: `tests/test_assess_helpers.py`, one per guard.

**Behavior change for release notes.** A partially-filled checklist now fails instead of producing a
report. Correct per §3 — response is required, exactly those three values — but it will affect
anyone mid-assessment.

---

## 2. Heatmap severity ignores subcategory weight

**Status:** Accepted — weight-independence is deliberate; `Yes` now returns `none`

**Location:** `score_to_sev()` inside `generate_governance_heatmap()`

`severity` is a pure function of `response`. Weight has no effect on it.

The cause is algebraic. `assessment_score` is `score × weight`, and both thresholds are expressed in
terms of `weight`, so weight cancels:

- `score = 0` → `0 <= 0` → `high`
- `score = 0.5` → `0.5w < w` → `medium`
- `score = 1` → `w >= w` → `low`

**Reproduction:**

```
 weight  response  severity
    1.0       Yes       low
    1.0   Partial    medium
    1.0        No      high
    1.2        No      high      ← identical to weight 1.0
    1.5        No      high      ← identical to weight 1.0
```

**Why it matters.** The heatmap output carries both `response` and `severity` in the same row. Since
one determines the other, `severity` conveys no information the reader does not already have.

A "No" on a critical 1.5 control is classified identically to a "No" on a foundational 1.0 control.
Spec §3 describes this output as "severity-classified gap prioritization", which implies severity
participates in prioritization. It does not.

Prioritization does work — the heatmap sorts by `gap_score`, which is weight-scaled, satisfying the
philosophy doc's "prioritized gaps based on subcategory weighting". The sort carries the weighting.
The severity column does not.

**Options.**

*Accept as a response label.* Document that `severity` restates `response` and that ranking comes
from the `gap_score` sort. Cheapest. Leaves a redundant column in a client-facing output.

*Drop the column.* Removes the redundancy. Breaking change to the §3 heatmap contract, and any
consumer rendering colour bands by severity has to switch to `gap_score`.

*Make it weight-aware.* Classify on absolute `gap_score` bands rather than thresholds relative to
weight, so a "No" on 1.5 outranks a "No" on 1.0. Changes scoring semantics.

**Recommendation.** Decide before a golden fixture is recorded — a fixture makes this expensive to
change. No recommendation on which option: this is a methodology call, and
`docs/assessment_philosophy.md` is authoritative on methodology.

**Resolution.** The weight-aware option was implemented, reviewed adversarially, and reverted. See
[CHK-0002](CHK-0002-adversarial-review-severity-rework.md) for the evidence that killed it.

Four bands on the weighted gap (`none` / `low` ≤ 0.75 / `medium` < 1.2 / `high`) changed the outcome
in exactly one cell of the nine weight × response combinations, and demoted 10 of 25 rows in the
shipped example — including "Data-at-rest is protected" answered No, from `high` to `medium`. The
cause is structural: weights span only 1.0 to 1.5, which is not enough range to band three coverage
classes without overlap.

Severity is now a function of coverage alone:

| Severity | Condition |
|---|---|
| `none` | `score = 1` (Yes) |
| `medium` | `score = 0.5` (Partial) |
| `high` | `score = 0` (No) |

This is the original behavior with one change: `Yes` returns `none` rather than `low`. A covered
control has no gap, so it carries no severity.

Weight is not abandoned — it drives priority through `gap_score`, which is the sort key. Two absent
subcategories both read `high`, and the one weighted 1.5 sorts above the one weighted 1.0. Weight
gets full resolution in the ordering instead of being flattened into a four-value label.

Spec §3 and `docs/GETTING_STARTED.md` updated. `output/examples/.../governance_heatmap_example.csv`
regenerated — 3 rows changed, all `low` → `none`.

---

## 3. Assessment and heatmap can report different gap_score

**Status:** Fixed

**Location:** `generate_governance_heatmap()` — the `astype(float)` on `assessment_score` and the
`gap_score` recomputation that follows

`generate_governance_heatmap()` casts `assessment_score` back from the string the assessment already
formatted to two decimals, then recomputes `gap_score` from that rounded value.
`generate_governance_assessement()` computed its `gap_score` from the unrounded float.

The two paths diverge whenever `score × weight` needs more than two decimals.

**Reproduction:**

```
weight 1.25, response Partial

  assessment_score = 0.62,  gap_score = 0.62
  heatmap                   gap_score = 0.63     ← disagrees
```

`1.25 × 0.5 = 0.625`. The assessment computes `1.25 − 0.625 = 0.625` → `"0.62"`. The heatmap parses
`"0.62"` and computes `1.25 − 0.62 = 0.63`.

**Why it matters.** Not reachable today. The three weights in use — 1.0, 1.2, 1.5 — all produce
exact two-decimal scores at every response value.

It becomes reachable the moment anyone adds a weight like 1.25, and `docs/assessment_philosophy.md`
line 444 already uses 1.25 in its worked example. Spec §10 states that reweighting a subcategory
"requires only changing this file", so a maintainer would hit this with no warning and no test
failure. Two client-facing deliverables would then disagree on the same number.

The underlying mistake is architectural: formatting is presentation, and the heatmap does arithmetic
on a presentation value.

**Options.**

*Recompute from unformatted inputs.* The assessment output already carries `score` and `weight`
unformatted. The heatmap can compute `score × weight` directly and never parse the rounded string.
Two lines, no contract change.

*Reuse the assessment's `gap_score`.* Also removes the divergence, but the heatmap sorts numerically
before formatting, so it still needs a float — same work, weaker guarantee.

**Recommendation.** Take the first option, before recording a golden fixture. A fixture taken now
would cement the inconsistency as reference behavior. Add a weight that exercises three decimals to
the fixture input so the case stays covered.

**Resolution.** `generate_governance_heatmap()` now computes the gap from `score × weight` and never
parses the rounded `assessment_score` string. Its required-columns set changed from
`assessment_score` to `score` as a result. Regression test asserts both outputs agree at weight 1.25.
Kept through the finding 2 revert — it is correct regardless of how severity is derived.

**Related notes.** Rounding is half-to-even, Python's f-string default: `0.625` formats as `"0.62"`,
not `"0.63"`. Consistent, but worth knowing for a client-facing number.

A weight of `0` would classify a "Yes" as `high`, since `assessment_score` would be 0. Not reachable
— all weights are ≥ 1.0 — and the finding 1 guards do not catch it, because 0 is not NaN.

---

## 4. notes dropped despite contract saying preserved

**Status:** Open

**Location:** `get_governance_checklist_results()`, the `required_columns` projection

Spec §3 documents `notes` in the Governance Checklist Input as "Assessor notes (preserved in output,
not consumed by scoring)".

`get_governance_checklist_results()` projects the frame to four columns — `csf_function`,
`csf_subcategory_id`, `csf_subcategory_name`, `response` — and discards everything else. `notes`
never reaches the assessment output.

`evidence` and `question` are also dropped, but §3 marks those informational with no preservation
claim, so only `notes` contradicts the contract.

**Why it matters.** Small today, larger in Phase 4. The web questionnaire will collect notes per
question, and an assessor writing context into a field that silently vanishes from the report is a
bad experience that looks like data loss.

§3 is prescriptive — it states that implementations deviating from these contracts are bugs. Either
the code or the contract is wrong; right now they disagree.

**Options.**

*Carry `notes` through.* Add it to the projection and to the assessment output columns. Changes the
§3 Governance Assessment Output contract, which does not currently list `notes`.

*Amend the contract.* Drop "preserved in output" from §3 and mark `notes` informational like
`question` and `evidence`.

*Handle it in the Phase 4 adapter.* Keep the scoring call unchanged and rejoin notes for the report
outside the scoring path. Avoids touching the module, but leaves the CLI contract wrong for as long
as the CLI exists.

**Recommendation.** Decide alongside the Phase 4 web form design, since that is where notes become
user-visible. If notes appear in the delivered report, take the first option and update §3 to match.
Whichever way it goes, the code and §3 need to agree.

---

## What was verified as correct

Recorded so the next run knows what has already been checked.

- Response mapping is `Yes=1, Partial=0.5, No=0`, matching §3 and the philosophy doc's evidence rule
- `assessment_score = score × weight` and `gap_score = weight − assessment_score`, matching §3
- All 25 weights are in the documented set: five at 1.0, nine at 1.2, eleven at 1.5
- No control IDs, weights, or thresholds are hardcoded — all derived from `csf_lookup.csv` at
  runtime, satisfying the §3 Design Rule
- Severity thresholds match what §3 documents, including the `assessment_score` basis (§3's heatmap
  table says "score", which reads ambiguously against the `score` column, but the code follows the
  documented intent)
