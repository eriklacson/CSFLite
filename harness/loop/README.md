# harness/loop/

The scripts that hold the agent's loop to the checks. None of them are written yet.

The loop is the agent's own loop. It works through the plan's tasks in one context. These scripts make sure the agent never decides by itself that a task is done.

| Script | What it does | Install status |
|---|---|---|
| `mark-done.sh <stub> <task-id>` | Runs the task's check. If it passes, sets the task's status to `done` in `<stub>.plan.md`. If it fails, changes nothing. Refuses if anything other than the status column differs from `<stub>.approved.sha`. | unbuilt |
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
