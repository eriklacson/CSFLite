# LeanSecurity — CSFLite
## Project Seed Document v1.0
**Classification:** LeanSecurity Internal IP  
**Status:** Phase 5 build in progress  
**Last updated:** March 2026

---

## 1. What This Is

CSFLite is a lean, governance-engineered cybersecurity assessment framework based on NIST CSF v2.0. It takes two inputs — a manual governance questionnaire and automated Nuclei vulnerability scan results — scores them against a curated set of 25 high-impact CSF subcategories using a weighted coverage model, and produces gap analyses with prioritized heatmaps and remediation guidance. The end-to-end value: an organization that has never assessed its security posture can identify what controls exist, what's missing, and what to fix first — in hours, not weeks.

CSFLite is LeanSecurity internal IP. It is the reusable framework engine that powers client delivery engagements but does not itself contain client-specific configurations, reports, or data.

There is no proof-of-concept client for CSFLite itself. Client engagements (SOC 2 readiness, HIPAA readiness) consume CSFLite as a dependency and are tracked as separate projects with their own seed documents.

### Project Separation

CSFLite is the framework layer. Client delivery projects consume its outputs. Compliance crosswalks (SOC 2, HIPAA, ISO 27001) are reference documents that live in CSFLite but inform client delivery.

| Project | Asset Type | Owns |
|---|---|---|
| `LeanSecurity — CSFLite` | Framework IP | 25 subcategories, scoring engine, governance pipeline, scan pipeline, remediation guidance, compliance crosswalks, assessment philosophy |
| `LeanSecurity — [Client]` | Client delivery | Client-specific questionnaire responses, scan targets, assessment reports, remediation roadmaps, engagement artifacts |
| `LeanSecurity — Spec System` | Tooling IP | Seed document template, system instruction, project.yaml schema, ADR format — the spec development workflow itself |

---

## 2. Architecture Pattern

**File-Driven Intake + Dual-Pipeline Scoring Engine.** Two independent assessment pipelines (governance questionnaire, Nuclei scan) feed into a shared scoring and heatmap layer, producing unified coverage reports.

### Layers

**Intake Layer**  
Responsible for ingesting raw inputs: CSV governance questionnaire responses and JSON Nuclei scan output. Validates required fields, normalizes data structures. Produces cleaned, typed records ready for scoring. Never performs scoring, weighting, or output generation.

**Scoring Layer**  
Responsible for joining intake records against the CSF lookup reference data (`csf_lookup.csv`), applying weights, computing coverage scores, and classifying heatmap severity. Produces scored assessment records and heatmap records. Never reads raw input files directly — only consumes validated records from the intake layer.

**Output Layer**  
Responsible for serializing scored records to CSV/JSON files. Never performs scoring logic. Handles path resolution via `path_config.json`.

### Flow

```
Governance CSV                Nuclei JSON
      │                            │
      ▼                            ▼
 Intake: validate             Intake: normalize
 required fields              + convert entries
      │                            │
      ▼                            ▼
 Scoring: join CSF            Scoring: map templates
 lookup, apply weights,       to CSF subcategories,
 compute coverage             compute scan heatmap
      │                            │
      ▼                            ▼
 governance_assessment.csv    scan-findings.csv
 governance_heatmap.csv       scan_heatmap.csv
      │                            │
      └──────────┬─────────────────┘
                 ▼
          Combined Assessment         ← merge governance + scan
                 │
                 ▼
          Unified report              ← combined heatmap + scores
```

### Delivery Mode

Synchronous, batch-oriented CLI execution. Each tool runs independently against file inputs and produces file outputs. There is no event bus, queue, or streaming component.

Built now: governance pipeline (end-to-end working), scan pipeline (tools built, not validated against live targets), combined assessment (built, awaiting integration testing).

Designed for but deferred: YAML-based tag mapping for Nuclei templates (feature branch exists, blocked on Phase 5 validation).

---

## 3. Interface Contracts

All contracts are prescriptive — they define what the schemas should be, not merely what they are today. Implementations that deviate from these contracts are bugs.

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

### Nuclei Scan Input (JSON)

Raw Nuclei scanner output. Produced by Nuclei CLI (via `nuclei_scan_tool.py`), consumed by `nuclei_json_converter.py`.

| Field | Type | Required | Description |
|---|---|---|---|
| `templateID` or `template-id` | `string` | Yes | Nuclei template identifier (both naming conventions accepted) |
| `host` or `url` | `string` | Yes | Target that was scanned (both naming conventions accepted) |
| `matched-at` | `string` | No | Specific URL or endpoint where finding was detected |
| `severity` | `string` | Yes | Nuclei severity: `info`, `low`, `medium`, `high`, `critical` |
| `timestamp` | `string` | No | ISO 8601 timestamp of finding |
| `matcher-name` | `string` | No | Name of the matcher that triggered |
| `description` | `string` | No | Human-readable finding description |

