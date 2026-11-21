# Vocabulary

Each part of jig has one name. Use these names in every file. The last column lists old names that are no longer used anywhere except here.

## Terms

| Term | What it means | Where it lives | Old names |
|---|---|---|---|
| **SDLC** | Software development life cycle: the path software takes from idea to release. Deciding what to build, planning it, building it, checking it and shipping it. | — | — |
| **harness** | Everything around a coding agent that controls how it works: the instructions it reads, the files it works from, and the checks that judge its output. jig is an SDLC harness for coding agents. | `AGENTS.md`, `harness/`, the templates in `docs/` | user harness, generic layer |
| **spec** | What the project is for: its goal, its outcomes and the ruleset it follows. The records describe the system it covers. | `docs/<project>.spec.md` | `project.yaml`, seed document |
| **scope** | A part of the spec that is built as one piece, with its own success criteria. A spec has one or more scopes. | `docs/scopes/<stub>.scope.md` | — |
| **record** | A document describing the system. Each of the five comes as a pair: build mode (as it should be) and audit mode (as it is). | `docs/build.<record>.md` and `docs/audit.<record>.md` | design mode |
| **plan** | The tasks for one scope, in order, each with the check that proves it. The agent drafts it. A person approves it. After approval only the status column changes. | Draft: `harness/drafts/<stub>.plan.md`. Approved: `harness/plans/<stub>.plan.md` | unit plan, frozen plan |
| **task** | One step in a plan. Tasks are rows in the plan, not separate files. | A row in the plan | unit, slice, sprint |
| **check** | The command that decides whether a task is done. Exit code 0 means done. The agent cannot change it. | `harness/plans/<stub>.check.sh` | exit condition, `verify.sh` |
| **status** | Whether a task is `todo` or `done`. Only `mark-done.sh` writes it, and only after the task's check passes. | Status column in the plan | — |
| **loop** | The agent's own loop: it works through the plan's tasks in one context. A Stop hook holds it to the checks. | — | — |
| **round** | One attempt at a task: the agent changes code, then the check runs. | — | iteration |
| **log** | One entry per round. Entries are only ever added at the end. | `harness/plans/<stub>.log.jsonl` | round log |
| **tests hash** | A hash of the plan's tests, taken after they first run and fail. Every later round confirms the tests still match it, so the agent cannot weaken a test to make it pass. | `harness/plans/<stub>.tests.sha` | `tests.sha` |
| **approval hash** | A hash of the plan and its check script at approval, ignoring the status column. | `harness/plans/<stub>.approved.sha` | — |
| **STUCK / BUDGET** | Why a loop stopped early: an unanswered question, or the round limit was reached. | Recorded in the log | — |
| **gate** | Checks that cover the whole system and run every round. | `harness/plans/<stub>.gate.yaml` | part of `verify.sh` |
| **plan approval**, **release approval** | The two points where a person must say yes. | The six-stage process | judgment gate, authorization gate, approval gate |
| **ruleset** | Rules about the software being built, each tied to a check the agent cannot change. A project picks exactly one, or keeps these rules in its own standards record. No ruleset builds on another. | `rulesets/<name>/` | context (as a layer), regime |
| **process rule** | A rule about the jig process itself: how tasks, scopes and plans are written and closed. Applies to every project, whatever its ruleset. | `harness/rules.md` | — |
| **context** | Everything the agent is given to read for a piece of work. This is the field's meaning (as in "context engineering"). | — | — |
| **project** | One codebase using jig. | A repo created from jig | engagement |
| **stub** | The short name shared by every file that belongs to one thing. Scopes and plans use a two-digit number and a name, like `01-login`. | The first part of a file name | — |
| **AGENTS.md** | Instructions for any AI agent. `CLAUDE.md` only loads it. | Repo root | `CLAUDE.md` as the main instructions |

## File names

Every file the process produces is named `<stub>.<type>.<extension>`. The stub says which thing the file belongs to. The type says what kind of file it is.

| Type | Extension | Stub | Example | Folder |
|---|---|---|---|---|
| spec | `.md` | the project name | `acme-portal.spec.md` | `docs/` |
| architecture, routes, schema, integrations, standards | `.md` | `build` or `audit` | `build.routes.md` | `docs/` |
| scope | `.md` | number and name | `01-login.scope.md` | `docs/scopes/` |
| decision | `.md` | four-digit number and name | `0001-azure-hosting.decision.md` | `docs/decisions/` |
| plan | `.md` | the scope's stub | `01-login.plan.md` | `harness/drafts/`, then `harness/plans/` |
| check | `.sh` | the scope's stub | `01-login.check.sh` | same as the plan |
| gate | `.yaml` | the scope's stub | `01-login.gate.yaml` | `harness/plans/` |
| log | `.jsonl` | the scope's stub | `01-login.log.jsonl` | `harness/plans/` |
| approved, tests | `.sha` | the scope's stub | `01-login.tests.sha` | `harness/plans/` |

Rules:

- Stubs use lowercase letters, digits and hyphens.
- In a repo that already had documents, these names apply only to new process files. Existing files keep their names, and `AGENTS.md` maps them.
- A plan and every file beside it share the stub of the scope they deliver. `01-login.scope.md` → `01-login.plan.md` → `01-login.log.jsonl`.
- Templates use the stub `template`: `template.spec.md`, `template.scope.md`, `template.plan.md`, `template.routes.md`.
- Files that explain a folder keep the name `README.md`. `harness/plans/CURRENT` keeps its name.

## Words with one meaning here

- A **gate** is a set of checks that runs every round. The points where a person says yes are called approvals.
- **Context** means what the agent is given to read. Rules about the software live in a **ruleset**. Rules about the process live in `harness/rules.md`.

## How the six stages line up

| Stage in AGENTS.md | What happens | Who decides it is done |
|---|---|---|
| (before READ) | A person writes the spec, the build records and the scope. | A person |
| READ, PLAN | The agent drafts `<stub>.plan.md`, `<stub>.check.sh` and `<stub>.gate.yaml` in `harness/drafts/`. | The agent drafts them |
| APPROVE | A person approves the plan and moves the files into `harness/plans/`. | A person |
| IMPLEMENT, VERIFY | The loop works through the tasks. Each task's check decides when it is done. | The checks |
| REPORT | A person audits the rows the scope covered, compares them with the build records, and reviews the result. | A person |

## Where jig differs from common usage

| Term | Common usage | jig |
|---|---|---|
| spec | Spec-kit and Kiro write one spec per feature. Project-wide knowledge is separate (Kiro "steering", spec-kit "constitution"). | The spec covers the whole project. A scope is the per-feature part. |
| scope | In project management, scope is the whole project boundary. | A scope is one part of the spec. Its document holds what a scope statement holds: deliverables, acceptance criteria, exclusions, constraints. |
| plan | In spec-kit, the plan is the technical design. | The plan is the ordered tasks and their checks. The technical design lives in the build records. |
| loop | The Ralph loop restarts the agent with a fresh context each round. | The loop runs in one context. The Stop hook enforces the checks. |
| ruleset | Spec-kit calls the nearest thing a constitution: project principles in prose. | Every rule is tied to a check. |

Status: drafted 2026-11-08.
