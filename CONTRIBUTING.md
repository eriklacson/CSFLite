# Contributing to CSFLite

Thank you for your interest in CSFLite. This document explains how to contribute effectively.

CSFLite is a lean cybersecurity framework for startups and SMEs. Contributions should preserve this intent: startup-first, governance-driven, actionable over aspirational, compliance as output not driver. If you haven't already, read the [Assessment Philosophy](docs/csflite-assessment-philosophy.md) before contributing — it governs all design decisions.

---

## Project Status

CSFLite is in **alpha** (v0.1.0-alpha). The governance assessment pipeline is functional. Nuclei scan integration is in preview. Expect breaking changes to data formats, CLI interfaces, and scoring methodology.

We welcome contributions but ask that you open an issue to discuss significant changes before investing time in a pull request.

---

## ⚠️ Mapping System Transition

CSFLite is migrating from direct template ID lookups to a more flexible YAML-based tag mapping system.

### Current State (v0.1.0-alpha)

The scan-to-CSF mapping uses **direct template ID matching** from `data/nuclei_csf_lookup.csv`:

```python
# Current: tools/assess_helpers.py
def map_scan_to_csf(scan_results, lookup_csv_path):
    lookup_df = pd.read_csv(lookup_csv_path)
    # Match exact templateID
    match = lookup_df[lookup_df["templateID"] == template_id]
```

### Future State (v0.2.0+)

The new system will use **tag-based heuristics** from `data/mapping_rules.yaml`, allowing fuzzy matching when exact template IDs aren't in the lookup table.

**Example YAML rule:**
```yaml
rules:
  - tags: [ssl, tls, certificate]
    subcategory_id: PR.DS-02
    confidence: high
```

This enables automatic mapping of new Nuclei templates without manual CSV updates.

### For Contributors

**⚠️ HOLD: Do NOT contribute new mappings to CSV/JSON files.**

The current CSV-based direct matching will be replaced by YAML tag-based rules in v0.2.0. 

**If you need to add mappings now:**
1. Open an issue describing the template(s) and proposed CSF mapping
2. Wait for maintainer guidance on whether to add to CSV (short-term) or YAML (future-proof)

**Why the freeze?**
- Prevents duplicate work when YAML system launches
- Ensures new mappings follow the tag-based philosophy
- Reduces merge conflicts during the transition

**Migration timeline:**
- v0.1.0-alpha: CSV/JSON (current — **no new contributions accepted**)
- v0.2.0-alpha: YAML parallel implementation (feature branch)
- v0.3.0-alpha: YAML becomes primary, CSV deprecated but still supported
- v1.0.0: CSV/JSON fully removed

---

## Getting Started

### Prerequisites

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.12+ | Runtime |
| Poetry | Latest | Dependency management |
| Git | Any | Version control |

### Setup

```bash
git clone https://github.com/eriklacson/CSFLite.git
cd CSFLite
poetry install --with dev
poetry run pre-commit install
```

### Verify

```bash
poetry run pytest
poetry run black --check .
poetry run ruff check .
```

---

## Contribution Workflow

1. **Fork the repository** on GitHub
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b fix/issue-123
   # or
   git checkout -b feat/nuclei-yaml-rules
   ```
3. **Make your changes** following the development standards below
4. **Run all checks locally:**
   ```bash
   poetry run black .
   poetry run ruff check .
   poetry run bandit -r tools --severity-level high
   poetry run pytest
   ```
5. **Commit with conventional format** (see Commit Messages section)
6. **Push and open a PR** against `main`
7. **Expect feedback within 3-5 business days**

---

## Development Standards

### Code Style

CSFLite uses automated formatting and linting. Don't fight the tools — let them handle style so reviews can focus on substance.

| Tool | Config | Purpose |
|------|--------|---------|
| **Black** | `line-length = 120`, `target-version = py312` | Code formatting |
| **Ruff** | Rules: `E, F, B, I, S, PT` | Linting, import sorting, security, pytest style |
| **Bandit** | HIGH severity only | Security scanning |
| **pytest** | `tests/` directory, `-q --maxfail=1` | Unit tests |

Pre-commit hooks enforce all of these on every commit. If a hook fails, fix the issue before committing — don't bypass hooks with `--no-verify`.

### Line Length

120 characters. Configured in both Black and Ruff. No exceptions.

### Imports

Ruff handles import sorting (`I` rule). Don't manually organize imports.

### Type Hints

Use type hints for function signatures. Not enforced by CI yet, but expected for new code.

### Docstrings

All public functions need docstrings. Use imperative mood: "Read the CSF lookup file" not "Reads the CSF lookup file."

### Tests

Every new function in `tools/` needs a corresponding test in `tests/`. Follow existing patterns:

```python
# tests/test_<module>.py

def test_<function>_<scenario>():
    """Test that <specific behavior> works correctly."""
    # arrange
    input_data = ...
    
    # act
    result = function_under_test(input_data)
    
    # assert
    assert result == expected_value
