# Getting Started with CSFLite

Welcome to CSFLite! This guide will help you run your first governance baseline assessment.

## What You'll Accomplish

By the end of this guide, you'll have:
- ✅ Installed all required dependencies
- ✅ Completed a governance questionnaire for your organization
- ✅ Generated a scored governance assessment with gap analysis
- ✅ Produced a risk heatmap showing priority areas

---

## Prerequisites

### Required Software

| Software | Version | Check Command | Purpose |
|----------|---------|---------------|---------|
| **Python** | 3.12+ | `python --version` | Core runtime |
| **Poetry** | Latest | `poetry --version` | Dependency management |
| **Git** | Any | `git --version` | Version control |

### System Requirements

- **Operating System**: Linux, macOS, or Windows with WSL2
- **Disk Space**: 500MB+ available

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/eriklacson/CSFLite.git
cd CSFLite
```

### Step 2: Install Python Dependencies

```bash
# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

**Expected output:**
```
Installing dependencies from lock file
...
Installing the current project: csflite (0.1.0)
```

### Step 3: Verify Installation

```bash
# Confirm tools are importable
poetry run python -c "import tools.global_helpers; print('CSFLite ready.')"
```

---

## Configuration

### Directory Structure

```
CSFLite/
├── config/          # Configuration files (paths, settings)
├── csflite/         # Framework validation artifacts
│   └── controls.json  # Canonical 25-control reference
├── data/            # Reference data & CSF mappings
│   ├── csf_lookup.csv
│   ├── nuclei_csf_lookup.json
│   ├── profiles.yaml
│   └── targets.txt
├── docs/
│   ├── adr/         # Architectural decision records
│   ├── reference/   # CSFLite framework reference docs
│   ├── soc2/        # SOC 2 readiness deliverables
│   └── hipaa/       # HIPAA readiness deliverables
├── templates/       # Input templates for assessments
├── scans/           # Nuclei scan outputs (generated)
├── output/          # Final assessment reports (generated)
└── tools/           # Python assessment scripts
```

### Create Output Directory

```bash
mkdir -p output
```

---

## Your First Governance Assessment

CSFLite's governance assessment answers a fundamental question: **do your core cybersecurity capabilities exist at all?** This is a coverage assessment, not a maturity model. A "Yes" means the capability exists in some intentional, repeatable form.

### Step 1: Prepare Your Governance Checklist

```bash
# Copy the governance template to your working file
cp templates/governance_checks_template.csv templates/my_governance.csv
```

Open `templates/my_governance.csv` in a spreadsheet editor or text editor. For each subcategory, fill in the `response` column with one of:

| Response | Meaning | Score |
|----------|---------|-------|
| **Yes** | Capability exists and is intentional | 1.0 |
| **Partial** | Some elements exist, gaps remain | 0.5 |
| **No** | Capability does not exist | 0.0 |

The checklist covers all 25 CSFLite subcategories across six CSF Functions:

- **GOVERN** — Policy, roles, risk management, supply chain
- **IDENTIFY** — Asset inventories, vulnerability management, risk prioritization
- **PROTECT** — Access control, data protection, backups, network security
- **DETECT** — Network monitoring, endpoint monitoring, alert analysis, incident declaration
- **RESPOND** — Incident response, notification, containment, eradication
- **RECOVER** — Recovery execution, recovery communication

Each item includes an evidence column describing what documentation or artifacts would support a "Yes" response.

### Step 2: Run the Governance Assessment

```bash
python tools/governance_check.py \
  --governance_checklist templates/my_governance.csv \
  --governance_assessment_csv output/governance_assessment.csv \
  --governance_heatmap output/governance_heatmap.csv
```

**Expected output:**
```
reading CSF lookup from: ../data/csf_lookup.csv
reading governance checklist from: templates/my_governance.csv
generating governance assessment...
Governance assessment written to: output/governance_assessment.csv
Governance assessment heatmap written to: output/governance_heatmap.csv
```

### Step 3: Review Your Results

**Governance Assessment** (`output/governance_assessment.csv`):

| Column | Description |
|--------|-------------|
| `csf_subcategory_id` | NIST CSF subcategory identifier |
| `csf_subcategory_name` | Human-readable subcategory name |
| `response` | Your Yes/Partial/No response |
| `weight` | Relative importance weight |
| `assessment_score` | Weighted score (response × weight) |
| `gap_score` | Weighted gap (weight − assessment_score) |
| `recommendation` | Suggested remediation action |

**Governance Heatmap** (`output/governance_heatmap.csv`):

| Column | Description |
|--------|-------------|
| `csf_subcategory_id` | NIST CSF subcategory identifier |
| `severity` | Risk severity: `high`, `medium`, or `low` |
| `gap_score` | Size of the gap |

The heatmap prioritizes your remediation efforts. Focus on `high` severity items first — these represent the largest weighted gaps in your security posture.

```bash
# View the assessment
cat output/governance_assessment.csv

# View the heatmap
cat output/governance_heatmap.csv

# Or open in a spreadsheet application
open output/governance_assessment.csv  # macOS
xdg-open output/governance_assessment.csv  # Linux
```

