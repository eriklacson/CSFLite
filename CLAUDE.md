# CLAUDE.md

Project guidance for all coding agents lives in `AGENTS.md`. Claude Code loads it through the import below. Put shared guidance there, not here. Add to this file only what is specific to Claude Code.

@AGENTS.md

## Claude Code only

- Use Plan Mode for the PLAN stage. Present the plan there and wait for approval.
- A Stop hook will run the current task's check before you can finish. See `.claude/hooks/README.md`. It is not built yet.
