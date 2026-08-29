# LeanSecurity — CSFLite
## Project Specification Brief v2.0
**Status:** Phase 3 complete; Phase 4 (Web Interface) next  
**Last updated:** March 2026

---

## 1. Overview

CSFLite is a governance assessment framework built on 25 curated NIST CSF 2.0 subcategories. It answers: "What essential cybersecurity controls should exist, and are they present?" It measures coverage — existence — before maturity. Not a compliance framework. Positioned as the Minimum Viable Control Framework.

Crosswalk reference documents for SOC 2, HIPAA, and SP 800-53 are provided as structured starting points for external assessment readiness. Scanning and other control enforcement are handled by external projects.

### Project Components

CSFLite is a framework with three layers:

- **The 25 curated NIST CSF 2.0 subcategories** — foundational to security posture, applicable across sectors, assessable with a simple yes/no, and clearly actionable when missing. Excluded controls reflect lower relative impact, not a neglected area. The cap at 25 is a deliberate, opinionated scope constraint that keeps the framework lean and avoids the scope creep that makes larger frameworks overwhelming for target organizations.
- **An assessment methodology** — a simple questionnaire and scoring rubric.
- **An application toolkit** — automates the assessment process. Currently a CLI; becomes a web application in Phase 4 (§12).

---

## 2. Architecture Pattern

**Batch CLI, file-based**

### Layers

**Intake Layer**
Responsible for ingesting raw inputs: the governance checklist CSV filled by the assessor. Validates required fields and produces cleaned, typed records ready for scoring. Never performs scoring, weighting, or output generation.

**Scoring Layer**
Responsible for joining intake records against the CSF lookup reference data (`csf_lookup.csv`), applying weights, computing coverage scores, and classifying heatmap severity. Produces scored assessment records and heatmap records. Never reads raw input directly — only consumes validated records from the intake layer.

**Output Layer**
Responsible for serializing scored records and heatmaps as machine-readable CSV files. Never performs scoring logic. Handles path resolution via `path_config.json`.

These layer responsibilities survive the Phase 4 web rewrite unchanged. Only the intake and output mechanisms change — see §12.

### Flow

```
Governance CSV
      │
      ▼
 Intake: validate
 required fields
      │
      ▼
 Scoring: join CSF
 lookup, apply weights,
 compute coverage
      │
      ▼
   Heatmap
      │
      ▼
   Report
```

### Delivery Mode

Synchronous, batch-oriented CLI execution. Each tool runs independently against file inputs and produces file outputs. There is no event bus, queue, or streaming component.

The governance assessment pipeline works end to end.

---

## 3. Interface Contracts

All contracts are prescriptive they define what the schemas should be, not merely what they are today. Implementations that deviate from these contracts are bugs.

### Governance Checklist Input (CSV)

The questionnaire filled by the assessor. Produced by the human operator, consumed by `governance_check.py`.

| Field | Type | Required | Description |
|---|---|---|---|
| `csf_function` | `string` | Yes | CSF Function name: Govern, Identify, Protect, Detect, Respond, Recover |
| `csf_subcategory_id` | `string` | Yes | Canonical NIST CSF v2.0 subcategory ID (e.g., `GV.PO-01`, `PR.DS-02`). Must exist in `csf_lookup.csv` |
| `csf_subcategory_name` | `string` | Yes | Human-readable outcome description |
| `question` | `string` | No | Assessment question text (informational, not consumed by scoring) |
| `evidence` | `string` | No | Expected evidence types (informational, not consumed by scoring) |
| `notes` | `string` | No | Assessor notes (preserved in output, not consumed by scoring) |
| `response` | `string` | Yes | One of: `Yes`, `Partial`, `No`. Case-sensitive. |

### CSF Lookup Reference (CSV)

The authoritative reference for subcategory weights and remediation recommendations. Produced by framework maintainer, consumed by all scoring functions.

| Field | Type | Required | Description |
|---|---|---|---|
| `csf_subcategory_id` | `string` | Yes | Canonical subcategory ID. Primary key. |
| `weight` | `float` | Yes | Relative importance weight. Values: 1.0 (foundational), 1.2 (important), 1.5 (critical) |
| `recommendation` | `string` | Yes | Remediation guidance text for gaps in this subcategory |

