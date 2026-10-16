# CHK-0003: Phase 4 Web Design Review

## Date

2026-10-16

## Scope

`docs/design/phase-4-web-interface.md` against `tools/assess_helpers.py` and the golden fixtures
in `tests/fixtures/golden/`, before implementation starts.

Prompted by the design review ahead of Phase 4 build-out. The design's acceptance criteria
require web output to be byte-identical to the golden fixtures; this review checked whether the
design, as written, actually produces that order.

## Findings

| # | Status | Finding |
|---|---|---|
| 1 | Fixed | Row order in `assessment.csv`/`heatmap.csv` depends on a sort the web view will never call |

---

## 1. Row order depends on a sort the web view will never call

**Status:** Fixed

**Location:** `tools/assess_helpers.py` — `get_governance_checklist_results()` and
`generate_governance_assessement()`

`generate_governance_assessement()` does not sort its output. The merge against `csf_lookup`
preserves the order of the input list. All row ordering in the CLI's output comes from
`get_governance_checklist_results()`, which sorts intake rows descending by `csf_subcategory_id`
before scoring runs.

The Phase 4 design (§5) has the web view build its checklist list from `Response` rows in the
database rather than from a CSV, so it never calls `get_governance_checklist_results()`. Nothing
in the design told the view to replicate that sort. Scores would still be correct in any order —
only row order in the exports would differ from the recordings.

**Reproduction:**

```
checklist = [PR.AA-03, AA.AA-01, ZZ.ZZ-99]   # arbitrary order
generate_governance_assessement(checklist, lookup)
→ [PR.AA-03, AA.AA-01, ZZ.ZZ-99]              # same order back, unsorted
```

**Why it matters.** §15 and §17 gate CLI retirement on `assessment.csv`/`heatmap.csv` being
byte-identical to `tests/fixtures/golden/`. A correct-but-differently-ordered export fails that
gate silently late in Phase 4, after the scoring logic is already trusted and the bug looks like
it must be somewhere else.

**Resolution.** §5 of the design now states the requirement explicitly: the view must order
`Response` rows descending by `csf_subcategory_id` before calling
`generate_governance_assessement()`. Added to the §17 acceptance criteria. Pinned with
`test_generate_governance_assessement_preserves_input_order` in `tests/test_assess_helpers.py`,
which asserts the function returns an unsorted input list unsorted — documenting that ordering is
the caller's job, not the scoring function's.

No code in `tools/assess_helpers.py` changed. This is a design-doc and test-only fix; there is no
web view yet to carry the sort.
