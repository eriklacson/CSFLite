# ADR-0003: Score Coverage Only, and Derive Severity from Coverage Alone

## Status

Accepted

## Date

Coverage-only scoring decided in Phase 1. Severity rule decided 2026-08-29
([CHK-0001](../checks/CHK-0001-scoring-rubric-review.md) #2,
[CHK-0002](../checks/CHK-0002-adversarial-review-severity-rework.md)). Recorded 2026-10-18.

## Context

Small teams cannot defend nuanced maturity scores. They can say whether a control exists.

Each subcategory also has a weight (1.0, 1.2, or 1.5). Severity was briefly banded on the weighted
gap. With weights this close together there was no room to separate three coverage classes, and the
bands demoted real findings (CHK-0002 #2).

## Decision

**Scoring.** Each response is `Yes` (1.0), `Partial` (0.5), or `No` (0.0). There are no maturity
levels. `assessment_score = score × weight` and `gap_score = weight − assessment_score`.

**Severity.** Severity depends on coverage only: `Yes` = `none`, `Partial` = `medium`, `No` = `high`.

**Weight.** Weight sets priority through `gap_score`, which is the sort key. It never changes the
severity label.

**Evidence.** A `Yes` requires evidence. Applying that rule is the assessor's judgement. Scoring
never reads evidence, and attaching evidence never changes a score.

## Consequences

**Positive:**
- Results are defensible. A `high` always means the control is absent.
- Weight still orders the work: an absent 1.5 subcategory sorts above an absent 1.0 one.

**Negative / trade-offs:**
- The evidence rule depends on assessor discipline. The tool cannot enforce it.

## Alternatives Considered

**Maturity levels (for example 0–5).** Rejected. Not defensible for small teams, and it measures
depth before existence.

**Severity banded on weighted gap.** Tried and reverted. See CHK-0002.
