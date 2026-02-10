# CSFLite Development Roadmap

This roadmap tracks the phased development of CSFLite from framework definition through validated automation tooling and community release. Each phase lists concrete deliverables with completion status.

CSFLite follows a governance-first development sequence: define the framework, validate it manually, then layer in automation. This mirrors the assessment philosophy — coverage before depth.

---

## Progress Summary

| Phase | Name | Status |
|-------|------|--------|
| 1 | Framework Foundation | ✅ Complete |
| 2 | Reference Data & Mappings | ✅ Complete |
| 3 | Governance Assessment Pipeline | ✅ Complete |
| 4 | Scan Tooling Infrastructure | ✅ Complete |
| 5 | Integration & Pilot Testing | 🚧 In Progress |
| 6 | Release Hardening | ⬚ Not Started |
| 7 | Community & Iteration | ⬚ Not Started |

---

## ✅ Phase 1: Framework Foundation

**Goal:** Define what CSFLite assesses and why.

**Deliverables:**
- [x] Select Top 25 CSF subcategories with documented selection criteria
- [x] Classify each subcategory as Full / Partial / Manual automation level
- [x] Validate subcategory IDs against NIST CSWP 29 (CSF 2.0, February 2024)
- [x] Document assessment philosophy (`csflite-assessment-philosophy.md`)
- [x] Document subcategory rationale (`docs/reference/top_25_sub_categories.md`)
- [x] Document automation classification (`docs/reference/automatable_subcategories.md`)

**Key artifacts:**
- `csflite-assessment-philosophy.md` — Authoritative methodology document
- `docs/reference/top_25_sub_categories.md` — Subcategory definitions with selection rationale
- `docs/reference/automatable_subcategories.md` — Full/Partial/Manual classification per subcategory

---

## ✅ Phase 2: Reference Data & Mappings

**Goal:** Build the data layer that connects scans and questionnaires to the CSF framework.

**Deliverables:**
- [x] Build `data/csf_lookup.csv` — Subcategory reference with weights and recommendations
- [x] Build `data/nuclei_csf_lookup.json` — Nuclei template → CSF subcategory mapping (deprecated)
- [x] Build `data/nuclei_csf_lookup.csv` — CSV version for scan-to-CSF mapping engine (deprecated)
- [x] Build `data/heat_map_lookup.csv` — Heatmap severity thresholds
- [x] Build `data/profiles.yaml` — Nuclei scan profiles (baseline_web, baseline_network, baseline_cloud, comprehensive)
- [x] Document Nuclei-to-CSF mapping rationale (`docs/reference/nuclei_to_csf_mapping.md`)

**Key artifacts:**
- `data/csf_lookup.csv` — Weights, recommendations, subcategory metadata
- `data/nuclei_csf_lookup.csv` — Template ID → subcategory mapping (will be replaced by YAML)
- `data/profiles.yaml` — Scan profile definitions
- `docs/reference/nuclei_to_csf_mapping.md` — Mapping rationale with remediation guidance

**Note:** JSON/CSV mapping approach is deprecated. YAML-based tag mapping is under development on feature branch.

---

## ✅ Phase 3: Governance Assessment Pipeline

**Goal:** Deliver a complete, working governance baseline assessment from questionnaire to scored heatmap.

**Deliverables:**
- [x] Create governance questionnaire template (`templates/governance_checks_template.csv`)
- [x] Implement questionnaire processing (`tools/governance_check.py`)
- [x] Implement governance scoring engine (`tools/assess_helpers.py` — `generate_governance_assessement()`)
- [x] Implement governance heatmap generation (`tools/assess_helpers.py` — `generate_governance_heatmap()`)
- [x] Write remediation guidance for all governance gaps (`docs/reference/manual_remediation.md`)
- [x] Implement shared I/O utilities (`tools/global_helpers.py` — CSV/JSON writers, path config)
- [x] Build centralized path configuration (`config/path_config.json`)
- [x] Write unit tests for governance scoring and heatmap (`tests/test_assess_helpers.py`)
- [x] Write unit tests for I/O utilities (`tests/test_global_helpers.py`)

**Key artifacts:**
- `tools/governance_check.py` — Standalone CLI for governance assessment
- `templates/governance_checks_template.csv` — 25-item questionnaire with evidence requirements
- `docs/reference/manual_remediation.md` — Per-subcategory remediation steps

