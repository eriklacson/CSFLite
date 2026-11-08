# AGENTS.md

This file provides guidance to coding agents working with code in this repository. It is tool-neutral. `CLAUDE.md` imports it for Claude Code.

## Commands

```bash
# Install dependencies
poetry install --with dev

# Run all tests
poetry run pytest

# Run a specific test file or test
poetry run pytest tests/test_assess_helpers.py
poetry run pytest tests/test_assess_helpers.py::test_function_name

# Format code (line-length: 120)
poetry run black .
poetry run black --check .  # check without modifying

# Lint
poetry run ruff check .

# Security scan (HIGH severity only)
poetry run bandit -r . -x .venv,venv,build,dist,docs,migrations --severity-level high

# Install pre-commit hooks (required before first commit)
poetry run pre-commit install
```

CI runs Black → Ruff → Bandit → pytest in sequence on Python 3.12. pytest runs with `--maxfail=1` (stops at first failure). Ruff selects rules `E, F, B, I, S, PT` (S = security lints, PT = pytest style); `E501` is ignored. Bandit skips `B101` (assert statements).

## Architecture

CSFLite is a lean NIST CSF v2.0 security assessment and governance framework for startups and SMEs. It measures control **coverage** (existence), not maturity. It operates on a curated set of **25 CSF subcategories** (`data/csf_lookup.csv`).

**Governance Assessment (manual)**
- User fills in `templates/governance_checks_template.csv` with Yes/Partial/No responses
- `tools/governance_check.py` orchestrates the pipeline
- Scoring in `tools/assess_helpers.py`: response (Yes=1, Partial=0.5, No=0) × subcategory weight → gap score
- Outputs: `governance_assessment.csv`, `governance_heatmap.csv`

### Key modules

| File | Role |
|------|------|
| `tools/assess_helpers.py` | Core scoring and heatmap logic for governance assessment |
| `tools/governance_check.py` | CLI entry point for governance assessment |
| `tools/global_helpers.py` | Path resolution, CSV/JSON I/O utilities |
| `config/path_config.json` | Centralized paths for all inputs/outputs |
| `data/csf_lookup.csv` | The single source of truth for the 25 CSFLite subcategories — function, display name, question, evidence prompt, weight, recommendation, and the full CSWP 29 outcome text (`csf_outcome`) |

### Test structure

Tests in `tests/` mirror `tools/`. Test data is built inline and written to pytest's `tmp_path`, except
`tests/test_golden_pipeline.py`, which replays `tests/fixtures/golden/` — recorded CLI output that gates
the Phase 4 web rewrite. A failure there means scoring behaviour changed.

### Crosswalk supplements

`templates/soc2-supplement-questionnaire.csv` is a delivered SOC 2 crosswalk supplement (28 questions covering 5 gap domains outside the core 25).

`templates/hipaa-supplement-questionnaire.csv` is a delivered HIPAA crosswalk supplement (exactly 9 questions covering gap domains outside the CSFLite 25; scoped for Business Associates). The full HIPAA deliverable set lives in `docs/hipaa/`: crosswalk, gap analysis template, and executive summary template. Spec source: `docs/specs/csflite-spec-brief.md`.

Both move into the web app in Phase 5 as collected, unscored tracks (`docs/specs/design/phase-4-web-interface.md` §16) — answers persist and export, but no coverage score is computed for them.

### Phase 4 — web interface (in progress)

The CLI in this section is being replaced. Scope: `docs/specs/phase-4/web-interface-scope.md`. Full design: `docs/specs/design/phase-4-web-interface.md`. `assess_helpers.py` carries over unchanged; everything else in this Architecture section is rewritten once Phase 4 ships.

Before changing Phase 4 code, read `docs/specs/standards.md` (the rules) and `docs/specs/standards-gaps.md` (what is not decided yet). Do not invent a rule for an open gap. Raise it with the architect.

### Doc templates