```

Use `pytest` fixtures and `unittest.mock.patch` for external dependencies (file I/O, subprocess calls). See `tests/test_nuclei_helpers.py` for examples of mocking subprocess and filesystem operations.

**Running tests:**

```bash
# Run all tests
poetry run pytest

# Run a specific test file
poetry run pytest tests/test_assess_helpers.py

# Run a specific test function
poetry run pytest tests/test_assess_helpers.py::test_map_scan_to_csf_valid

# Run with verbose output
poetry run pytest -v
```

### Integration Tests

Integration tests go in `tests/integration/`. They test the full pipeline:

```python
def test_governance_to_heatmap_pipeline():
    """Verify governance CSV → scored output → heatmap generation."""
    # Load sample governance responses from fixtures
    # Run assessment tool
    # Assert heatmap severity thresholds are correct
```

Use `tests/fixtures/` for sample data files.

**Note:** Integration tests for the scan pipeline are pending (Phase 5). See roadmap for status.

---

## Project Structure

```
CSFLite/
├── tools/           # Python source — CLI tools and helper modules
├── tests/           # pytest unit tests (mirrors tools/ structure)
│   ├── fixtures/    # Sample data for tests
│   └── integration/ # End-to-end pipeline tests
├── data/            # Reference data — CSF lookups, mappings, scan profiles
├── templates/       # User-facing input templates (governance questionnaire)
├── config/          # Runtime configuration (path_config.json)
├── docs/            # Documentation
│   └── reference/   # Framework reference docs (subcategories, mappings, remediation)
├── scans/           # Generated scan outputs (gitignored)
├── output/          # Generated assessment outputs (gitignored)
└── .github/         # CI workflows
```

### Key files

| File | Role | Change carefully | Status |
|------|------|-----------------|--------|
| `data/csf_lookup.csv` | Subcategory weights and recommendations | Yes — affects all scoring | Stable |
| `data/nuclei_csf_lookup.csv` | Template-to-CSF mapping (current) | Yes — affects scan mapping | **⚠️ Deprecated — YAML migration in progress** |
| `data/nuclei_csf_lookup.json` | JSON version of template mappings | Yes — reference only | **⚠️ Deprecated — YAML migration in progress** |
| `data/mapping_rules.yaml` | Tag-based mapping rules (future) | N/A — not yet merged | **🚧 Preview — see feature branch** |
| `data/heat_map_lookup.csv` | Heatmap severity thresholds | Yes — affects visual output | Stable |
| `data/profiles.yaml` | Nuclei scan profiles | Yes — affects scan execution | Stable |
| `templates/governance_checks_template.csv` | Governance questionnaire | Yes — changes user-facing assessment | Stable |
| `config/path_config.json` | Centralized path configuration | Yes — breaks tools if misconfigured | Stable |
| `docs/csflite-assessment-philosophy.md` | Authoritative methodology document | Requires maintainer approval | Stable |

---

## Known Issues (Don't Fix These Yet)

Before you open a PR, check if it's already tracked as technical debt:

- **`assess.py` is marked for deprecation** — Awaiting refactor (see roadmap Phase 5)
- **`path_config.json` uses `../` relative paths** — Breaks on non-standard CWD
- **CI Bandit target is placeholder `your_package`** — Not scanning actual CSFLite code
- **CI Python version (3.10) doesn't match project requirement (3.12+)** — Tests may pass in CI but fail locally
- **`scan_input_json` key referenced in `assess.py` but missing from `path_config.json`** — Will cause runtime error
- **Nuclei mapping uses CSV instead of YAML** — Feature branch exists; merge blocked until Phase 5 testing complete

See `docs/development_roadmap.md` for full technical debt list and resolution timeline.

---

## What to Contribute

### High-Value Contributions

These are the most impactful things you can contribute right now:

**Bug Fixes** — Especially in the scan pipeline (`tools/assess.py`, `tools/nuclei_json_converter.py`), which hasn't been pilot-tested end-to-end yet.

**Test Coverage** — Integration tests covering the full pipeline (scan JSON → mapped CSV → heatmap) are missing entirely. This is the highest-priority gap.

**Scan Profile Contributions** — Industry-specific or environment-specific Nuclei scan profiles in `data/profiles.yaml`. For example: profiles optimized for SaaS applications, healthcare environments, or financial services infrastructure.

**Documentation Fixes** — Broken links, inaccurate CLI examples, outdated file references, typos in docstrings.

### Welcome Contributions

**Compliance Crosswalks** — Mappings between CSFLite subcategories and other frameworks (SOC 2, HIPAA, ISO 27001). These should be added as reference documents in `docs/reference/`.

**Output Format Additions** — Markdown reports, HTML dashboards, or other report formats generated from assessment data.

**Remediation Guidance Improvements** — More specific, actionable remediation steps in `docs/reference/manual_remediation.md`, especially for cloud-native or container environments.

### Requires Discussion First

Open an issue before working on these — they affect framework integrity:

**Subcategory Changes** — Adding, removing, or reweighting subcategories in `data/csf_lookup.csv`. Every subcategory in CSFLite was selected against specific criteria documented in `docs/reference/top_25_sub_categories.md`. Proposals must include rationale aligned with these criteria.

**Scoring Methodology Changes** — Modifications to the weighted scoring, gap calculation, or heatmap severity thresholds in `tools/assess_helpers.py`.

**Assessment Philosophy Changes** — Any change that contradicts `docs/csflite-assessment-philosophy.md` will be rejected. If you believe the philosophy should evolve, open a discussion issue first.

**Nuclei Template Mappings** — Currently frozen due to YAML migration. See "Mapping System Transition" section above.

---

## Proposing Subcategory Changes

CSFLite deliberately limits scope to 25 subcategories. This is a design constraint, not a gap.

### To Propose Adding a Subcategory

Open an issue with:

1. The exact NIST CSF v2.0 subcategory ID and name (from NIST CSWP 29)
2. Which existing subcategory it should replace (we maintain 25, not 25+N)
3. Why it has a higher impact-to-effort ratio for SMEs than the one it replaces
4. Whether it's automatable, manual, or both
5. A draft governance question and evidence requirements

### To Propose Reweighting

Open an issue with:

1. The subcategory ID
2. Current weight (from `data/csf_lookup.csv`)
3. Proposed weight
4. Evidence or reasoning for the change (threat landscape data, incident statistics, practitioner experience)

---

## Pull Request Process

### Before Submitting

1. **Branch from `main`** — Use a descriptive branch name: `fix/nuclei-mapping-ssl`, `feat/soc2-crosswalk`, `docs/fix-getting-started-links`
2. **Run all checks locally:**
   ```bash
   poetry run black .
   poetry run ruff check .
   poetry run bandit -r tools --severity-level high
   poetry run pytest
   ```
3. **Write or update tests** for any code changes
4. **Update documentation** if your change affects user-facing behavior

### PR Description

Include:

- **What** the change does (one sentence summary)
- **Why** it's needed (link to issue if applicable)
- **How** to verify it works (test commands, expected output)
- **What breaks** if this is wrong (impact assessment)

### Review Criteria

PRs are evaluated on:

1. **Correctness** — Does it work? Do tests pass?
2. **Alignment** — Does it preserve CSFLite's philosophy (coverage-first, lean, startup-focused)?
3. **NIST Accuracy** — Are CSF subcategory IDs, names, and function assignments correct per NIST CSWP 29?
4. **Test coverage** — Is new code tested? Are edge cases covered?
5. **Simplicity** — Is this the simplest way to solve the problem? Enterprise complexity is a bug, not a feature.

### What Will Get Your PR Rejected

- Changes that add maturity scoring, risk quantification, or compliance certification language (contradicts assessment philosophy)
- Subcategory additions without removing one (we stay at 25)
- New CSV/JSON mappings without prior discussion (migration freeze)
- Code without tests
- Style violations (let the pre-commit hooks catch these before you push)

---

## Commit Messages

Use conventional format:

```
type: short description