**User workflow (working end-to-end):**
```
Fill questionnaire → governance_check.py → Scored assessment CSV + Heatmap CSV
```

---

## ✅ Phase 4: Scan Tooling Infrastructure

**Goal:** Build the tooling to run Nuclei scans, convert output, and map findings to CSF subcategories.

**Deliverables:**
- [x] Implement Nuclei CLI wrapper with profile support (`tools/nuclei_scan_tool.py`)
- [x] Implement Nuclei helpers — profile loading, command building, execution (`tools/nuclei_helpers.py`)
- [x] Implement raw Nuclei JSON → CSFLite summary converter (`tools/nuclei_json_converter.py`)
- [x] Implement converter CLI (`tools/nuclei_convert_tool.py`)
- [x] Implement scan-to-CSF mapping engine (`tools/assess_helpers.py` — `map_scan_to_csf()`)
- [x] Implement scan heatmap generation (`tools/assess_helpers.py` — `generate_scan_heatmap()`)
- [x] Implement combined assessment tool (`tools/assess.py`)
- [x] Write unit tests for Nuclei helpers (`tests/test_nuclei_helpers.py`)
- [x] Write unit tests for JSON converter (`tests/test_nuclei_json_converter.py`)
- [x] Configure CI pipeline — Black, Ruff, Bandit, pytest (`.github/workflows/python-lint.yaml`)
- [x] Configure pre-commit hooks (`.pre-commit-config.yaml`)

**Key artifacts:**
- `tools/nuclei_scan_tool.py` — Profile-based Nuclei scan execution
- `tools/nuclei_convert_tool.py` — Raw scan → CSFLite format conversion
- `tools/assess.py` — Combined scan + governance assessment

**Status note:** All tools are implemented and unit-tested. The end-to-end scan pipeline has **not** been validated against live targets (see Phase 5).

---

## 🚧 Phase 5: Integration & Pilot Testing

**Goal:** Validate the complete scan-to-assessment pipeline against real targets and produce a reference report.

**Deliverables:**
- [ ] Run Nuclei scan against a controlled test environment
- [ ] Process raw scan output through `nuclei_convert_tool.py` and validate mapping accuracy
- [ ] Run combined assessment (`assess.py`) with real scan data + sample governance responses
- [ ] Validate all output formats — CSV structure, heatmap severity thresholds, score calculations
- [ ] Fix any integration issues discovered during pilot
- [ ] Generate and publish a reference assessment report in `examples/`
- [ ] Write integration test covering the full pipeline (scan JSON → mapped CSV → heatmap)
- [ ] Validate `data/nuclei_csf_lookup.csv` mappings against real Nuclei template IDs (confirm no stale/renamed IDs)
- [ ] Document pilot testing results and lessons learned
- [ ] Update GETTING_STARTED.md with validated end-to-end workflow

**Acceptance criteria:**
- A user can follow the Getting Started guide from clone to final report without errors
- Governance assessment produces correct scores for known inputs
- Scan pipeline produces correct CSF mappings for known Nuclei output
- All example outputs are committed and reviewable
- Integration tests prevent regression in core workflows

**Blocked by:** Access to a test environment with known-state targets for reproducible scan results.

**Current blocker resolution:** Setting up Docker-based test targets with intentional vulnerabilities (e.g., DVWA, WebGoat).

---

## ⬚ Phase 6: Release Hardening

**Goal:** Polish the project for public consumption as `v0.1.0`.

**Deliverables:**
- [x] Write `CONTRIBUTING.md` (completed 2026-02-10)
- [ ] Add GitHub issue templates (bug report, feature request, question)
- [ ] Add GitHub PR template with checklist
- [ ] Create GitHub Discussions categories (Q&A, Feature Proposals, Show & Tell)
- [ ] Audit all documentation for broken links and outdated references
- [ ] Verify all CLI examples in docs work on clean install
- [ ] Update CI to test against Python 3.12 (currently using 3.10)
- [ ] Fix CI Bandit scan to target `tools/` instead of placeholder `your_package`
- [ ] Resolve known technical debt (see table below)
- [ ] Tag v0.1.0 release

