# Contributing to CSFLite

Thank you for your interest in CSFLite. This document explains how to contribute effectively.

CSFLite is a lean cybersecurity framework for startups and SMEs. Contributions should preserve this intent: startup-first, governance-driven, actionable over aspirational, compliance as output not driver. If you haven't already, read the [Assessment Philosophy](docs/csflite-assessment-philosophy.md) before contributing — it governs all design decisions.

---

## Project Status

CSFLite is in **alpha** (v0.1.0-alpha). The governance assessment pipeline is functional. Nuclei scan integration is in preview. Expect breaking changes to data formats, CLI interfaces, and scoring methodology.

We welcome contributions but ask that you open an issue to discuss significant changes before investing time in a pull request.

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
    """<what the test verifies>."""
    # arrange
    # act
    # assert
```

Use `pytest` fixtures and `unittest.mock.patch` for external dependencies (file I/O, subprocess calls). See `tests/test_nuclei_helpers.py` for examples of mocking subprocess and filesystem operations.

Run tests before submitting:

```bash
poetry run pytest
```

---

## Project Structure

```
CSFLite/
├── tools/           # Python source — CLI tools and helper modules
├── tests/           # pytest unit tests (mirrors tools/ structure)
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

| File | Role | Change carefully |
|------|------|-----------------|
| `data/csf_lookup.csv` | Subcategory weights and recommendations | Yes — affects all scoring |
| `data/nuclei_csf_lookup.json` | Template-to-CSF mapping | Yes — affects scan mapping accuracy |
| `data/mapping_rules.yaml` | Tag-based mapping rules | Yes — affects automated classification |
| `templates/governance_checks_template.csv` | Governance questionnaire | Yes — changes user-facing assessment |
| `config/path_config.json` | Centralized path configuration | Yes — breaks tools if misconfigured |
| `csflite-assessment-philosophy.md` | Authoritative methodology document | Requires maintainer approval |

---

## What to Contribute

### High-Value Contributions

These are the most impactful things you can contribute right now:

**Nuclei Template Mappings** — The current `data/nuclei_csf_lookup.json` covers a small set of templates. Adding validated mappings for additional Nuclei templates directly improves scan coverage. See the "Adding Nuclei Mappings" section below.

**Scan Profile Contributions** — Industry-specific or environment-specific Nuclei scan profiles in `data/profiles.yaml`. For example: profiles optimized for SaaS applications, healthcare environments, or financial services infrastructure.

**Bug Fixes** — Especially in the scan pipeline (`tools/assess.py`, `tools/nuclei_json_converter.py`), which hasn't been pilot-tested end-to-end yet.

**Test Coverage** — Integration tests covering the full pipeline (scan JSON → mapped CSV → heatmap) are missing entirely.

**Documentation Fixes** — Broken links, inaccurate CLI examples, outdated file references.

### Welcome Contributions

**Compliance Crosswalks** — Mappings between CSFLite subcategories and other frameworks (SOC 2, HIPAA, ISO 27001). These should be added as reference documents in `docs/reference/`.

**Output Format Additions** — Markdown reports, HTML dashboards, or other report formats generated from assessment data.

**Remediation Guidance Improvements** — More specific, actionable remediation steps in `docs/reference/manual_remediation.md`, especially for cloud-native or container environments.

### Requires Discussion First

Open an issue before working on these — they affect framework integrity:

**Subcategory Changes** — Adding, removing, or reweighting subcategories in `data/csf_lookup.csv`. Every subcategory in CSFLite was selected against specific criteria documented in `docs/reference/top_25_sub_categories.md`. Proposals must include rationale aligned with these criteria.

**Scoring Methodology Changes** — Modifications to the weighted scoring, gap calculation, or heatmap severity thresholds in `tools/assess_helpers.py`.

**Assessment Philosophy Changes** — Any change that contradicts `csflite-assessment-philosophy.md` will be rejected. If you believe the philosophy should evolve, open a discussion issue.

---

## Adding Nuclei Mappings

