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
- [x] Build `data/nuclei_csf_lookup.json` — Nuclei template → CSF subcategory mapping
- [x] Build `data/nuclei_csf_lookup.csv` — CSV version for scan-to-CSF mapping engine
- [x] Build `data/heat_map_lookup.csv` — Heatmap severity thresholds
- [x] Build `data/profiles.yaml` — Nuclei scan profiles (baseline_web, baseline_network, baseline_cloud, comprehensive)
- [x] Document Nuclei-to-CSF mapping rationale (`docs/reference/nuclei_to_csf_mapping.md`)

**Key artifacts:**
- `data/csf_lookup.csv` — Weights, recommendations, subcategory metadata
- `data/nuclei_csf_lookup.json` — Template ID → subcategory mapping
- `data/profiles.yaml` — Scan profile definitions
- `docs/reference/nuclei_to_csf_mapping.md` — Mapping rationale with remediation guidance

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
- [ ] Validate `nuclei_csf_lookup.csv` mappings against real Nuclei template IDs (confirm no stale/renamed IDs)

**Acceptance criteria:**
- A user can follow the Getting Started guide from clone to final report without errors
- Governance assessment produces correct scores for known inputs
- Scan pipeline produces correct CSF mappings for known Nuclei output
- All example outputs are committed and reviewable

**Blocked by:** Access to a test environment with known-state targets for reproducible scan results.

---

## ⬚ Phase 6: Release Hardening

**Goal:** Polish the project for public consumption as `v0.1.0`.

**Deliverables:**
- [ ] Write `CONTRIBUTING.md`
- [ ] Add GitHub issue templates (bug report, feature request)

**Acceptance criteria:**
- `poetry install && poetry run pytest` passes on a clean clone
- CI pipeline passes on push to master
- All documentation links resolve
- No placeholder values in configuration files

---

## ⬚ Phase 7: Community & Iteration

**Goal:** Open the project for external contributions and expand coverage.

**Deliverables:**
- [ ] Publish `CONTRIBUTING.md` with contribution guidelines
- [ ] Add GitHub issue templates
- [ ] Create discussion templates for subcategory nominations and mapping proposals
- [ ] Expand Nuclei template mappings beyond initial set (target: 50+ templates)
- [ ] Add compliance crosswalk documents (HIPAA, SOC 2, ISO 27001)
- [ ] Add support for additional output formats (Markdown report, HTML dashboard)
- [ ] Explore JSONL streaming support for large scan outputs
- [ ] Community-submitted scan profiles for industry-specific environments

---

*Last updated: 2026-02-06*
