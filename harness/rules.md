# Process rules

These rules govern the jig process itself: how specs, scopes, plans and tasks are written and closed. They apply to every project, whatever its ruleset.

Rules about the software being built live in the project's ruleset, in `rulesets/<name>/rules.md`. A ruleset never repeats these rules. This split is why each project needs only one ruleset.

None of these rules is tied to a working check yet, so all are `unbuilt`.

| ID | Rule | How it will be checked | Enforced at | Install status | Was |
|---|---|---|---|---|---|
| P-1 | A task is done only when its check passes. | `mark-done.sh` reruns the check and writes `done` only on exit code 0. | Every task | unbuilt | neutral N-1 |
| P-2 | An approved plan changes only in its status column. | `mark-done.sh` compares the plan and check script with `<stub>.approved.sha` before writing. | Every task | unbuilt | — |
| P-3 | A task's tests do not change after their hash is taken. | `stop-check.sh` compares the tests with `<stub>.tests.sha` every round. | Every round | unbuilt | — |
| P-4 | Every task links to the scope criteria it covers and to its tests. | Plan approval fails if a task has no link in the plan's coverage table. | Plan approval | unbuilt | neutral N-3 |
| P-5 | Every scope has at least one deliverable and one success criterion. | The agent cannot draft a plan for a scope missing either. | PLAN | unbuilt | neutral N-5 |
| P-6 | Every success criterion can be checked by a command, or is marked `human`. | Plan approval fails on a criterion with an empty "Checked by" cell. | Plan approval | unbuilt | lean-security LS-6 |
| P-7 | Every constraint is specific enough to enforce. | A person judges it at plan approval. No command can check this. | Plan approval | unbuilt | lean-security LS-7 |
| P-8 | Every outcome in the spec is covered by at least one scope, or listed as deferred. | A check over the spec and `docs/scopes/` fails on any uncovered outcome. | Plan approval | unbuilt | neutral N-7 |
| P-9 | Every scope change has an accepted decision record. | Release approval is blocked if the scope differs from the plan with no record. | Release approval | unbuilt | neutral N-4 |
| P-10 | Every file the process produces is named `<stub>.<type>.<extension>`, with lowercase stubs. The project name is the spec's stub. | A name check over `docs/`, `harness/drafts/` and `harness/plans/`. | Every round | unbuilt | neutral N-6 |

## Why these live in the harness

The harness enforces rules but does not define what good software is. These rules don't describe the software. They describe jig's own documents and steps, which the harness already owns. If they lived in a ruleset, every ruleset would need a copy, and the copies would drift.
