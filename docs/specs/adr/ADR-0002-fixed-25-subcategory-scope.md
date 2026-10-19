# ADR-0002: Fix the Framework Scope at 25 Subcategories

## Status

Accepted

## Date

Decided in Phase 1. Recorded 2026-10-18.

## Context

NIST CSF 2.0 has 106 subcategories. CSFLite's users are startups and SMEs with no dedicated
security staff. A full CSF assessment is too large for them to complete or act on.

The subcategories were selected on impact-to-effort ratio, governance clarity, and SME relevance.
The selection and its exclusions are documented in `docs/reference/top_25_sub_categories.md`.

## Decision

CSFLite assesses exactly 25 NIST CSF 2.0 subcategories, listed in `data/csf_lookup.csv`.

Adding a subcategory requires removing one. The count stays at 25.

## Consequences

**Positive:**
- An assessment fits in one sitting for a small team.
- Every gap maps to a clear, concrete action.

**Negative / trade-offs:**
- Real areas are left out (for example training, data flows, physical security).
- Compliance work needs crosswalks and supplement questionnaires to cover the gaps (ADR-0001, ADR-0008).

## Alternatives Considered

**Assess the full 106 subcategories.** Rejected. It is the scope creep that makes larger frameworks
overwhelming for the target users.

**Let the count grow over time.** Rejected. Without a cap, the framework drifts toward the size it
was built to avoid.