### Governance Assessment Output (CSV)

Scored governance results. Produced by `generate_governance_assessement()`, consumed by heatmap generator and report tools.

| Field | Type | Description |
|---|---|---|
| `csf_subcategory_id` | `string` | Canonical subcategory ID |
| `csf_subcategory_name` | `string` | Human-readable outcome description |
| `response` | `string` | Original assessor response (Yes/Partial/No) |
| `score` | `float` | Normalized response: Yes=1.0, Partial=0.5, No=0.0 |
| `weight` | `float` | Subcategory weight from CSF lookup |
| `recommendation` | `string` | Remediation guidance from CSF lookup |
| `assessment_score` | `string` | Weighted score (score × weight), formatted to 2 decimal places |
| `gap_score` | `string` | Weighted gap (weight − assessment_score), formatted to 2 decimal places |

### Governance Heatmap Output (CSV)

Severity-classified gap prioritization. Produced by `generate_governance_heatmap()`, consumed by report tools and dashboards.

| Field | Type | Description |
|---|---|---|
| `csf_subcategory_id` | `string` | Canonical subcategory ID |
| `name` | `string` | Human-readable subcategory name |
| `response` | `string` | Original assessor response |
| `severity` | `string` | One of: `high` (score ≤ 0), `medium` (score < weight), `low` (score ≥ weight) |
| `gap_score` | `string` | Weighted gap, formatted to 2 decimal places |


### Path Configuration (JSON)

Centralized file path registry. Produced by framework maintainer, consumed by all CLI tools via `global_helpers.get_paths()`.

| Field | Type | Description |
|---|---|---|
| `governance_checklist` | `string` | Path to governance checklist input CSV |
| `heatmap_lookup` | `string` | Path to heatmap severity threshold CSV |
| `csf_lookup` | `string` | Path to CSF subcategory reference CSV |
| `governance_assessment_csv` | `string` | Path for governance assessment output CSV |
| `governance_heatmap_csv` | `string` | Path for governance heatmap output CSV |

### Design Rules

- All `csf_subcategory_id` values must be validated against NIST CSWP 29 before inclusion in any reference data file
- `csf_lookup.csv` is the single source of truth for subcategory weights — no tool hardcodes weights
- Response values in governance checklists must be exactly `Yes`, `Partial`, or `No` — case-sensitive, no synonyms
- All scored output fields that represent decimal values are formatted as strings with 2 decimal places (e.g., `"1.50"`)
- Path configuration uses paths relative to project root — tools resolve paths via `path_config.json`, not hardcoded paths

---

## 4. Component Registry

| Component | Source/Domain | Status |
|---|---|---|
| `governance_check.py` | Governance assessment CLI | Complete |
| `assess_helpers.py` | Shared scoring and heatmap functions | Complete |
| `global_helpers.py` | Shared I/O utilities (CSV/JSON, path config) | Complete |

---

## 5. Repository Structure

### `CSFLite`

```
CSFLite/
├── tools/                          ← Python CLI tools and helper modules
│   ├── governance_check.py         ← Governance assessment CLI (working)
│   ├── assess_helpers.py           ← Scoring engine and heatmap functions
│   └── global_helpers.py           ← Shared I/O utilities
├── tests/                          ← pytest unit tests (mirrors tools/)
│   ├── test_assess_helpers.py      ← Scoring and heatmap tests
│   └── test_global_helpers.py      ← I/O utility tests
├── data/                           ← Reference data (CSF lookups)
│   ├── csf_lookup.csv              ← Authoritative subcategory weights + recommendations
│   └── heat_map_lookup.csv         ← Heatmap severity thresholds
├── templates/                      ← User-facing input templates
│   └── governance_checks_template.csv  ← 25-item governance questionnaire
├── config/                         ← Runtime configuration
│   └── path_config.json            ← Centralized path registry
├── docs/                           ← Documentation
│   ├── csflite-assessment-philosophy.md  ← Authoritative methodology (governs all decisions)
│   ├── development_roadmap.md      ← Phased deliverables and progress
│   ├── GETTING_STARTED.md          ← Installation and first assessment
│   ├── CONTRIBUTING.md             ← Contribution guidelines
│   └── reference/                  ← Framework reference documents
│       ├── top_25_sub_categories.md
│       ├── automatable_subcategories.md
│       ├── manual_remediation.md
│       └── manual_questionnaire.md
├── input/examples/                 ← Sample input data
├── output/examples/                ← Sample output data
├── output/                         ← Generated assessment outputs (gitignored)
├── .github/workflows/              ← CI pipeline (Black, Ruff, Bandit, pytest)
├── pyproject.toml                  ← Poetry project definition
├── .pre-commit-config.yaml         ← Pre-commit hook configuration
└── README.md
```