### Step 4: Address Gaps

For each gap identified, refer to [`docs/reference/manual_remediation.md`](reference/manual_remediation.md) for specific, actionable remediation steps organized by CSF subcategory.

---

## Interpreting Your Assessment

### What Scores Mean

CSFLite scores represent **coverage**, not maturity or risk.

- A score of 80% means: "80% of the assessed governance outcomes exist in some intentional form."
- It does **not** mean: "80% of cybersecurity risks are mitigated."

### Priority Framework

1. **High severity gaps** (gap_score > 0) in GOVERN subcategories — fix first, these are foundational
2. **High severity gaps** in PROTECT subcategories — these prevent or limit incident impact
3. **Any "No" response** — a missing capability is always higher priority than a partial one
4. **Partial responses** — improve these after addressing missing capabilities

---

## SOC 2 Readiness Assessment

If your organization needs to demonstrate readiness for a SOC 2 examination, CSFLite includes a standalone set of deliverables that map your governance assessment results to AICPA Trust Services Criteria.

> **Scope:** Security (CC1–CC9), Availability (A1), Confidentiality (C1). These deliverables are a readiness assessment only — they do not constitute SOC 2 compliance or an audit opinion.

### Step 1: Complete the Governance Assessment First

The SOC 2 deliverables are designed to be used after you have completed the standard governance assessment (see above). Your governance assessment results determine which SOC 2 criteria have coverage and which are gaps.

### Step 2: Review the Crosswalk

Open [`docs/soc2/csflite-soc2-crosswalk.md`](soc2/csflite-soc2-crosswalk.md) to see how your assessed controls map to each Trust Services Criterion. Each entry shows:

- The SOC 2 criterion and its mapped NIST CSF 2.0 subcategory
- Whether the subcategory is in the CSFLite 25 (`Yes` / `No`)
- A coverage rating: `full`, `partial`, or `gap`
- Notes on what is missing and which supplement questionnaire section addresses the gap

### Step 3: Complete the Supplement Questionnaire

For SOC 2 criteria that map to subcategories outside the CSFLite 25, complete the supplement questionnaire:

```bash
cp templates/soc2-supplement-questionnaire.csv templates/my_soc2_supplement.csv
```

Open the file and fill in the `response` column (Yes / Partial / No) along with any notes. The questionnaire covers five gap domains:

| Domain | SOC 2 Criteria |
|--------|----------------|
| Security awareness and communication | CC2 |
| Physical access controls | CC6.4 |
| Change management | CC8 |
| Business continuity planning | A1 |
| Data disposal | C1.2 |

### Step 4: Populate the Gap Analysis Template

Open [`docs/soc2/soc2-gap-analysis-template.md`](soc2/soc2-gap-analysis-template.md) and fill in the **Current State** and **Evidence Assessed** columns for each SOC 2 criterion using your governance assessment output and supplement questionnaire responses. Coverage status and remediation recommendations are pre-populated from the crosswalk.

### Step 5: Complete the Executive Summary

Open [`docs/soc2/soc2-executive-summary-template.md`](soc2/soc2-executive-summary-template.md) and fill in the overall coverage score, criteria breakdown counts, and the top 3 priority remediation items identified in the gap analysis. This is the primary client-facing deliverable.

---

## HIPAA Readiness Assessment

If your organization handles electronic Protected Health Information (ePHI) for US healthcare Covered Entities as a Business Associate, CSFLite includes a standalone set of deliverables that map your governance assessment results to the HIPAA Security Rule and Breach Notification Rule.

> **Scope:** Administrative Safeguards (§164.308), Physical Safeguards (§164.310), Technical Safeguards (§164.312), and Breach Notification Rule — BA obligations (§164.400–414). These deliverables are a readiness assessment only — they do not constitute HIPAA compliance, a HIPAA audit, or any certification.

### Step 1: Complete the Governance Assessment First

The HIPAA deliverables are designed to be used after you have completed the standard governance assessment (see above). Your governance assessment results determine which HIPAA standards have coverage and which are gaps.

### Step 2: Review the Crosswalk

Open [`docs/hipaa/csflite-hipaa-crosswalk.md`](hipaa/csflite-hipaa-crosswalk.md) to see how your assessed controls map to each HIPAA Security Rule standard and implementation specification. Each entry shows:

- The HIPAA section reference and implementation specification name
- Whether the specification is Required (R) or Addressable (A)
- The mapped NIST CSF 2.0 subcategory and whether it is in the CSFLite 25
- A coverage rating: `full`, `partial`, `gap`, or `advisory`
- Notes on ePHI scoping requirements and which supplement questions address gaps

### Step 3: Complete the Supplement Questionnaire

For HIPAA standards that map to subcategories outside the CSFLite 25, complete the supplement questionnaire:

```bash
cp templates/hipaa-supplement-questionnaire.csv templates/my_hipaa_supplement.csv
```

Open the file and fill in the `response` column (Yes / Partial / No) along with any notes. The questionnaire covers nine gap domains in this order:

