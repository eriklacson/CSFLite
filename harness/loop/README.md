# harness/loop/

The scripts that hold the agent's loop to the checks. `approve.sh` and `mark-done.sh` are written. The others are not.

The loop is the agent's own loop. It works through the plan's tasks in one context. These scripts make sure the agent never decides by itself that a task is done.

Every `<stub>.*` file named below sits in the scope's folder, `harness/plans/<stub>/`.

| Script | What it does | Install status |
|---|---|---|
| `approve.sh <stub>` | Run by the architect, never the agent. Moves `harness/drafts/<stub>/` to `harness/plans/<stub>/`, sets `status: approved`, writes `<stub>.approved.sha` (the plan with its Status column blanked, and the check script) and sets `CURRENT`. Runs every check before moving anything. Refuses if the plan is already approved, a file is missing, the plan has no tasks table, or `CURRENT` names another plan with open tasks. | installed |
| `mark-done.sh <stub> <task-id>` | Runs the task's check. If it passes, sets the task's status to `done` in `<stub>.plan.md`. If it fails, changes nothing. Refuses if anything other than the status column differs from `<stub>.approved.sha`, or if a task it depends on is not done. | installed |
| `stop-check.sh` | Run by the Stop hook each time the agent tries to finish. Takes or verifies `<stub>.tests.sha`, runs the current task's check and adds the round to `<stub>.log.jsonl`. Blocks the stop while the check fails, until the round limit. | unbuilt |
| `gate.sh` | Runs the system-wide checks in `<stub>.gate.yaml`. Reports each as passed, failed or unbuilt. | unbuilt |

Install status moves from `unbuilt` to `installed` to `proven`. A check is proven only after it has caught a real mistake and held. Until then, it may be checking nothing.

## How a task runs

Before the first round, the agent writes the task's tests and runs them. They must fail, because nothing is built yet. A test that passes before any code exists checks nothing. `stop-check.sh` then hashes the tests into `<stub>.tests.sha`, so the agent cannot weaken them later.

Each round:

1. The agent changes the code.
2. The agent tries to finish, or runs the check itself.
3. The check runs and the round is added to the log.
4. If the check passes, the agent runs `mark-done.sh` and moves to the next task.
5. If it fails, the agent gets the real output and tries again, until the round limit.

The decision to stop uses only what the scripts report. Anything the agent writes is commentary.

## What controls the loop

| Control | What it is here |
|---|---|
| When a task is done | Its check returns 0 and `mark-done.sh` records it |
| How progress is measured | The number of tasks marked `done` |
| How many tries are allowed | The round limit set per task in the plan |
| Where state is kept | The plan's status column, the log and the hashes, on disk |
| What the agent sees after each try | The real output of the check |

## Exit codes

`approve.sh` and `mark-done.sh` share `planlib.py` and its exit codes.

| Code | Meaning |
|---|---|
| 0 | Done. For `mark-done.sh`, the check passed and the status is `done`, or it already was |
| 1 | The task's check failed. Status unchanged |
| 2 | Usage error or a bad stub |
| 3 | The plan or check script changed since approval (rule P-2) |
| 4 | The task or plan cannot proceed: unknown task, open dependency, missing file, already approved, or `CURRENT` busy |

## Known limits

- The approval hash covers the plan and the check script, as `VOCABULARY.md` defines it. The gate file is not covered.
- Nothing stops the agent from running `approve.sh` itself. Approval is still a person's act.
- `mark-done.sh` reads task dependencies from the plan's "Depends on" column. It understands `T-1`, `T-2, T-3` and `T-2 to T-8`.
