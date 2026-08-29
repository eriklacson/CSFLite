# CHK-0002: Adversarial Review Of The Severity Rework

## Date

2026-08-29

## Scope

Adversarial review of the working-tree changes to `tools/assess_helpers.py` — the input guards from
[CHK-0001](CHK-0001-scoring-rubric-review.md) #1, the weight-banded severity from #2, and the gap
computation from #3.

The brief was to break six claims the author had asserted, not to summarise the change. Findings
below were independently reproduced before being acted on.

## Findings

| # | Status | Finding |
|---|---|---|
| 1 | Fixed | Weight bands reopened the silent-low path they were meant to close |
| 2 | Fixed | Weight bands demoted 10 of 25 rows in the shipped example |
| 3 | Fixed | Blank spreadsheet row raised `TypeError`, not `ValueError` |
| 4 | Fixed | Threshold constants pinned by no test — three mutants survived |
| 5 | Fixed | Downstream docs and committed example output left stale |
| 6 | Open | CLI exits 0 after reporting a data error |

---

## 1. Weight bands reopened the silent-low path

**Status:** Fixed

The CHK-0001 #1 guards closed the NaN route to a wrongly-reassuring severity. Banding on the
weighted gap opened a second route through low weights.

```
weight=0.5, response=No  ->  gap 0.50  ->  severity "low"
weight=0.0, response=No  ->  gap 0.00  ->  severity "none"
```

An entirely absent control read as `low`. At weight 0 it read `none`, which the spec defined as
"Control is covered" — a false statement in a client deliverable. The pre-change code returned
`high` for a zero score at every weight, so this class of defect was introduced by the fix.

Weights are maintainer-editable in `data/csf_lookup.csv` and the thresholds were documented as
tunable, so this was reachable rather than theoretical.

**Resolution.** Severity is now derived from `score` alone. Verified at weights 0.0, 0.5, 1.0 and
1.5: an absent control is `high` at every one.

---

## 2. Weight bands demoted 10 of 25 rows in the shipped example

**Status:** Fixed

Measured against `input/examples/governance_check/governance_check_sample.csv`.

Weight changed the severity in one cell of nine:

```
w=1.0   Yes none | Partial low | No medium
w=1.2   Yes none | Partial low | No high
w=1.5   Yes none | Partial low | No high
```

Severity remained a pure function of `response` in the other eight. `Partial` was never separated by
weight at all.

The cost was 10 demoted rows, including "Data-at-rest is protected" answered No dropping from `high`
to `medium`, and "Identities and credentials are managed" — MFA, weight 1.5, the highest in the
framework — answered Partial reading as `Partial | low` with the two fields adjacent in the same row.

Structural cause: weights span 1.0 to 1.5. A 1.5x range cannot be banded to separate three coverage
classes without overlap.

**Resolution.** Reverted to coverage-driven severity with `none` retained for covered controls. See
CHK-0001 #2 Resolution. Regenerating the example changed 3 rows, all `low` → `none`, confirming the
revert restored prior behavior apart from the intended `Yes` fix.

---

## 3. Blank spreadsheet row raised TypeError

**Status:** Fixed

A trailing partly-empty row — what a hand-edited spreadsheet produces — made `csf_subcategory_id`
NaN. The guard's error message built its list with `', '.join(...)` and raised before it could
report anything useful.

```
TypeError: sequence item 0: expected str instance, float found
```

`main()` in `governance_check.py` catches only `ValueError`, so the user got a raw traceback.

**Resolution.** IDs are coerced to `str` when building both guard messages. The same input now
raises `ValueError` and prints cleanly.

---

## 4. Threshold constants pinned by no test

**Status:** Fixed

Mutation testing against the band implementation. Three mutants survived the full suite:

| Mutation | Result |
|---|---|
| `SEVERITY_LOW_MAX` `0.75` → `0.99` | survived |
| `SEVERITY_MEDIUM_MAX` `1.2` → `1.49` | survived |
| `elif gap < SEVERITY_MEDIUM_MAX` → `<=` | survived |

The third moved every weight-1.2 absent control from `high` to `medium` — 3 of 25 rows in the
shipped example — with no test failing. The tests chose gap values sitting comfortably inside bands
and never defended a boundary.

A related observation: both boundaries were exactly reachable with shipped weights, and the
operators resolved them in opposite directions. `1.5 × 0.5 = 0.75` exactly, caught by `<=` and
rounded to less severe. `1.2 − 0 = 1.2` exactly, missed by `<` and rounded to more severe.

**Resolution.** The thresholds no longer exist. The replacement logic is mutation-tested — five
mutants against the coverage branches and the gap expression, all caught.

---

## 5. Downstream docs and committed example left stale

**Status:** Fixed

The severity change did not propagate:

- `docs/GETTING_STARTED.md` documented severity as `high`/`medium`/`low`, with `none` undocumented
- its Priority Framework told users to fix "high severity gaps (gap_score > 0)" first, wrong for 10
  of 25 rows under the band scheme
- `output/examples/governance_assessment/governance_heatmap_example.csv` is a committed
  expected-output artifact the tool no longer reproduced

**Resolution.** Both doc references updated. Example regenerated.

---

## 6. CLI exits 0 after reporting a data error

**Status:** Open

```
$ poetry run python tools/governance_check.py --governance_checklist <blank responses> ...
Argument Error: Response must be exactly Yes, Partial, or No — missing or invalid for: GV.RR-01
EXIT=0
```

`main()` catches `ValueError`, prints to stderr, and returns normally. No output files are written,
but the exit code reports success. Any wrapper script or CI step treats a rejected checklist as a
pass.

The handler predates these changes, but the CHK-0001 #1 guards make it the routine path:
`templates/governance_checks_template.csv` ships with every response cell empty, so the first run of
the documented workflow now lands here.

The `Argument Error:` label is also wrong for a data error.

**Recommendation.** `sys.exit(1)` in the handler, and relabel. Deferred because it changes the CLI's
exit contract, which is a decision separate from the scoring work. Phase 4 retires this entry point,
so it may be resolved by deletion.

---

## Attacks that held

Recorded so they are not re-run.

- **`Yes` → `none` at every weight.** Grid over 1.0, 1.2, 1.5, 0, −1.0, 0.5, 1e9. Held.
- **Heatmap and assessment agree on `gap_score`.** 500-case fuzz, random weights 0.01–3.0 crossed
  with all three responses. Zero mismatches.
- **Formatting does not affect classification.** Heatmap fed `assessment_score` of `"0.00"`,
  `"999.99"`, `None`, `"garbage"`. Output identical every time — it reads only `score` and `weight`.
- **Sort order.** Regenerated example byte-identical in row order to the committed one.
- **Round trip.** Empty list, single row, and CSV-read-back all handled.
- **Case and whitespace.** `"yes"`, `" Yes"`, `"YES"`, `"Yes "`, `"Partial\n"` all rejected.
- **Duplicate lookup rows.** Merge fans out, both rows scored, no crash. Pre-existing.
- **`required.issubset` returning `[]`.** Not reachable in-repo — the only caller passes assessment
  output, which contains `score`. Silent for an external caller on the old shape: returns `[]`,
  `write_to_csv([])` writes no file, and the CLI still prints "written to" and exits 0. Worth an
  exception rather than a bare `return []`, but nothing that exists is broken by it.
