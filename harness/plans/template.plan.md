---
plan: 01-name                 # the stub of the scope this plan delivers
scope_doc: docs/scopes/01-name.scope.md
status: draft                 # draft | approved
round_limit: 5                # default round limit per task; a task row can override it
---

# Plan 01-name — {{Scope name}}

> The agent drafts this plan as `harness/drafts/<stub>.plan.md`, with `<stub>.check.sh` and `<stub>.gate.yaml` beside it.
> A person approves it and moves all three into `harness/plans/`.
> After approval only the Status column changes, and only `mark-done.sh` changes it.

## What this plan delivers

One sentence, taken from the scope.

## Tasks

Do the tasks in order. A task starts only when every task it depends on is `done`.

| ID | Task | Depends on | Check | Round limit | Status |
|---|---|---|---|---|---|
| T-1 | | — | `bash harness/plans/01-name.check.sh T-1` | 5 | todo |
| T-2 | | T-1 | | 5 | todo |

## How the tasks cover the scope

Every success criterion in the scope maps to at least one task.

| Success criterion | Task |
|---|---|
| SC-1 | T-1 |

## Rules from the ruleset

The process rules in `harness/rules.md` apply to every plan automatically. List here only the ruleset rules that apply to the tasks in this plan. A project with no ruleset lists the rows of its standards record instead.

| Rule | How it is checked |
|---|---|
| | |

## Not in this plan

What this plan leaves out, and why.