This is the most common and most needed contribution type.

### Structure

Mappings live in `data/nuclei_csf_lookup.json`. Each entry maps a Nuclei template ID to one or more CSF subcategories:

```json
{
  "templateID": "ssl-issuer",
  "csf_function": "Protect",
  "csf_subcategory_id": "PR.DS-02",
  "csf_subcategory_name": "Data-in-transit is protected",
  "rationale": "SSL/TLS certificate validation signals transport security posture"
}
```

### Requirements for New Mappings

1. **Template ID must be exact** — Match the Nuclei template ID precisely. Run `nuclei -tl` to list available templates.
2. **Subcategory ID must be canonical** — Use IDs from `data/csf_lookup.csv`. All IDs are validated against NIST CSWP 29.
3. **Rationale must be specific** — Explain *why* this template finding maps to this subcategory. "Related to security" is not a rationale.
4. **One mapping per finding-to-subcategory relationship** — If a template maps to multiple subcategories, create separate entries.

### Validation

Before submitting, verify your mapping makes sense by asking: "If this Nuclei template fires, does it provide evidence about the existence (or absence) of the capability described by this CSF subcategory?"

If the answer is "sort of, loosely" — the mapping is probably wrong. CSFLite values defensible mappings over broad coverage.

---

## Proposing Subcategory Changes

CSFLite deliberately limits scope to 25 subcategories. This is a design constraint, not a gap.

### To Propose Adding a Subcategory

Open an issue with:

1. The exact NIST CSF v2.0 subcategory ID and name (from CSWP 29)
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

1. **Branch from `master`** — Use a descriptive branch name: `fix/nuclei-mapping-ssl`, `feat/soc2-crosswalk`, `docs/fix-getting-started-links`
2. **Run all checks locally:**
   ```bash
   poetry run black --check .
   poetry run ruff check .
   poetry run bandit -r tools --severity-level high
   poetry run pytest
   ```
3. **Write or update tests** for any code changes
4. **Update documentation** if your change affects user-facing behavior

### PR Description

Include:

- **What** the change does (one sentence)
- **Why** it's needed (link to issue if applicable)
- **How** to verify it works (test commands, expected output)
- **What breaks** if this is wrong (impact assessment)

### Review Criteria

PRs are evaluated on:

1. **Correctness** — Does it work? Do tests pass?
2. **Alignment** — Does it preserve CSFLite's philosophy (coverage-first, lean, startup-focused)?
3. **NIST Accuracy** — Are CSF subcategory IDs, names, and function assignments correct per CSWP 29?
4. **Test coverage** — Is new code tested? Are edge cases covered?
5. **Simplicity** — Is this the simplest way to solve the problem? Enterprise complexity is a bug, not a feature.

### What Will Get Your PR Rejected

- Changes that add maturity scoring, risk quantification, or compliance certification language (contradicts assessment philosophy)
- Subcategory additions without removing one (we stay at 25)
- Mappings without rationale
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

Types: `fix`, `feat`, `docs`, `test`, `refactor`, `chore`

Examples:
```
fix: correct PR.DS-02 weight in csf_lookup.csv
feat: add SOC 2 compliance crosswalk document
docs: fix broken links in GETTING_STARTED.md
test: add integration test for governance heatmap scoring
```

---

## Reporting Issues

### Bug Reports

Include:

- Python version (`python --version`)
- OS and version
- Steps to reproduce
- Expected vs. actual behavior
- Relevant error output

### Feature Requests

Include:

- What you're trying to accomplish (the goal, not the implementation)
- Why existing functionality doesn't solve it
- How it aligns with CSFLite's philosophy

---

## Code of Conduct

Be professional. Be constructive. Assume good intent. Disagree on ideas, not people.

This is a security framework project — accuracy and rigor matter more than speed. Take the time to validate your work against canonical sources.

---

## Questions?

Open a GitHub issue. There's no Slack, Discord, or mailing list yet — the project is too early for that overhead.

---

*Last updated: 2026-02-06*
