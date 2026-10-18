# ADR-0004: Keep the 25 Subcategories in One Reference File

## Status

Accepted

## Date

2026-10-16

## Context

The 25 subcategories were defined in three files: `data/csf_lookup.csv`, `data/heat_map_lookup.csv`,
and `templates/governance_checks_template.csv`. They disagreed. The display name in `csf_lookup.csv`
matched the template on only 3 of 25 rows. Nothing read `heat_map_lookup.csv`.

The Phase 4 questionnaire view needs one place to read question text, evidence prompts, and weights.

## Decision

`data/csf_lookup.csv` is the single source of truth. It holds the ID, function, display name,
question, evidence prompt, weight, recommendation, and the full CSWP 29 outcome text (`csf_outcome`).

`heat_map_lookup.csv` is retired. The governance template is regenerated from the lookup and then
frozen. It stays only as the CLI input and the Phase 4 import format.

Reference data stays in version-controlled files. It does not move into the database.

## Consequences

**Positive:**
- One file to edit when a subcategory is reweighted or reworded.
- Scoring is unaffected. It selects only `csf_subcategory_id`, `weight`, and `recommendation`.

**Negative / trade-offs:**
- The template can drift from the lookup until the CLI is retired.

## Alternatives Considered

**Keep three files and add a consistency test.** Rejected. It keeps the duplication and only
detects drift after it happens.

**Move reference data into the database.** Rejected. Reweighting would become a migration instead
of a reviewed file change.
