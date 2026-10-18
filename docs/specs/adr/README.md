# Architecture Decision Records

One decision per file: `ADR-NNNN-subject-slug.md`. Numbers are assigned in order and never reused.

An ADR records a decision and why it was made. A check in `.claude/checks/` records what a review
found. A finding settled by a decision links to the ADR.

| ADR | Decision |
|---|---|
| [0001](ADR-0001-full-csf-crosswalk.md) | SOC 2 crosswalk maps to the full CSF 2.0 set |
| [0002](ADR-0002-fixed-25-subcategory-scope.md) | Scope fixed at 25 subcategories |
| [0003](ADR-0003-coverage-only-scoring.md) | Coverage-only scoring; severity from coverage alone |
| [0004](ADR-0004-single-reference-data-file.md) | `csf_lookup.csv` is the single reference file |
| [0005](ADR-0005-web-application-replaces-cli.md) | Web application replaces the CLI |
| [0006](ADR-0006-self-hosted-container-delivery.md) | Self-hosted container, portable not elastic |
| [0007](ADR-0007-operator-declared-public-mode.md) | Password required only when declared public |
| [0008](ADR-0008-supplements-collected-not-scored.md) | Supplements collected, not scored |
