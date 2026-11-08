# .claude/hooks/

How Claude Code is held to the checks while it loops. None of this is built yet.

## Why a hook

The agent works through the plan in its own loop, in one context. Left alone, the agent decides when to stop. A Stop hook takes that decision away from it.

## The Stop hook

Claude Code runs a Stop hook every time the agent tries to finish. The hook will run `harness/loop/stop-check.sh`, which:

1. Reads `harness/plans/CURRENT` and finds the first task in `<stub>.plan.md` whose status is not `done`.
2. On round 0, confirms the task's tests fail, then writes `<stub>.tests.sha`. On every later round, refuses to continue if the tests no longer match that hash.
3. Runs that task's check from `<stub>.check.sh` and adds the result to `<stub>.log.jsonl`.
4. If the check fails and the round limit is not reached, blocks the stop and sends the check's real output back to the agent.
5. If the round limit is reached, records `BUDGET` in the log and lets the agent stop.
6. If every task is `done`, lets the agent stop.

## Status

| Item | Install status |
|---|---|
| `harness/loop/stop-check.sh` | unbuilt |
| Hook entry in `.claude/settings.json` | unbuilt |

Status: Recommended, not yet agreed.

Other tools need their own adapter for the same job. OpenCode is the next target.