### Nuclei-to-CSF Mapping (CSV — current; YAML — target)

Maps Nuclei template IDs to CSF subcategories. Produced by framework maintainer, consumed by `map_scan_to_csf()`.

**Current format (CSV, deprecated):**

| Field | Type | Description |
|---|---|---|
| `templateID` | `string` | Exact Nuclei template ID |
| `csf_function` | `string` | CSF Function name |
| `csf_subcategory_id` | `string` | Canonical subcategory ID |
| `csf_subcategory_name` | `string` | Human-readable subcategory name |
| `rationale` | `string` | Why this template maps to this subcategory |

**Target format (YAML, feature branch):** Tag-based rules that match Nuclei template tags to CSF subcategories without requiring per-template entries. Schema TBD — blocked on Phase 5 validation.

### Scan Heatmap Output (CSV)

Scan-derived severity rankings. Produced by `generate_scan_heatmap()`, consumed by combined assessment and report tools.

| Field | Type | Description |
|---|---|---|
| `csf_subcategory_id` | `string` | Canonical subcategory ID |
| `name` | `string` | Human-readable subcategory name |
| `count` | `int` | Number of scan findings mapped to this subcategory |
| `max_severity` | `string` | Highest Nuclei severity among findings |
| `weighted_score` | `string` | Composite score (weight × severity + log finding count), formatted to 2 decimal places |

### Path Configuration (JSON)

Centralized file path registry. Produced by framework maintainer, consumed by all CLI tools via `global_helpers.get_paths()`.

| Field | Type | Description |
|---|---|---|
| `governance_checklist` | `string` | Path to governance checklist input CSV |
| `lookup_csv` | `string` | Path to Nuclei-to-CSF mapping CSV |
| `heatmap_lookup` | `string` | Path to heatmap severity threshold CSV |
| `csf_lookup` | `string` | Path to CSF subcategory reference CSV |
| `output_csv` | `string` | Path for scan findings output CSV |
| `output_json` | `string` | Path for scan findings output JSON |
| `heatmap_csv` | `string` | Path for scan heatmap output CSV |
| `governance_assessment_csv` | `string` | Path for governance assessment output CSV |
| `governance_heatmap_csv` | `string` | Path for governance heatmap output CSV |
| `nuclei_profile` | `string` | Path to Nuclei scan profiles YAML |
| `nuclei_scan_findings` | `string` | Path for converted Nuclei scan findings JSON |

### Design Rules

- All `csf_subcategory_id` values must be validated against NIST CSWP 29 before inclusion in any reference data file
- `csf_lookup.csv` is the single source of truth for subcategory weights — no tool hardcodes weights
- Response values in governance checklists must be exactly `Yes`, `Partial`, or `No` — case-sensitive, no synonyms
- All scored output fields that represent decimal values are formatted as strings with 2 decimal places (e.g., `"1.50"`)
- Path configuration uses paths relative to project root — tools resolve paths via `path_config.json`, not hardcoded paths
- Nuclei converter accepts both legacy (`template-id`, `host`) and current (`templateID`, `url`) field names — no breaking changes when Nuclei updates its output format

---

## 4. Component Registry

| Component | Source/Domain | Status |
|---|---|---|
| `governance_check.py` | Governance assessment CLI | Complete |
| `assess_helpers.py` | Shared scoring and heatmap functions | Complete |
| `global_helpers.py` | Shared I/O utilities (CSV/JSON, path config) | Complete |
| `nuclei_scan_tool.py` | Nuclei CLI wrapper with profile support | Complete (not validated) |
| `nuclei_helpers.py` | Nuclei profile loading, command building, execution | Complete (not validated) |
| `nuclei_json_converter.py` | Raw Nuclei JSON → CSFLite summary format | Complete (not validated) |
| `nuclei_convert_tool.py` | Nuclei converter CLI | Complete (not validated) |
| `assess.py` | Combined scan + governance assessment | Complete (not validated, marked for deprecation) |
| `mapping_rules.yaml` | YAML tag-based Nuclei mapping rules | Feature branch (not merged) |

---

## 5. Repository Structure

### `CSFLite`

