---
doc: scope
scope: scope-check-fixes
spec_outcomes: []
status: ready for plan
version: 0.1
date: 2026-11-28
---

# Scope scope-check-fixes — Close the gaps the review found in the scope check

> The independent review of plan `scope-template-check` found gaps in `harness/loop/scope-check.sh` and `harness/loop/approve.sh`. This scope closes them. It also repairs that plan's T-2 record, which a parsing bug wrote into the wrong cell.
> Drafted by the agent. Accepted by the architect on 2026-11-28 (`status: ready for plan`).

## 1. What this scope delivers

`approve.sh` and `scope-check.sh` enforce rules P-2, P-5, P-6 and P-11 without the holes the review found, and plan `scope-template-check` has a correct T-2 record.

## 2. Rows it covers

| Record | Row ID |
|---|---|
| `harness/rules.md` | P-2 |
| `harness/rules.md` | P-5 |
| `harness/rules.md` | P-6 |
| `harness/rules.md` | P-11 |

## 3. Success criteria

| ID | Criterion | Checked by |
|---|---|---|
| SC-1 | `approve.sh` refuses a plan whose scope is the template itself | `test_approve_refuses_template_scope` |
| SC-2 | `approve.sh` refuses a plan whose scope status is not `ready for plan` | `test_approve_refuses_draft_scope` |
| SC-3 | Table rows split only on unescaped pipes, in plans and in scopes. An escaped pipe stays text. | `test_escaped_pipe_in_scope_cell_is_text`, `test_escaped_pipe_in_task_row_is_text` |
| SC-4 | A scope table row whose cell count differs from its header fails | `test_short_row_fails` |
| SC-5 | "Rows it covers" fails on an empty Row ID, a record outside the repo, or a row ID that is not the first cell of a table row in the record | `test_empty_row_id_fails`, `test_record_outside_repo_fails`, `test_row_id_only_in_prose_fails` |
| SC-6 | A criterion or deliverable counts toward P-5 only when its text cell is filled | `test_id_only_criterion_does_not_count` |
| SC-7 | Open items IDs follow the template's prefix | `test_open_item_bad_prefix_fails` |
| SC-8 | `--all` fails on a scope_doc outside the repo, and warns (does not fail) on a draft plan with no scope. `approve.sh` still refuses such a draft. | `test_all_fails_scope_doc_outside_repo`, `test_all_draft_without_scope` |
| SC-9 | A change to the template changes what the check requires | `test_template_change_changes_rules` |
| SC-10 | `AGENTS.md`, `harness/loop/README.md` and `harness/rules.md` say only what the code does | Plan check T-5 |
| SC-11 | Plan `scope-template-check` T-2 reads Round limit `3` and Status `done`, and its approval hash matches | Plan check T-6 |

## 4. Deliverables

| ID | Deliverable | Description |
|---|---|---|
| D-1 | Tests first | New harness tests for SC-1 to SC-9, written and shown to fail before any fix |
| D-2 | Parser fix | `split_row` in `harness/loop/planlib.py` splits only on unescaped pipes. Used by plan tables and scope tables. |
| D-3 | Scope check fixes | Cell count, the three "Rows it covers" holes, the text-cell rule for P-5, the Open items prefix, and the `--all` handling of scope_doc paths |
| D-4 | Approval fixes | `approve` refuses the template as a scope, and refuses a scope whose status is not `ready for plan` |
| D-5 | Template example row | `docs/scopes/template.scope.md` §6 gets an example row `OI-1`, so Open items get a prefix like the other sections |
| D-6 | Docs say what the code does | `AGENTS.md`, `harness/loop/README.md` and `harness/rules.md` P-11 corrected |
| D-7 | One-time repair | The architect corrects T-2's row in plan `scope-template-check` and rewrites its approval hash once, as a recorded one-off |

## 5. Not in this scope

| ID | Left out | Why |
|---|---|---|
| NG-1 | Stale citations of the old Phase 4 scope headings in `standards.md` and `standards-gaps.md` | Docs-only change. Needs its own plan. |
| NG-2 | The tests hash-lock | Part of jig's unbuilt parts, tracked in eriklacson/jig#6 |
| NG-3 | A `##` line inside a code fence read as a heading | Gives a false failure, never a bypass. Low value now. |
| NG-4 | Carrying the fixes over to jig | After CSFLite proves them |
| NG-5 | A general re-hash command | A standing way to rewrite approval hashes would weaken P-2. The repair in D-7 is a one-off done by the architect. |

## 6. Open items

| ID | Item | Why it is still open | What it blocks |
|---|---|---|---|
