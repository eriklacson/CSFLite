# ADR-0008: Collect Supplement Answers Without Scoring Them

## Status

Accepted

## Date

2026-09-13

## Context

CSFLite ships SOC 2 (28 questions) and HIPAA (9 questions) supplement questionnaires for areas
outside the core 25 (ADR-0001). The UX prototype scored them as selectable tracks with a flat
weight of 1.0.

Scoring them would conflict with three existing rules:
- Crosswalks are reference documents, not consumed by the scoring engine (spec brief §10).
- Readiness assessments belong to client engagements, not to CSFLite (spec brief §11).
- Weights come from reference data (spec brief §8). The flat 1.0 was invented at render time.

## Decision

Phase 4 ships the core 25 only. The supplements stay CSV templates.

In Phase 5 the supplements enter the web app as tracks that are collected and exported but not
scored. No coverage score is computed for them.

Crosswalks remain reference documents in `docs/reference/`, `docs/soc2/`, and `docs/hipaa/`.

## Consequences

**Positive:**
- No locked decision moves.
- CSFLite does not imply a compliance score.

**Negative / trade-offs:**
- Supplement answers carry no coverage number. The assessor interprets them using the crosswalk.

## Alternatives Considered

**Score the supplements.** Rejected. Needs per-question weights in reference data and changes to
spec brief §10 and §11 first.

**Leave the supplements out of the web app entirely.** Chosen for Phase 4 only. Phase 5 adds them
unscored so assessors can collect everything in one place.