```
CSFLite/
├── tools/                          ← Python CLI tools and helper modules
│   ├── governance_check.py         ← Governance assessment CLI (working)
│   ├── assess.py                   ← Combined assessment CLI (preview, deprecated)
│   ├── assess_helpers.py           ← Scoring engine and heatmap functions
│   ├── global_helpers.py           ← Shared I/O utilities
│   ├── nuclei_scan_tool.py         ← Nuclei scan CLI wrapper (preview)
│   ├── nuclei_helpers.py           ← Nuclei profile/command helpers
│   ├── nuclei_json_converter.py    ← Raw scan → CSFLite format
│   └── nuclei_convert_tool.py      ← Nuclei converter CLI (preview)
├── tests/                          ← pytest unit tests (mirrors tools/)
│   ├── fixtures/                   ← Sample data for tests
│   ├── integration/                ← End-to-end pipeline tests (planned)
│   ├── test_assess_helpers.py      ← Scoring and heatmap tests
│   ├── test_global_helpers.py      ← I/O utility tests
│   ├── test_nuclei_helpers.py      ← Nuclei helper tests
│   └── test_nuclei_json_converter.py
├── data/                           ← Reference data (CSF lookups, mappings, profiles)
│   ├── csf_lookup.csv              ← Authoritative subcategory weights + recommendations
│   ├── nuclei_csf_lookup.csv       ← Template→CSF mapping (deprecated)
│   ├── nuclei_csf_lookup.json      ← JSON version (deprecated)
│   ├── heat_map_lookup.csv         ← Heatmap severity thresholds
│   ├── profiles.yaml               ← Nuclei scan profile definitions
│   └── targets.txt                 ← Default scan targets
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
│       ├── nuclei_to_csf_mapping.md
│       └── manual_questionnaire.md
├── input/examples/                 ← Sample input data
├── output/examples/                ← Sample output data
├── scans/                          ← Generated scan outputs (gitignored)
├── output/                         ← Generated assessment outputs (gitignored)
├── .github/workflows/              ← CI pipeline (Black, Ruff, Bandit, pytest)
├── pyproject.toml                  ← Poetry project definition
├── .pre-commit-config.yaml         ← Pre-commit hook configuration
└── README.md
```

### Boundary Rules

- `tools/` modules may import from `tools/global_helpers.py` and `tools/assess_helpers.py` — never from CLI entry points (`governance_check.py`, `assess.py`, `nuclei_scan_tool.py`)
- `tests/` mirrors `tools/` structure — each `tools/x.py` has a corresponding `tests/test_x.py`
- `data/` files are reference data, not generated output — they are version-controlled and change only through deliberate maintainer action
- `config/path_config.json` is the single source of truth for file paths — no tool constructs paths independently
- `docs/csflite-assessment-philosophy.md` is the authoritative methodology document — conflicts between it and any other documentation are resolved in its favor
- `templates/` contains user-facing input templates that define the assessment interface — changes here affect the client-facing assessment experience

---

## 6. Database Schema

Not applicable. CSFLite uses file-based persistence (CSV/JSON). All state is contained in input files, reference data files, and output files. There is no database, no ORM, no migrations.

If CSFLite evolves to a service model, this section becomes relevant and should define tables for assessment sessions, client configurations, and historical results with a multi-tenancy isolation strategy.

---

## 7. Hosting Stack

CSFLite runs as a local CLI tool on the operator's machine. There is no hosting infrastructure, no deployment pipeline, and no remote services.

### Infrastructure Needs

| Need | Interface/Constraint | Notes |
|------|---------------------|-------|
| Python runtime | Python 3.12+ | Required for all tools |
| Dependency management | Poetry | Manages virtualenv and packages |
| Nuclei scanner | Nuclei CLI (latest) | Required only for scan pipeline, not governance |
| Filesystem | Read/write access to project directory | All I/O is local file-based |

### Deployment Profile — Local Development

| Need | Service | Notes |
|------|---------|-------|
| Runtime | Local Python 3.12+ via Poetry | `poetry install && poetry shell` |
| Scanner | Nuclei installed via Go or binary | Optional — governance pipeline works without it |
| Test targets | Docker containers (DVWA, WebGoat) | For Phase 5 validation only |

Local-first because the tool is operated by the consultant on their own machine, processing client data that should not leave the local environment without explicit agreement.

### Future Profiles

No other deployment profiles are currently designed for. A web-based or API-based profile would require a separate seed document if/when that scope is approved.

---

## 8. CSFLite Interface Contract

This section is self-referential — CSFLite IS the framework. The contracts below define how CSFLite's own components interact with the reference data that defines the framework.

### `csf_lookup.csv` — Authoritative Schema

```csv
csf_subcategory_id,weight,recommendation
GV.PO-01,1.0,"Establish and communicate a formal cybersecurity policy"
GV.RR-01,1.2,"Assign named accountability for cybersecurity risk"
...
```

