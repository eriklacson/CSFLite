---
plan: scope-check-fixes
scope_doc: docs/scopes/scope-check-fixes.scope.md
status: draft
round_limit: 3
---

# Plan scope-check-fixes — Close the gaps the review found in the scope check

> Draft. Not approved. The architect sets the scope to `status: ready for plan`, then runs `harness/loop/approve.sh scope-check-fixes`, which moves this folder to `harness/plans/scope-check-fixes/`.
> After approval only the Status column changes, and only `mark-done.sh` changes it.

## What this plan delivers

`approve.sh` and `scope-check.sh` enforce rules P-2, P-5, P-6 and P-11 without the holes the independent review found, and plan `scope-template-check` has a correct T-2 record.

## Branch and order

- Branch `fix/scope-check-fixes`, based on `harness/scope-template-check`, because `master` does not have that work yet.
- The PR for `scope-template-check` is on hold until this plan is done (architect, 2026-11-28). The two PRs then merge in order: `scope-template-check` first, then this one.

## Tasks

Do the tasks in order. A task starts only when every task it depends on is `done`. No task cell in this table contains a pipe, so the old parser bug cannot touch this plan before T-2 fixes it.

| ID | Task | Depends on | Check | Round limit | Status |
|---|---|---|---|---|---|
| T-1 | Write the new tests in `harness/loop/tests/test_scope_check.py` for SC-1 to SC-9, using the names in the scope. Correct the file's docstring claim about the template. Run the new tests: they must fail. | — | `bash harness/plans/scope-check-fixes/scope-check-fixes.check.sh T-1` | 3 | todo |
| T-2 | Fix `split_row` in `harness/loop/planlib.py` so it splits only on pipes with no backslash before them. Plan tables and scope tables both use it. | T-1 | `bash harness/plans/scope-check-fixes/scope-check-fixes.check.sh T-2` | 3 | todo |
| T-3 | Fix the scope check: fail rows whose cell count differs from the header; close the three Rows it covers holes; count a criterion or deliverable only when its text cell is filled; check Open items IDs against the template prefix; make `--all` fail on a scope_doc outside the repo and warn (not fail) on a draft plan with no scope. Add the example row `OI-1` to §6 of `docs/scopes/template.scope.md`. | T-2 | `bash harness/plans/scope-check-fixes/scope-check-fixes.check.sh T-3` | 3 | todo |
| T-4 | Fix `approve`: refuse when the scope is the template itself, and refuse when the scope status is not `ready for plan`. Both refusals happen before anything moves. | T-3 | `bash harness/plans/scope-check-fixes/scope-check-fixes.check.sh T-4` | 3 | todo |
| T-5 | Correct the docs to say only what the code does: the scopes row in `AGENTS.md`, the `approve.sh` and `scope-check.sh` rows and limits in `harness/loop/README.md`, and the P-11 row in `harness/rules.md`. | T-4 | `bash harness/plans/scope-check-fixes/scope-check-fixes.check.sh T-5` | 3 | todo |
| T-6 | Architect only, one-off: correct the T-2 row in plan `scope-template-check` (Round limit `3`, Status `done`), then rewrite its approval hash with the command below. The agent then runs `mark-done.sh` on this task. | T-2 | `bash harness/plans/scope-check-fixes/scope-check-fixes.check.sh T-6` | 3 | todo |

## The one-off repair in T-6

Why it is needed: T-2 fixes the parser. The approval hash of plan `scope-template-check` was taken with the old parser, which blanked the wrong cell in its T-2 row. After T-2, that hash no longer matches, and T-2's row is still wrong.

What the architect does, on this branch, after this plan's T-2 is done:

1. In `harness/plans/scope-template-check/scope-template-check.plan.md`, in the T-2 row, set the Round limit cell to `3` and the Status cell to `done`. Change nothing else.
2. Rewrite that plan's approval hash with the shared code:

```bash
python3 -c 'import sys; sys.path.insert(0, "harness/loop"); import planlib; planlib.write_sha("scope-template-check")'
```

3. Commit both files with a message that names this as the T-6 one-off repair.

There is no standing re-hash command. A tool that rewrites approval hashes on demand would weaken P-2 (scope NG-5).

## How the tasks cover the scope

| Success criterion | Task |
|---|---|
| SC-1 | T-1, T-4 |
| SC-2 | T-1, T-4 |
| SC-3 | T-1, T-2 |
| SC-4 | T-1, T-3 |
| SC-5 | T-1, T-3 |
| SC-6 | T-1, T-3 |
| SC-7 | T-1, T-3 |
| SC-8 | T-1, T-3 |
| SC-9 | T-1, T-3 |
| SC-10 | T-5 |
| SC-11 | T-6 |

## Rules from the standards record

| Rule | How it is checked |
|---|---|
| P-1 A task is done only when its check passes | `check.sh` exit code, through `mark-done.sh` |
| P-2 An approved plan changes only in its Status column | T-2 makes the hash blank the right cell. T-6 repairs the one plan the old parser hashed wrong. |
| P-5, P-6, P-11 | Tightened by T-3 and T-4 |
| CO-11 Black, Ruff, Bandit pass | Gate G-4 |
| Files in `docs/` change only if the approved plan lists them | Only `docs/scopes/template.scope.md` (T-3) and this plan's own scope file change. T-3 and T-5 check it. |

## Files this plan changes

- `harness/loop/planlib.py`, `harness/loop/tests/test_scope_check.py`, `harness/loop/README.md`
- `harness/rules.md`, `AGENTS.md`
- `docs/scopes/template.scope.md` (one example row)
- `docs/scopes/scope-check-fixes.scope.md` (this plan's scope, written during PLAN)
- `harness/plans/scope-template-check/scope-template-check.plan.md` and its `.approved.sha` (T-6 only, by the architect)

## Not in this plan

See scope §5: stale citations of old headings, the tests hash-lock, headings inside code fences, carry-over to jig, and a general re-hash command.

## Decisions

1. **A plan may only be approved on a scope with `status: ready for plan`** (architect, 2026-11-28). Built in T-4.
2. **The `scope-template-check` PR waits for this plan** (architect, 2026-11-28).
3. **`--all` warns on a draft plan with no scope; it does not fail** (architect, 2026-11-28). CI stays green. `approve.sh` still refuses such a draft.
4. **The scope is accepted** (architect, 2026-11-28). Its status is `ready for plan`.

## Open items for the architect

None.
