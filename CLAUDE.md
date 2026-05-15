# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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
poetry run bandit -r tools --severity-level high

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
| `data/csf_lookup.csv` | The 25 CSFLite subcategories with weights and recommendations |
| `data/heat_map_lookup.csv` | Same 25 subcategories with shortened display names for heatmap rendering (separate from `csf_lookup.csv`) |

### Test structure

Tests in `tests/` mirror `tools/`. Fixtures live in `tests/fixtures/`.

### Crosswalk supplements

`templates/soc2-supplement-questionnaire.csv` is a delivered SOC 2 crosswalk supplement (28 questions covering 5 gap domains outside the core 25).

`templates/hipaa-supplement-questionnaire.csv` is a delivered HIPAA crosswalk supplement (exactly 9 questions covering gap domains outside the CSFLite 25; scoped for Business Associates). The full HIPAA deliverable set lives in `docs/hipaa/`: crosswalk, gap analysis template, and executive summary template. Spec source: `claude-project/project.yaml`.

## Known Issues

- `path_config.json` uses relative `../` paths — breaks if CWD is not the project root
- CI Bandit target is a placeholder `your_package` (not scanning actual code yet)