Exactly 25 rows. One per subcategory. This file is the single source of truth for what CSFLite assesses.

### What the Scoring Engine Uses

| Field | Used for |
|---|---|
| `csf_subcategory_id` | Join key — links governance responses and scan findings to the framework |
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
| 2 | Reference Data & Mappings — CSF lookup, Nuclei mappings, scan profiles | Complete |
| 3 | Governance Assessment Pipeline — questionnaire → scored output → heatmap | Complete |
| 4 | Scan Tooling Infrastructure — Nuclei wrapper, converter, scan-to-CSF mapping | Complete (not validated) |
| 5 | Integration & Pilot Testing — end-to-end validation against live targets | In progress |
| 6 | Release Hardening — CI fixes, documentation audit, v0.1.0 tag | Not started |
| 7 | Community & Iteration — external contributions, expanded mappings | Not started |

### Current Status (Phase 5)

**Decided, not yet built:**
- Docker-based test targets (DVWA, WebGoat) for reproducible scan validation
- Integration tests covering full scan pipeline (scan JSON → mapped CSV → heatmap)
- YAML-based tag mapping merge (blocked on Phase 5 validation)

**In progress:**
- Validating Nuclei scan pipeline against live targets
- Fixing known technical debt (CI Bandit target, Python version mismatch, path_config relative paths)

**Known blockers:**
- Scan pipeline validation requires controlled test environment with known-state targets
- YAML mapping branch cannot merge until CSV-based pipeline is validated (avoid compounding unknowns)

### Configuration (current structure)

```json
{
    "governance_checklist": "scans/governance_checks.csv",
    "lookup_csv": "data/nuclei_csf_lookup.csv",
    "heatmap_lookup": "data/heat_map_lookup.csv",
    "csf_lookup": "data/csf_lookup.csv",
    "output_csv": "output/scan-findings.csv",
    "output_json": "output/scan-findings.json",
    "heatmap_csv": "output/scan_heatmap.csv",
    "governance_assessment_csv": "output/governance_assessment.csv",
    "governance_heatmap_csv": "output/governance_heatmap.csv",
    "nuclei_profile": "data/profiles.yaml",
    "nuclei_scan_findings": "output/nuclei_scan_findings.json"
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
| Governance pipeline before scan pipeline | Governance validated first, scans layered on top | Mirrors assessment philosophy — coverage before depth. Manual governance establishes baseline that scanning extends. |
| Nuclei as scan engine | Nuclei (ProjectDiscovery) | Open source, template-based, tag system enables CSF mapping, active community, covers web/network/cloud. |
| CSV/JSON for persistence | Flat files, no database | Eliminates infrastructure dependency. Keeps tool portable and local. Appropriate for current CLI-based delivery mode. |
| YAML migration for template mapping | Moving from per-template CSV to tag-based YAML rules | CSV approach does not scale — requires manual entry per template. YAML tag rules can match categories of templates. Blocked on Phase 5 validation to avoid compounding unknowns. |
| Compliance crosswalks as reference docs | Stored in `docs/reference/`, not as executable mappings | Crosswalks inform client delivery projects but are not consumed by the scoring engine. CSFLite does not claim compliance. |
| Assessment philosophy as authoritative | `csflite-assessment-philosophy.md` overrides all other docs on conflicts | Single source of truth for methodology prevents drift across documentation. |
| Pre-commit hooks + CI | Black, Ruff, Bandit, pytest | Enforces code quality without manual review overhead. Appropriate for solo developer workflow. |

---

## 11. What This Project Does Not Own

- **Client-specific assessment data** — lives in `LeanSecurity — [Client]` projects. CSFLite provides the framework; client projects provide the questionnaire responses, scan targets, and deliverables.
- **SOC 2 / HIPAA / ISO 27001 readiness assessments** — these are client delivery engagements that consume CSFLite. Compliance crosswalk reference documents live in CSFLite; readiness assessment workflows, gap analyses, and remediation roadmaps live in client projects.
- **Tool integrations (OWASP ZAP, Graylog, TheHive, DefectDojo)** — planned integrations per the development roadmap are future scope. When built, they may live in CSFLite if they are framework-generic, or in separate projects if they are deployment-specific.
- **Unified governance dashboard** — longer-horizon milestone that would require a service model. Would need its own seed document.
- **Maturity assessment, risk quantification, continuous monitoring** — explicitly out of scope by design. CSFLite is Stage 1 (coverage). Later stages are separate projects.
- **Spec development workflow** — the seed document template, system instruction, project.yaml schema, and ADR format are owned by `LeanSecurity — Spec System`, not CSFLite.
