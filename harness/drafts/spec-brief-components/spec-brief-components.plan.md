---
plan: spec-brief-components
scope_doc: none yet   # open item: no scope doc exists. See "Open items".
status: draft
round_limit: 3
---

# Plan spec-brief-components — Label the three components in the spec brief

> Draft. Not approved. Do not start IMPLEMENT until the architect approves and moves the folder `harness/drafts/spec-brief-components/` to `harness/plans/spec-brief-components/`.

## What this plan delivers

The spec brief states that CSFLite is one framework with three components, and every section says which component it belongs to.

## The change in plain words

- CSFLite stays one framework. The toolkit is a component of it, not a separate product.
- The three components are Control Set, Assessment Method and Toolkit.
- Section numbers and section order do not change. Other documents cite them.
- No contract, rule or decision text changes. Only labels are added, and §1 is rewritten.

## Tasks

Do the tasks in order. A task starts only when every task it depends on is `done`.

| ID | Task | Depends on | Check | Round limit | Status |
|---|---|---|---|---|---|
| T-1 | Rewrite §1 Overview and "Project Components". Define the three components. State the principle: engineer governance into systems where it makes the process more efficient. State the two relationship rules (below). | — | `bash harness/plans/spec-brief-components/spec-brief-components.check.sh T-1` | 3 | todo |
| T-2 | Add a `**Component:** <value>` line under every `##` heading from §2 on, and under every `###` heading in §3, using the tag table below. | T-1 | `bash harness/plans/spec-brief-components/spec-brief-components.check.sh T-2` | 3 | todo |
| T-3 | Add a Component column to the §9 milestones table and the §10 decisions table, using the tag table below. | T-1 | `bash harness/plans/spec-brief-components/spec-brief-components.check.sh T-3` | 3 | todo |
| T-4 | Confirm nothing else moved: headings are identical to the original, and the only removed lines are in §1 or are table rows. | T-2, T-3 | `bash harness/plans/spec-brief-components/spec-brief-components.check.sh T-4` | 3 | todo |

## Relationship rules to state in §1 (T-1)

1. The Assessment Method defines what a score means. The Toolkit encodes it. If they disagree, the Method wins.
2. The Toolkit may add operational features, such as storage and notes. It may not add controls, weights or scoring rules.

These match the existing rule that `assessment_philosophy.md` overrides other documents. They do not add a new authority.

## Tag table (proposed, needs architect approval)

| Section | Component |
|---|---|
| §2 Architecture Pattern | Toolkit |
| §3 Interface Contracts (heading) | Framework-wide |
| §3 Governance Checklist Input | Assessment Method |
| §3 CSF Lookup Reference | Control Set |
| §3 Governance Assessment Output | Assessment Method |
| §3 Governance Heatmap Output | Assessment Method |
| §3 Path Configuration | Toolkit |
| §3 Design Rules | Framework-wide |
| §4 Component Registry | Toolkit |
| §5 Repository Structure | Toolkit |
| §6 Database Schema | Toolkit |
| §7 Hosting Stack | Toolkit |
| §8 Reference Data | Control Set |
| §9 Build Status | Framework-wide |
| §10 Key Design Decisions | Framework-wide |
| §11 What This Project Does Not Own | Framework-wide |
| §12 Phase 4 Web Interface | Toolkit |

§10 rows: 25-subcategory scope = Control Set. Crosswalks = Control Set. Coverage-only scoring and evidence rule = Assessment Method. Philosophy precedence = Framework-wide. Web replaces CLI, delivery model, cloud-native scope, container, pre-commit and CI = Toolkit.

§9 rows: Phases 1 and 2 = Control Set. Phases 3 and 4 = Toolkit. Phases 5 and 6 = Framework-wide.

The output CSVs are tagged Assessment Method because §12 says they carry over unchanged to the web app. Their field layout is a toolkit detail, but their meaning is the method.

## How the tasks cover the scope

No scope doc exists yet, so there are no scope criteria to map. See open items.

| Success criterion | Task |
|---|---|
| §1 defines all three components and both rules | T-1 |
| Every section is tagged | T-2 |
| Milestones and decisions are tagged | T-3 |
| No numbering, contract or rule text changed | T-4 |

## Rules from the standards record

| Rule | How it is checked |
|---|---|
| P-1 A task is done only when its check passes | `check.sh` exit code |
| Files in `docs/` change only if the approved plan lists them | This plan lists only `docs/specs/csflite-spec-brief.md`. T-4 checks no other path changed. |

## Not in this plan

These came out of the adversarial review. Each needs an architect decision first, so none is decided here.

- **Three authorities.** Where weights and severity are defined: prose, `csf_lookup.csv` or code. Needs an ADR.
- **Method version.** Adding a version field to the output contracts. This changes a contract and the golden fixtures.
- **Conformance.** A one-line definition of what following CSFLite means without the software.
- **Supplements.** Whether the SOC 2 and HIPAA tracks belong to the Control Set or the Method.
- **Reordering sections.** Rejected: it breaks references from other documents for little gain.

## Open items for the architect

1. No scope doc exists for this work. Should one be written in `docs/scopes/`, or is this plan enough for a docs-only change?
2. Approve or change the tag table.
3. The only file this plan changes is `docs/specs/csflite-spec-brief.md`. Confirm.
