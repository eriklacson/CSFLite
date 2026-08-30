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
| 4 | Web Interface | ⬚ Not Started |
| 5 | Release Hardening | ⬚ Not Started |
| 6 | Community & Iteration | ⬚ Not Started |

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

**Goal:** Build the data layer that drives the governance assessment framework.

**Deliverables:**
- [x] Build `data/csf_lookup.csv` — Subcategory reference with weights and recommendations
- [x] Build `data/heat_map_lookup.csv` — Heatmap severity thresholds

**Key artifacts:**
- `data/csf_lookup.csv` — Weights, recommendations, subcategory metadata
- `data/heat_map_lookup.csv` — Display names for heatmap rendering

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

## ⬚ Phase 4: Web Interface

**Goal:** Replace the CLI with a web application. After this phase CSFLite is not operable from a terminal.

Solution design: `docs/design/phase-4-web-interface.md`. Locked decisions: `.claude/docs/csflite-spec-brief.md` §10 and §12.

CSFLite ships as a container image the operator runs themselves. Local profile first, then a self-hosted profile on Railway. AWS, Azure, and GCP are later phases.

**Deliverables:**
- [ ] Move `pytest` to the dev dependency group only (`pyproject.toml`)
- [ ] Django application skeleton, server-rendered, no build step
- [ ] Web questionnaire form with evidence upload and notes (replaces the checklist CSV)
- [ ] Web-rendered report and heatmap, with CSV/JSON download
- [ ] Database persistence — assessments, responses, evidence, immutable result snapshots
- [ ] Container image and local `docker compose` profile
- [ ] Railway deployment profile — Postgres addon, mounted volume, always-on
- [ ] Operator password guard — refuse to bind a non-loopback address without `CSFLITE_PASSWORD`
- [ ] CSV import for assessments already completed with the CLI
- [ ] Retire `governance_check.py` and `config/path_config.json`

**Acceptance criteria:**
- An assessment can be completed end to end in the browser
- Web output is byte-identical to `tests/fixtures/golden/` for the same responses
- `assess_helpers.py` is unchanged, verified by diff
- The container starts from `docker compose up` with no host Python
- A past assessment's result does not change when `csf_lookup.csv` is reweighted

---

## ⬚ Phase 5: Release Hardening

**Goal:** Polish the project for public consumption as `v0.1.0`.

**Deliverables:**
- [x] Write `CONTRIBUTING.md` (completed 2026-02-10)
- [ ] Add GitHub issue templates (bug report, feature request, question)
- [ ] Add GitHub PR template with checklist
- [ ] Create GitHub Discussions categories (Q&A, Feature Proposals, Show & Tell)
- [ ] Audit all documentation for broken links and outdated references
- [ ] Verify all documented workflows work on a clean install
- [ ] Resolve known technical debt (see table below)
- [ ] Tag v0.1.0 release

**Acceptance criteria:**
- `poetry install && poetry run pytest` passes on a clean clone
- CI pipeline passes on push to `main`
- All documentation links resolve
- No placeholder values in configuration files
- All known critical bugs are fixed or documented as limitations

---

## ⬚ Phase 6: Community & Iteration

**Goal:** Open the project for external contributions and expand coverage.

**Deliverables:**
- [ ] Publish v0.1.0 release on GitHub with release notes
- [ ] Create GitHub issue templates
- [ ] Create discussion templates for subcategory nominations and mapping proposals
- [x] Add SOC 2 compliance crosswalk and readiness assessment deliverables (crosswalk, supplement questionnaire, gap analysis template, executive summary — completed 2026-03-26)
- [x] Add HIPAA compliance crosswalk and readiness assessment deliverables (crosswalk, 9-question supplement questionnaire, gap analysis template, executive summary — completed 2026-03-30; scoped for Business Associates serving US healthcare Covered Entities)
- [x] Add SP 800-53 Rev 5 compliance crosswalk as a framework reference document mapping all 25 CSFLite subcategories to SP 800-53 Rev 5 controls with assessment methods from SP 800-53A Rev 5 (completed 2026-04-09)
- [ ] Add compliance crosswalk documents (ISO 27001)
- [ ] Add support for additional output formats (Markdown report, HTML dashboard)
- [ ] Publish blog post or tutorial on using CSFLite for SOC 2 preparation

**Success metrics:**
- 5+ external contributors
- 10+ GitHub stars
- 3+ community-submitted compliance crosswalks
- Active usage by at least 3 organizations (based on feedback/issues)

---

## Known Technical Debt

These items are not blocking release but should be addressed before v1.0.0:

| Item | Location | Impact | Resolution Plan |
|------|----------|--------|-----------------|
| `pytest` in both main and dev dependency groups | `pyproject.toml` | Should only be in dev | Move to dev-only in Phase 4 |

---

## Version History

| Version | Release Date | Key Changes |
|---------|--------------|-------------|
| v0.1.0-alpha | TBD | First public release — governance pipeline working |
| v1.0.0 | TBD | Production-ready with integration tests, documentation complete |

---

*Last updated: 2026-08-30*