### Boundary Rules

- `tools/` modules may import from `tools/global_helpers.py` and `tools/assess_helpers.py` — never from CLI entry points (`governance_check.py`)
- `tests/` mirrors `tools/` structure — each `tools/x.py` has a corresponding `tests/test_x.py`
- `data/` files are reference data, not generated output — they are version-controlled and change only through deliberate maintainer action
- `config/path_config.json` is the single source of truth for file paths — no tool constructs paths independently
- `docs/csflite-assessment-philosophy.md` is the authoritative methodology document — conflicts between it and any other documentation are resolved in its favor
- `templates/` contains user-facing input templates that define the assessment interface — changes here affect the client-facing assessment experience

---

## 6. Database Schema

Not applicable. CSFLite uses file-based persistence (CSV/JSON). All state is contained in input files, reference data files, and output files. There is no database, no ORM, no migrations.

Phase 4 introduces a database — see §12.

---

## 7. Hosting Stack

CSFLite runs as a local CLI tool on the operator's machine. There is no hosting infrastructure, no deployment pipeline, and no remote services.

### Infrastructure Needs

| Need | Interface/Constraint | Notes |
|------|---------------------|-------|
| Python runtime | Python 3.12+ | Required for all tools |
| Dependency management | Poetry | Manages virtualenv and packages |
| Filesystem | Read/write access to project directory | All I/O is local file-based |

### Deployment Profile — Local Development

| Need | Service | Notes |
|------|---------|-------|
| Runtime | Local Python 3.12+ via Poetry | `poetry install && poetry shell` |

Local-first because the tool is operated by the consultant on their own machine, processing client data that should not leave the local environment without explicit agreement.

---


## 8. Reference Data

### What the Scoring Engine Uses

| Field | Used for |
|---|---|
| `csf_subcategory_id` | Join key — links governance responses to the framework |
| `weight` | Multiplier for coverage scoring (assessment_score = response_score × weight) |
| `recommendation` | Populated into assessment output for each subcategory with a gap |

The scoring engine does not hardcode control IDs, weights, or scoring rules. All scoring parameters are derived from `csf_lookup.csv` at runtime. Adding, removing, or reweighting a subcategory requires only changing this file (and the corresponding governance template row).

---

## 9. Proof-of-Concept — Build Status

CSFLite is its own proof-of-concept. There is no external client for the framework itself — client engagements are separate projects that consume CSFLite.

### CSFLite Framework — Milestones

| Phase | Milestone | Status |
|---|---|---|
| 1 | Framework Foundation — 25 subcategories, assessment philosophy, reference docs | Complete |
| 2 | Reference Data & Mappings — CSF lookup, heatmap lookup | Complete |
| 3 | Governance Assessment Pipeline — questionnaire → scored output → heatmap | Complete |
| 4 | Web Interface — web questionnaire and report, replaces the CLI | Not started |
| 5 | Release Hardening — CI fixes, documentation audit, v0.1.0 tag | Not started |
| 6 | Community & Iteration — external contributions, expanded mappings | Not started |

### Current Status

Phase 3 complete. The governance assessment pipeline runs end to end as a CLI.

**Decided, not yet built:** the Phase 4 web interface, which replaces the CLI. Specified in §12.

### Configuration (current structure)