Longer explanation if needed.

Refs #issue-number
```

**Types:** `fix`, `feat`, `docs`, `test`, `refactor`, `chore`

**Examples:**
```
fix: correct PR.DS-02 weight in csf_lookup.csv

The weight was incorrectly set to 3, should be 4 based on
the Top 25 selection criteria.

Refs #42
```

```
feat: add SOC 2 compliance crosswalk document

Maps all 25 CSFLite subcategories to SOC 2 Trust Service
Criteria with rationale for each mapping.

Refs #58
```

```
docs: fix broken links in GETTING_STARTED.md

All relative paths now resolve correctly from docs/ subdirectory.
```

```
test: add integration test for governance heatmap scoring

Verifies the full pipeline from CSV input through weighted
scoring to heatmap severity classification.
```

---

## Reporting Issues

### Bug Reports

Include:

- Python version (`python --version`)
- Poetry version (`poetry --version`)
- OS and version
- Steps to reproduce
- Expected vs. actual behavior
- Relevant error output (full traceback)

### Feature Requests

Include:

- What you're trying to accomplish (the goal, not the implementation)
- Why existing functionality doesn't solve it
- How it aligns with CSFLite's philosophy (startup-first, lean, governance-driven)
- Whether you're willing to implement it yourself

---

## Code of Conduct

Be professional. Be constructive. Assume good intent. Disagree on ideas, not people.

This is a security framework project — accuracy and rigor matter more than speed. Take the time to validate your work against canonical sources (NIST CSWP 29, Nuclei template documentation, etc.).

We value diverse perspectives and welcome contributors of all backgrounds and experience levels. If you're new to open source or security frameworks, ask questions. The maintainers are here to help.

---

## Questions?

Open a GitHub issue with the `question` label. There's no Slack, Discord, or mailing list yet — the project is too early for that overhead.

For security vulnerabilities, email the maintainer directly (see GitHub profile) rather than opening a public issue.

---

*Last updated: 2026-02-10*