| Q# | Topic | HIPAA Section |
|----|-------|---------------|
| Q1 | PHI data flow mapping (prerequisite) | §164.308(a)(1)(i) |
| Q2 | Physical safeguards — facility/workstation (remote/hybrid qualifier) | §164.310(a)(1), (b), (c) |
| Q3 | Device and media disposal | §164.310(d)(1)(i–ii) |
| Q4 | Security awareness and training | §164.308(a)(5) |
| Q5 | BAA existence verification | §164.308(b)(1), §164.314(a)(2)(i) |
| Q6 | Breach notification procedures | §164.410, §164.412 |
| Q7 | Contingency planning / BCP/DR | §164.308(a)(7) |
| Q8 | Workforce security | §164.308(a)(3) |
| Q9 | Minimum necessary standard | §164.308(a)(4) |

### Step 4: Populate the Gap Analysis Template

Open [`docs/hipaa/hipaa-gap-analysis-template.md`](hipaa/hipaa-gap-analysis-template.md) and fill in the **Current State** and **Evidence Assessed** columns for each HIPAA standard using your governance assessment output and supplement questionnaire responses. Coverage status and remediation recommendations are pre-populated from the crosswalk.

### Step 5: Complete the Executive Summary

Open [`docs/hipaa/hipaa-executive-summary-template.md`](hipaa/hipaa-executive-summary-template.md) and fill in the overall coverage score, HIPAA standards breakdown counts, and the top 3 priority remediation items. This is the primary client-facing deliverable and is limited to one page.

---

## 🚧 Preview: Nuclei Scan Integration

> **Status**: The scan tooling infrastructure is built and unit-tested, but has not been validated end-to-end against live targets. The tools below are functional but should be treated as preview features. Pilot testing is tracked in the [development roadmap](development_roadmap.md).

CSFLite is designed to combine governance assessment with automated vulnerability scanning. The following tools exist for the scan workflow:

### Prerequisites (Additional)

| Software | Version | Check Command | Purpose |
|----------|---------|---------------|---------|
| **Nuclei** | Latest | `nuclei -version` | Vulnerability scanner |

**Install Nuclei:**
```bash
# macOS
brew install nuclei

# Using Go
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# Update templates
nuclei -update-templates
```

### Configure Targets

```bash
# Edit the targets file with systems you own
nano data/targets.txt
```

**Example targets format:**
```
# Web applications
https://example.com
https://app.example.com

# IP addresses
192.168.1.100

# Domains
internal.company.local
```

⚠️ **Important**: Only scan systems you own or have explicit permission to test.

### Scan Profiles

CSFLite includes pre-configured scan profiles in `data/profiles.yaml`:

- `baseline_web` — Web application security checks
- `baseline_network` — Network infrastructure scans
- `baseline_cloud` — Cloud infrastructure checks
- `comprehensive` — Full coverage scan (slower)

### Preview Workflow

```bash
# Step 1: Run a Nuclei scan using a profile
python tools/nuclei_scan_tool.py \
  --profile baseline_web \
  --targets data/targets.txt

# Step 2: Convert raw Nuclei output to CSFLite format
python tools/nuclei_convert_tool.py \
  --nuclei_raw scans/nuclei_raw_scan.jsonl \
  --csflite_out output/nuclei_csf_mapped.json
```

The combined assessment tool (`tools/assess.py`) can merge scan findings with governance results, but this workflow has not yet been pilot-tested. Refer to the roadmap for updates.

---

## Troubleshooting

### Common Issues

#### "Poetry not found"

```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
exec $SHELL
```

#### "Module not found" errors

```bash
# Ensure you're in the Poetry environment
poetry shell

# Or prefix commands with poetry run
poetry run python tools/governance_check.py --help

# Clear cache and reinstall
poetry env remove python
poetry install
```

#### "Permission denied" on output

```bash
mkdir -p scans output
chmod -R 755 scans/ output/
```

---

## Explore Further

### Reference Documentation

- [`docs/reference/top_25_sub_categories.md`](reference/top_25_sub_categories.md) — Subcategory definitions and selection rationale
- [`docs/reference/automatable_subcategories.md`](reference/automatable_subcategories.md) — Automation classification per subcategory
- [`docs/reference/manual_remediation.md`](reference/manual_remediation.md) — Remediation guidance for every governance gap
- [`docs/reference/nuclei_to_csf_mapping.md`](reference/nuclei_to_csf_mapping.md) — How Nuclei templates map to CSF subcategories

### Customize Your Assessments

- **Adjust weights**: Edit `data/csf_lookup.csv` to change subcategory weights
- **Modify mappings**: Edit `data/nuclei_csf_lookup.json` for scan-to-CSF mapping
- **Extend the questionnaire**: Add rows to `templates/governance_checks_template.csv`

---

## Getting Help

This project is in early development. For questions or issues:
1. Check existing documentation in `docs/`
2. Review the troubleshooting section above
3. Open an issue on GitHub

---

*Last updated: 2026-02-06*
