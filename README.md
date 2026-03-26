# CSFLite

**Lean Security Framework for Startups and SMEs**

CSFLite is a lightweight cybersecurity framework implementation based on NIST CSF v2.0, designed specifically for resource-constrained organizations. It combines automated vulnerability scanning with governance assessments to answer a fundamental question: **Do these security controls exist at all?**

This is not a compliance tool. CSFLite treats cybersecurity as governance under adversarial conditions. Security emerges from embedded constraints, automation, and measurable outcomes, not documentation.

See the [Assessment Philosophy](docs/assessment-philosophy.md) for the full design rationale.

**☕ Support CSFLite:** If this project helps you in any way consider [buying me a coffee](https://buymeacoffee.com/eriklacson). 

---

## Current Status

### ✅ Working Now

- **Governance assessment pipeline** — Complete end-to-end workflow for manual governance baseline assessment
- **Weighted scoring and heatmaps** — Gap analysis with severity ratings across all CSF Functions
- **Top 25 subcategory framework** — Curated, validated against NIST CSWP 29
- **Remediation guidance** — Actionable follow-up steps for every governance gap
- **Governance questionnaire template** — Ready-to-use CSV covering all 25 subcategories with evidence requirements
- **SOC 2 readiness assessment** — CSFLite-to-Trust Services Criteria crosswalk (CC1–CC9, A1, C1), supplement questionnaire for gap domains, gap analysis template, and executive summary template

### 🚧 In Preview

- **Nuclei scan tooling** — CLI wrapper, profile-based scan configuration, and raw output conversion are implemented but not yet validated end-to-end against live targets
- **Scan-to-CSF mapping** — CSV-based template lookups exist (⚠️ deprecated; YAML tag-based system in development on feature branch)
- **Combined assessment** — Tool to merge scan findings with governance results is built but awaiting integration testing

---

## What's Included

### Framework Assets
- Curated CSFLite **Top 25 subcategories** list
- Mapping of **Nuclei templates → CSF subcategories** (CSV format, YAML migration pending)
- **Lookup tables** for automation (CSV/JSON)

### Tooling
- **Governance assessment tool** (`governance_check.py`) — Processes questionnaire responses into scored assessments and heatmaps
- **Nuclei scan tool** (`nuclei_scan_tool.py`) — Profile-based scan configuration and execution *(preview)*
- **Nuclei converter** (`nuclei_convert_tool.py`) — Maps raw scan output to CSF subcategories *(preview)*
- **Combined assessment** (`assess.py`) — Merges scan and governance data into unified report *(preview)*

### Templates & Guidance
- **Governance checklist template** — Pre-built CSV questionnaire for all 25 subcategories
- **Remediation guidance** — Step-by-step actions for each governance gap
- **Scan profiles** — Pre-configured Nuclei scan profiles (baseline_web, baseline_network, baseline_cloud, comprehensive)
- **SOC 2 crosswalk** — Full mapping of Trust Services Criteria (CC1–CC9, A1, C1) to NIST CSF 2.0 subcategories with coverage ratings
- **SOC 2 supplement questionnaire** — 28-question CSV covering five gap domains not addressed by the CSFLite 25 (change management, physical access, security awareness, business continuity, data disposal)
- **SOC 2 gap analysis template** — Client-facing markdown template organized by SOC 2 category, pre-populated from the crosswalk
- **SOC 2 executive summary template** — One-page client-facing summary with coverage score, criteria breakdown, and top remediation items

---

## Use Case

This toolkit is for SMEs, startups, freelance consultants, and security-oriented DevOps teams who want structured risk insight without enterprise overhead.

**Who this is for:**
- Startups preparing for SOC 2, ISO 27001, or customer security questionnaires
- Solo security practitioners or consultants serving multiple small clients
- DevOps teams implementing security controls without dedicated security staff
- Organizations that need evidence-based security assessments, not compliance theater

**Who this is NOT for:**
- Enterprises with dedicated GRC teams (you need enterprise tools)
- Organizations seeking compliance certification (this measures coverage, not maturity)
- Teams wanting automated risk quantification (we do existence checks, not risk scores)

---

## 🚀 Getting Started

Ready to run your first CSF assessment?

**→ [Get Started](docs/GETTING_STARTED.md)**

The Getting Started guide walks you through:
- Installing dependencies (Python 3.12+, Poetry)
- Running a governance baseline assessment
- Interpreting your scored results and heatmap

---

## 📅 Roadmap

See [`docs/development_roadmap.md`](docs/development_roadmap.md) for phased deliverables and progress tracking.

**Current phase:** Integration & Pilot Testing (Phase 5)

**Next milestones:**
- End-to-end validation of scan pipeline against live targets
- YAML-based tag mapping system (feature branch)
- Integration test coverage for full assessment workflow

---

## 📄 License

Released under the [MIT License](./LICENSE).

---

## 🙌 Contributing

Contributions are welcome. Please read **[CONTRIBUTING.md](docs/CONTRIBUTING.md)** before submitting a pull request.

**High-value contributions right now:**
- Bug fixes in the scan pipeline
- Integration test coverage for governance → scan → combined assessment
- Scan profiles for specific environments (SaaS, healthcare, fintech)

**Currently frozen:**
- Nuclei template mappings (YAML migration in progress on feature branch)

This project uses Claude Code for spec-driven development. See CLAUDE.md for context and conventions, and claude-project/ for spec templates and artifacts.

**Requires discussion first:**
- Subcategory changes
- Scoring methodology changes

All contributions must align with the [Assessment Philosophy](docs/csflite-assessment-philosophy.md).

---

## 🏗️ Project Philosophy

CSFLite is built on three core principles:

1. **Coverage before depth** — Determine if controls exist before measuring their effectiveness
2. **Governance as infrastructure** — Policy becomes code, not documents
3. **Lean by default** — Eliminate waste, prioritize secure defaults, design for scalability

This is not a maturity assessment framework. We measure **existence**, not **excellence**.

---

## 📚 Documentation

- [Assessment Philosophy](docs/csflite-assessment-philosophy.md) — Design rationale and methodology
- [Getting Started](docs/GETTING_STARTED.md) — Installation and first assessment
- [Development Roadmap](docs/development_roadmap.md) — Progress tracking and future work
- [Contributing Guide](docs/CONTRIBUTING.md) — How to contribute effectively

### Reference Documentation

- [Top 25 Subcategories](docs/reference/top_25_sub_categories.md) — Selection criteria and definitions
- [Automatable Subcategories](docs/reference/automatable_subcategories.md) — Automation classification
- [Manual Remediation Guide](docs/reference/manual_remediation.md) — Step-by-step remediation for governance gaps
- [Nuclei-to-CSF Mapping](docs/reference/nuclei_to_csf_mapping.md) — Template mapping rationale
- [claude-project/](claude-project/) — Seed documents, spec templates, and ADRs for Claude Code workflows

### SOC 2 Readiness

- [CSFLite-to-SOC 2 Crosswalk](docs/soc2/csflite-soc2-crosswalk.md) — Full TSC mapping with coverage ratings (full / partial / gap)
- [SOC 2 Gap Analysis Template](docs/soc2/soc2-gap-analysis-template.md) — Client-facing findings template organized by Security, Availability, Confidentiality
- [SOC 2 Executive Summary Template](docs/soc2/soc2-executive-summary-template.md) — One-page client-facing readiness summary
- [SOC 2 Supplement Questionnaire](templates/soc2-supplement-questionnaire.csv) — Standalone CSV covering gap domains outside the CSFLite 25
- [ADR-0001: Full CSF Crosswalk Decision](docs/adr/ADR-0001-full-csf-crosswalk.md) — Architectural decision record

---

## 🔧 Technical Stack

- **Language:** Python 3.12+
- **Dependency Management:** Poetry
- **Testing:** pytest
- **Code Quality:** Black (formatting), Ruff (linting), Bandit (security)
- **Scanning:** Nuclei (vulnerability detection)
- **Data:** CSV/JSON (current), YAML (future)
- **Claude Code:** Latest — AI-assisted spec execution

---

## ⚠️ Known Limitations

- Scan pipeline has **not been validated** against live targets (see Phase 5 in roadmap)
- Nuclei mapping uses **deprecated CSV approach** (YAML migration on feature branch)
- No maturity scoring or risk quantification (by design)
- Limited to 25 subcategories (intentional scope constraint)
- Designed for startups/SMEs, not enterprises

---

## 🤝 Support

- **Issues:** Report bugs or request features via [GitHub Issues](https://github.com/eriklacson/CSFLite/issues)
- **Discussions:** Not yet enabled (project too early)
- **Security:** Email maintainer directly for vulnerability reports (see GitHub profile)
- **Donations:** Help sustain development → [Buy Me a Coffee](https://buymeacoffee.com/eriklacson)


---

## 🎯 Success Metrics

CSFLite is successful if it helps organizations:

1. **Identify security gaps** with minimal effort
2. **Prioritize remediation** based on weighted risk
3. **Generate evidence** for compliance needs without compliance-driven work
4. **Scale security practices** as the organization grows

If you're spending more time on the framework than on fixing security gaps, we've failed.

---

*Built with the philosophy that security is governance under adversarial conditions.*