**Acceptance criteria:**
- `poetry install && poetry run pytest` passes on a clean clone
- CI pipeline passes on push to `main`
- All documentation links resolve
- No placeholder values in configuration files
- All known critical bugs are fixed or documented as limitations

---

## ⬚ Phase 7: Community & Iteration

**Goal:** Open the project for external contributions and expand coverage.

**Deliverables:**
- [ ] Publish v0.1.0 release on GitHub with release notes
- [ ] Create GitHub issue templates
- [ ] Create discussion templates for subcategory nominations and mapping proposals
- [ ] Merge YAML-based tag mapping system (from feature branch)
- [ ] Expand Nuclei template mappings using YAML rules (target: 50+ templates covered)
- [ ] Add compliance crosswalk documents (HIPAA, SOC 2, ISO 27001)
- [ ] Add support for additional output formats (Markdown report, HTML dashboard)
- [ ] Explore JSONL streaming support for large scan outputs
- [ ] Accept and review community-submitted scan profiles for industry-specific environments
- [ ] Publish blog post or tutorial on using CSFLite for SOC 2 preparation

**Success metrics:**
- 5+ external contributors
- 10+ GitHub stars
- 3+ community-submitted scan profiles or compliance crosswalks
- Active usage by at least 3 organizations (based on feedback/issues)

---

## Known Technical Debt

These items are not blocking release but should be addressed before v1.0.0:

| Item | Location | Impact | Resolution Plan |
|------|----------|--------|-----------------|
| `assess.py` marked for deprecation in its own docstring | `tools/assess.py` | Confusing for contributors | Refactor or remove deprecation notice by Phase 6 |
| `path_config.json` uses relative paths with `../` prefix | `config/path_config.json` | Breaks if tools are run from unexpected working directory | Switch to PROJECT_ROOT-relative paths in Phase 6 |
| `numpy` in production dependencies | `pyproject.toml` | Only used by pandas; may not need explicit dependency | Audit and remove if pandas brings it transitively |
| `pytest` in both main and dev dependency groups | `pyproject.toml` | Should only be in dev | Move to dev-only in Phase 6 |
| CI Bandit target is `your_package` (placeholder) | `.github/workflows/python-lint.yaml` | Bandit scan isn't actually running against CSFLite code | Fix to scan `tools/` in Phase 6 |
| CI Python version (3.10) doesn't match project requirement (3.12+) | `.github/workflows/python-lint.yaml` | Tests may pass on CI but fail on target runtime | Update to 3.12 in Phase 6 |
| `scan_input_json` key referenced in `assess.py` not in `path_config.json` | `tools/assess.py`, `config/path_config.json` | `assess.py` will fail on missing key | Add key to config or update assess.py in Phase 5 |
| Nuclei mapping uses CSV instead of YAML | `data/nuclei_csf_lookup.csv`, `tools/assess_helpers.py` | Feature branch exists with YAML implementation | Merge YAML branch after Phase 5 testing complete (target: v0.2.0) |
| No integration tests for scan pipeline | `tests/` | Scan-to-assessment workflow could break undetected | Add in Phase 5 as part of pilot testing |

---

## YAML Mapping Migration Timeline

The transition from CSV to YAML-based mapping is tracked separately:

| Version | Status | Description |
|---------|--------|-------------|
| v0.1.0-alpha | **Current** | CSV/JSON direct templateID matching (working but deprecated) |
| v0.2.0-alpha | **Feature branch** | YAML tag-based rules in parallel with CSV (CSV still works) |
| v0.3.0-alpha | **Planned** | YAML becomes primary, CSV deprecated but still supported as fallback |
| v1.0.0 | **Future** | CSV/JSON fully removed, YAML only |

**Feature branch:** `feature/yaml-mapping` (not yet public)

**Blocked by:** Phase 5 validation must complete before merging YAML changes to avoid compounding unknowns.

---

## Version History

| Version | Release Date | Key Changes |
|---------|--------------|-------------|
| v0.1.0-alpha | TBD | First public release — governance pipeline working, scan pipeline in preview |
| v0.2.0-alpha | TBD | YAML mapping system, scan pipeline validated |
| v1.0.0 | TBD | Production-ready with integration tests, documentation complete |

---

*Last updated: 2026-02-10*
