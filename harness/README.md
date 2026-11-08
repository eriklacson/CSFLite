# harness/

This folder holds the plans the agent works from, and the scripts that hold the agent to its checks. People write the spec, the records and the scopes in `docs/`. The agent turns one scope at a time into a plan here.

## Two folders, two permissions

| Folder | Who writes it | What it holds |
|---|---|---|
| `drafts/` | The agent, during PLAN | A plan being drafted, with its check script and gate |
| `plans/` | A person moves the files here at approval. After that only the harness scripts write here. | Approved plans and everything the loop produces for them |

Approval is a physical move. The agent can write to `drafts/` but not to `plans/`, so an approved plan cannot be quietly edited. The agent's tool settings block edits to `plans/`.

That block covers the Edit and Write tools only. A shell command can still write a file. The approval hash (`<stub>.approved.sha`, rule P-2) is the backstop: `mark-done.sh` refuses to run if anything but the status column changed. Until that script is built, this backstop is not enforced.

## File names

Every file here is named `<stub>.<type>.<extension>`. The stub is the stub of the scope the plan delivers, so all files for one scope sort together.

## Rules

`rules.md` lists the process rules in full, with how each will be checked. In short:

- An approved plan never changes, except its status column. Only `loop/mark-done.sh` writes status, and only after the task's check passes.
- A plan's tests never change after their hash is taken.
- The log only grows. New entries are added at the end.
- The agent never writes to `docs/` from here.
- To change scope, write a decision record and draft a new plan.
- Deleting `harness/` must leave a project that still builds. Nothing in the product depends on it.

## Layout

```
harness/
  rules.md                     the process rules every project follows
  drafts/
    02-billing.plan.md         a plan being drafted
    02-billing.check.sh        its checks, drafted with it
    02-billing.gate.yaml       its system-wide checks, drafted with it
  plans/
    CURRENT                    the stub of the approved scope being worked on
    template.plan.md           starting point for a new plan
    01-login.plan.md           the approved plan: tasks in order, each with its check and status
    01-login.check.sh          the check for each task
    01-login.gate.yaml         system-wide checks, built from the build records
    01-login.approved.sha      hash of the plan and check script at approval, ignoring the status column
    01-login.tests.sha         hash of the plan's tests, taken after they first run and fail
    01-login.log.jsonl         one entry per round
  loop/
    mark-done.sh               runs a task's check and sets its status to done if it passes
    stop-check.sh              run by the Stop hook; blocks the agent from stopping while a check fails
    gate.sh                    runs the system-wide checks
```

The tests themselves live in the project's own `tests/` folder, because they are part of the product. The check script names which tests prove each task.

## What exists today

| Path | Status |
|---|---|
| `rules.md` | The process rules every project follows. Not yet tied to checks. |
| `drafts/` | Empty |
| `plans/template.plan.md` | In place |
| `plans/00-restructure.*` and `plans/CURRENT` | The plan that set up this layout in the jig repo itself. Removed at its release approval, so new projects never inherit it. |
| `loop/*.sh` | Not written yet. See `loop/README.md`. |