```json
{
    "governance_checklist": "scans/governance_checks.csv",
    "heatmap_lookup": "data/heat_map_lookup.csv",
    "csf_lookup": "data/csf_lookup.csv",
    "governance_assessment_csv": "output/governance_assessment.csv",
    "governance_heatmap_csv": "output/governance_heatmap.csv"
}
```

---

## 10. Key Design Decisions — Locked

These become ADRs when decomposed into the template.

| Decision | Choice | Rationale |
|---|---|---|
| Scope limited to 25 subcategories | Fixed at 25, additions require a removal | Keeps framework lean and assessable by resource-constrained teams. Broader coverage available through later-stage maturity assessments. |
| Coverage-only scoring | Yes/Partial/No (1.0/0.5/0.0) — no maturity levels | Small teams cannot defend nuanced maturity scores. Binary or near-binary answers are defensible and actionable. |
| Evidence required for "Yes" | Assertions without proof score Partial or No | Prevents attestation theater. Most critical quality control mechanism. |
| Compliance crosswalks as reference docs | Stored in `docs/reference/`, not as executable mappings | Crosswalks inform client delivery projects but are not consumed by the scoring engine. CSFLite does not claim compliance. Crosswalks now cover SOC 2, HIPAA, and SP 800-53 Rev 5. |
| Assessment philosophy as authoritative | `csflite-assessment-philosophy.md` overrides all other docs on conflicts | Single source of truth for methodology prevents drift across documentation. |
| Web interface replaces the CLI | Phase 4 rewrite — CLI is retired, not kept alongside | One front end to maintain rather than two. The scoring core (`assess_helpers.py`) is I/O-free and carries over unchanged, so the rewrite is confined to intake and output. |
| Pre-commit hooks + CI | Black, Ruff, Bandit, pytest | Enforces code quality without manual review overhead. Appropriate for solo developer workflow. |

---

## 11. What This Project Does Not Own

- **Client-specific assessment data** — CSFLite provides the framework; client projects provide the questionnaire responses and deliverables.
- **SOC 2 / HIPAA / ISO 27001 readiness assessments** — these are client delivery engagements that consume CSFLite. Compliance crosswalk reference documents live in CSFLite; readiness assessment workflows, gap analyses, and remediation roadmaps live in client projects.
- **Tool integrations (OWASP ZAP, Graylog, TheHive, DefectDojo)** — planned integrations per the development roadmap are future scope. When built, they may live in CSFLite if they are framework-generic, or in separate projects if they are deployment-specific.
- **Unified governance dashboard** — longer-horizon milestone that would require a service model. Would need its own seed document.
- **Maturity assessment, risk quantification, continuous monitoring** — explicitly out of scope by design. CSFLite is Stage 1 (coverage). Later stages are separate projects.

---

## 12. Planned — Phase 4 Web Interface

Not built. Nothing in this section is contract-binding. It records decisions made, not implementation.

The web interface **replaces** the CLI. After Phase 4, CSFLite is not operable from a terminal. `governance_check.py` is retired, and §4, §5, and the §5 Boundary Rules are rewritten at that point.

### Carries over unchanged

- The 25 curated subcategories and `csf_lookup.csv` as their single source of truth
- The scoring rules and output contracts in §3 — a web form producing the same records satisfies the same contracts
- `assess_helpers.py` — pure functions over dicts, no I/O, callable directly from a web layer

### Changes

**Intake** — web questionnaire form with evidence upload, replacing the checklist CSV. The Governance Checklist Input contract in §3 is the reference for form fields.

**Output** — web-rendered report and heatmap, plus downloadable CSV/JSON. The Governance Assessment Output and Governance Heatmap Output contracts in §3 are the reference for both.

**Persistence** — a database replaces file-based state. Tables for assessment sessions, configurations, and historical results. Single-tenant isolation.

**Hosting** — a hosted profile replaces the local-only profile.

**Design** — available via Claude Design.

### Open questions

- **Local-first rationale.** §7 states the tool is local-first because client data should not leave the operator's machine without explicit agreement. A hosted web application breaks that. Resolve before building.
- **`path_config.json`.** Whether it survives, and what replaces it for a hosted deployment.
- **Migration.** What happens to assessments already completed as CSV.