`docs/specs/templates/` holds blank templates (`architecture`, `schema`, `routes`, `integrations`, `standards`). Use them as the structure when writing repo-specific architecture docs for CSFLite. Fill them for this repo's context. Tenancy is a later phase, not Phase 4, so mark tenant rows `n/a` rather than inventing them. ADR-0009 and `schema.md` still describe tenant-ready tables; see `docs/specs/standards-gaps.md` G-1.

### Records

- `docs/specs/adr/` — decisions and why they were made (`ADR-NNNN-*.md`)
- `docs/specs/checks/` — what a review run found (`CHK-NNNN-*.md`)

## Known Issues

Tracked in the Known Technical Debt table in `docs/development_roadmap.md` (TD-1, TD-2, TD-3). Add new debt there, not here.

## Execution Loop (jig)

CSFLite follows the jig process. `VOCABULARY.md` defines the terms. `harness/rules.md` holds the process rules. jig's enforcement scripts are not built yet, so treat these rules as guidance until they are. The tool settings in `.claude/settings.json` block the Edit and Write tools on `harness/plans/`, but nothing blocks a shell command from writing there, and the approval hash that would catch it is not built. No setting enforces the rest of the list below.

Every piece of work goes through six stages, no exceptions.

| Stage | What happens | Who decides it is done |
|---|---|---|
| READ | Read the spec brief (`docs/specs/csflite-spec-brief.md`), the files in `docs/specs/` that apply, and existing ADRs in `docs/specs/adr/`. | You |
| PLAN | Draft the plan in `harness/drafts/<stub>.plan.md`, with `<stub>.check.sh` and `<stub>.gate.yaml` beside it. Use Plan Mode if your tool has it. | You draft it |
| APPROVE | The architect approves the plan, moves the files into `harness/plans/`, and records significant decisions as ADRs. | The architect |
| IMPLEMENT | Work through the tasks in order. | The checks |
| VERIFY | Run each task's check and report its real output. Also validate control IDs against `data/csf_lookup.csv`, check acceptance criteria, run tests, and have the work checked independently (a second agent or a person). | The checks, then a second reviewer |
| REPORT | Present the output and the verification results. Flag unresolved items honestly. | The architect |

Never skip PLAN. Never start IMPLEMENT before the architect approves the plan.

### Tasks

- A task is done only when its check passes. Your own judgment does not count.
- Write the task's tests first and run them. They must fail. They are then locked.
- If a question is not answered by the files, stop and write `STUCK` and the question. Do not guess.
- If a task reaches its round limit, stop and report how far you got.
- Report the check's real output, not a summary of it.

### What you must never change

- Anything in `harness/plans/`. Only `mark-done.sh` changes a plan's status column. You edit drafts only.
- Any check or check result.
- A test after its hash is taken.
- The log, except through the harness scripts.
- `VOCABULARY.md`.
- Files in `docs/` unless the approved plan lists them. Most CSFLite work is docs, so the plan is what grants this.

### Where the rules come from

- Process rules: `harness/rules.md`.
- Software rules: `docs/specs/standards.md`. CSFLite uses no jig ruleset. Anything a ruleset would add is added to `standards.md`, with the architect's approval. Where jig files mention a ruleset, read it as `standards.md`.
- Do not invent a rule for an open gap in `docs/specs/standards-gaps.md`. Raise it with the architect.

### How jig terms map to CSFLite files

| jig term | CSFLite file |
|---|---|
| spec | `docs/specs/csflite-spec-brief.md` |
| build records | `docs/specs/architecture.md`, `schema.md`, `standards.md` (`routes.md` and `integrations.md` are not written yet) |
| record templates | `docs/specs/templates/` |
| decision records | `docs/specs/adr/` |
| audit records | `docs/specs/checks/` |
| scopes | `docs/scopes/` (Phase 4 summary today: `docs/specs/phase-4/web-interface-scope.md`) |
| plans, checks, logs | `harness/drafts/`, then `harness/plans/` |

Existing files keep their names. ADRs stay `ADR-NNNN-*.md`, not jig's `NNNN-*.decision.md`. Process rule P-10 (file names) applies only to new process files: scopes, plans, checks, gates and logs. Existing files under `docs/specs/` are exempt.

### Never

- Never write a secret value into any file.
- Never build anything the scope does not ask for.
