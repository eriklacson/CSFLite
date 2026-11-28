# Branch naming

Every branch in this repo follows these rules, whoever creates it: a person or an agent. `AGENTS.md` points here.

## The rule

Name every branch `<type>/<stub>`.

- The stub is lowercase letters, digits and hyphens.
- Where a plan or scope exists, the stub matches its stub. Plan `phase4-descope` works on a branch ending in `/phase4-descope`.

## Types

| Prefix | Use for |
|---|---|
| `feat/<stub>` | Features |
| `doc/<stub>` | Documentation |
| `fix/<stub>` | Fixes for bugs, security issues and similar |
| `harness/<stub>` | Agent harness changes: plans, drafts, loop scripts, hooks |
| `refactor/<stub>` | Restructuring or descoping existing work, with no new features |

## One plan, one branch

- All tasks of one plan stay on one branch. `approve.sh` and `mark-done.sh` expect the whole plan in one place.
- Pick the prefix from most of the plan's work. A harness plan with one docs task stays on `harness/<stub>`.

## Examples

| Branch | Why |
|---|---|
| `harness/scope-template-check` | Plan `scope-template-check`. Mostly harness work, with one docs task. |
| `refactor/phase4-descope` | Plan `phase4-descope`. Cuts Phase 4 back to the container. |
| `doc/branch-naming` | Adds this file. No plan stub. |
