# Checks

One review run, one document. All findings from a run live in that run's file.

## Naming

```
CHK-NNNN-subject-slug.md
```

- `NNNN` — zero-padded, assigned per run in chronological order, never reused
- slug — names what was reviewed (`scoring-rubric-review`), not what was found

This mirrors `docs/adr/ADR-NNNN-*.md`. The two are different things: an ADR records a decision and
its rationale, a check records what a review run found. A finding settled by a real design decision
should link to the ADR that settles it.

## Structure

Each run document opens with a summary table — one row per finding, with its status — then a
section per finding. Cite a finding as `CHK-0001 #2`.

Findings carry their own status; the document does not have one. A run is never "closed", because
its findings resolve independently.

| Status | Meaning |
|---|---|
| `Open` | Confirmed, not yet addressed |
| `Fixed` | Code changed; the fix is named in that finding's Resolution |
| `Accepted` | Behaves as designed. Reasoning recorded, the entry stays as the answer |
| `Won't Fix` | Real, but not worth addressing. Reason recorded |

Findings are not deleted when resolved. The document is the record.

## Writing a finding

Location, Summary, Reproduction, Why it matters, Options, Recommendation. Drop what does not apply,
add Resolution when it is fixed. Reproduction should be runnable or copy-pasteable output, not prose.

Record what passed, too. A run that only lists defects tells the next reviewer nothing about what
was already verified.
