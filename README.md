# CSFLite Framework

*v0.1.0-alpha — Early release. Governance assessment pipeline is functional. Nuclei scan integration is in preview.*

A lightweight NIST CSF v2.0 implementation for startups and SMEs that answers a simple question: **do your foundational security capabilities exist at all?**

---

## Vision

**CSFLite** is designed for lean security operations. Instead of overwhelming organizations with the full CSF catalog, this framework focuses on:

- The **Top 25 most impactful subcategories** across all CSF Functions
- What can be **automated** (e.g., open ports, outdated software, misconfigurations)
- What must be **validated manually** (e.g., policies, incident response plans, recovery strategies)

CSFLite takes a governance-first approach: a manual checklist assesses whether foundational capabilities exist before any attempt at maturity scoring, risk quantification, or control prescriptions.

---

## Current Status

### ✅ Working Now

- **Governance assessment pipeline** — Complete end-to-end workflow for manual governance baseline assessment
- **Weighted scoring and heatmaps** — Gap analysis with severity ratings across all CSF Functions
- **Top 25 subcategory framework** — Curated, validated against NIST CSWP 29
- **Remediation guidance** — Actionable follow-up steps for every governance gap
- **Governance questionnaire template** — Ready-to-use CSV covering all 25 subcategories with evidence requirements

### 🚧 In Preview

- **Nuclei scan tooling** — CLI wrapper, profile-based scan configuration, and raw output conversion are implemented but not yet validated end-to-end against live targets
- **Scan-to-CSF mapping** — Template-to-subcategory lookup tables and mapping engine exist; pilot testing is pending
- **Combined assessment** — Tool to merge scan findings with governance results is built but awaiting integration testing

---

## What's Included

### Framework Assets
- Curated CSFLite **subcategories** list (Top 25)
- Mapping of **Nuclei templates → CSF subcategories**
- CSV/JSON **lookup tables** for automation

### Tooling
- **Governance assessment tool** (`governance_check.py`) — Processes questionnaire responses into scored assessments and heatmaps
- **Nuclei scan tool** (`nuclei_scan_tool.py`) — Profile-based scan configuration and execution *(preview)*
- **Nuclei converter** (`nuclei_convert_tool.py`) — Maps raw scan output to CSF subcategories *(preview)*
- **Combined assessment** (`assess.py`) — Merges scan and governance data into unified report *(preview)*

### Templates & Guidance
- **Governance checklist template** — Pre-built CSV questionnaire for all 25 subcategories
- **Remediation guidance** — Step-by-step actions for each governance gap
- **Scan profiles** — Pre-configured Nuclei scan profiles (baseline_web, baseline_network, baseline_cloud, comprehensive)

---

## Use Case

This toolkit is for SMEs, startups, freelance consultants, and security-oriented DevOps teams who want structured risk insight without enterprise overhead.

---

## 🚀 Getting Started

Ready to run your first CSF assessment?

**→ [Get Started](docs/GETTING_STARTED.md)**

The Getting Started guide walks you through:
- Installing dependencies (Python, Poetry)
- Running a governance baseline assessment
- Interpreting your scored results and heatmap

---

## 📅 Roadmap

See [`docs/development_roadmap.md`](docs/development_roadmap.md) for phased deliverables and progress tracking.

---

## 📄 License

Released under the [MIT License](./LICENSE).

---

## 🙌 Contributions

Interested in contributing templates, fixes, or feedback? Please wait until the project reaches its first stable release milestone, then check the upcoming `CONTRIBUTING.md`.
