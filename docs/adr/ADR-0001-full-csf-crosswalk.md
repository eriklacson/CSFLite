# ADR-0001: Map Full NIST CSF 2.0 Subcategory Set in SOC 2 Crosswalk

## Status

Accepted

## Date

2026-03-26

## Context

CSFLite measures control coverage across 25 curated NIST CSF 2.0 subcategories selected for
relevance to start-ups and SMBs (20–200 employees). These 25 controls cover the highest-impact
areas for the target market and form the basis of the governance assessment pipeline.

When extending CSFLite to support SOC 2 readiness gap analysis, a scoping decision was required:
should the CSFLite-to-SOC 2 crosswalk map Trust Services Criteria only to the 25 CSFLite controls,
or to the full NIST CSF 2.0 subcategory set (106 subcategories across 6 functions)?

The AICPA 2017 Trust Services Criteria (revised 2022 points of focus) reference security practices
that span the full CSF 2.0 subcategory set. Five SOC 2 requirement areas — change management (CC8),
physical access controls (CC6.4), security awareness and communication (CC2), business continuity
planning (A1), and data disposal (C1.2) — map primarily to CSF subcategories that are outside the
CSFLite 25. Restricting the crosswalk to the CSFLite 25 would leave these areas as undocumented
blind spots rather than explicitly identified gaps.

A readiness gap analysis that silently omits coverage for SOC 2 criteria would be misleading to
clients and their auditors. The purpose of the assessment is to surface gaps, not obscure them.

## Decision

The CSFLite-to-SOC 2 crosswalk maps all in-scope Trust Services Criteria (CC1–CC9, A1, C1) to the
**full NIST CSF 2.0 subcategory set**, not limited to CSFLite's 25 controls.

Each crosswalk entry includes an "In CSFLite 25?" flag indicating whether the mapped CSF
subcategory is assessed by the standard CSFLite governance pipeline. Entries mapping to
subcategories outside the CSFLite 25 receive a coverage rating of `gap` and are addressed by the
standalone supplement questionnaire (`templates/soc2-supplement-questionnaire.csv`).

This decision was made for the SOC 2 readiness deliverables only. It does not change the scope of
CSFLite's governance assessment pipeline, scoring engine, or `csflite/controls.json`.

## Consequences

**Positive:**
- Every in-scope SOC 2 criterion is explicitly accounted for — either covered by the CSFLite 25 or
  documented as a gap requiring supplement questionnaire responses.
- Clients and their US customers or auditors receive an honest picture of coverage and gaps.
- The supplement questionnaire addresses gap areas without modifying the existing pipeline.

**Negative / trade-offs:**
- The crosswalk is larger than if restricted to the CSFLite 25 — it references ~40 CSF
  subcategories rather than 25, requiring the assessor to collect evidence for additional items via
  the supplement questionnaire.
- The supplement questionnaire is currently a standalone CSV (Tier 1). Integration into the
  CSFLite scoring engine is deferred to Tier 2.

## Alternatives Considered

**Map only the 25 CSFLite subcategories.**
Rejected. Five significant SOC 2 requirement areas (change management, physical access, security
awareness, business continuity, data disposal) would have no mapped coverage evidence. A crosswalk
that omits these areas provides a false sense of readiness.

**Map to a custom SOC 2 control set independent of NIST CSF 2.0.**
Rejected. The value of CSFLite is its grounding in NIST CSF 2.0. Introducing a parallel control
vocabulary would break the mapping coherence and complicate future updates as CSF evolves.
