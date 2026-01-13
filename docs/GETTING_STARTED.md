# Getting Started with CSFLite

Welcome to CSFLite! This guide will help you set up and run your first NIST CSF assessment in under 10 minutes.

## What You'll Accomplish

By the end of this guide, you'll have:
- ✅ Installed all required dependencies
- ✅ Configured CSFLite for your environment
- ✅ Run a test security scan
- ✅ Generated your first CSF assessment baseline

---

## Prerequisites

### Required Software

Before you begin, ensure you have the following installed:

| Software | Version | Check Command | Purpose |
|----------|---------|---------------|---------|
| **Python** | 3.12+ | `python --version` | Core runtime |
| **Poetry** | Latest | `poetry --version` | Dependency management |
| **Nuclei** | Latest | `nuclei -version` | Vulnerability scanner |
| **Git** | Any | `git --version` | Version control |

### System Requirements

- **Operating System**: Linux, macOS, or Windows with WSL2
- **Disk Space**: 2GB+ available
- **Network**: Internet connection for downloading templates and dependencies
- **Permissions**: Ability to install packages and run network scans

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/eriklacson/CSFLite.git
cd CSFLite
```

### Step 2: Install Python Dependencies

CSFLite uses Poetry for dependency management:

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

### Step 3: Install Nuclei Scanner

Nuclei is the vulnerability scanner that powers CSFLite's technical checks.

**Option A: Using Go (Recommended)**
```bash
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

**Option B: Using Package Managers**
```bash
# macOS
brew install nuclei

# Linux (Debian/Ubuntu)
sudo apt update && sudo apt install nuclei

# Or download binary from: https://github.com/projectdiscovery/nuclei/releases
```

**Verify installation:**
```bash
nuclei -version
```

### Step 4: Update Nuclei Templates

Download the latest vulnerability detection templates:

```bash
nuclei -update-templates
```

This downloads 5000+ templates to `~/nuclei-templates/`

---

## Configuration

### Understanding the Directory Structure

```
CSFLite/
├── config/          # Configuration files (paths, settings)
├── data/            # Reference data & CSF mappings
│   ├── csf_lookup.csv
│   ├── nuclei_csf_lookup.json
│   ├── profiles.yaml
│   └── targets.txt
├── templates/       # Input templates for assessments
├── scans/           # Nuclei scan outputs (generated)
├── output/          # Final assessment reports (generated)
└── tools/           # Python assessment scripts
```

### Configure Target Systems

CSFLite needs to know what to scan. Create your target list:

```bash
# Option 1: Edit the default targets file
nano data/targets.txt

# Option 2: Create a custom targets file
cp data/targets.txt data/my_targets.txt
nano data/my_targets.txt
```

**Example targets format:**
```
# Web applications
https://example.com
https://app.example.com

# IP addresses
192.168.1.100

# IP ranges (CIDR notation)
10.0.0.0/24

# Domains (Nuclei will resolve)
internal.company.local
```

⚠️ **Important**: Only scan systems you own or have explicit permission to test.

### Review Configuration Files

**Path Configuration** (`config/path_config.json`)
```json
{
  "nuclei_json_output": "scans/nuclei_output.json",
  "nuclei_csv_output": "output/nuclei_csf_mapped.csv",
  "governance_input": "templates/governance_checks_template.csv",
  "governance_output": "output/governance_results.csv",
  "combined_output": "output/csf_assessment.csv"
}
```

**Scan Profiles** (`data/profiles.yaml`)

CSFLite includes pre-configured scan profiles:
- `baseline_web` - Web application security checks
- `baseline_network` - Network infrastructure scans
- `baseline_cloud` - Cloud infrastructure checks
- `comprehensive` - Full coverage scan (slower)

View available profiles:
```bash
cat data/profiles.yaml
```

---

## Quick Validation Test

Let's verify everything works with a safe test scan.

### Run a Test Scan

```bash
# Create a test target (scanme.nmap.org is a safe test site)
echo "scanme.nmap.org" > data/test_target.txt

# Run a quick baseline scan
python tools/nuclei_scan_tool.py --profile baseline_web --targets data/test_target.txt
```

**Expected output:**
```
[INFO] Starting Nuclei scan...
[INFO] Profile: baseline_web
[INFO] Target file: data/test_target.txt
[INFO] Output: scans/nuclei_output.json
[INFO] Scan completed successfully
```

### Verify Output Files

Check that scan results were created:

```bash
# List scan outputs
ls -lh scans/

# Preview scan results (first 20 lines)
head -n 20 scans/nuclei_output.json
```

---

## Your First Full Assessment

Now let's run a complete CSF assessment workflow.

### Workflow Overview

```
1 Governance Check → 2. Generate Report 3. Scan Endpoints → 4. Convert Results
   (Manual Review)       (CSF Assessment)     (Nuclei)         (Map to CSF)         
```


### Step 1: Complete Governance Checklist

```bash
# Copy the governance template
cp templates/governance_checks_template.csv templates/my_governance.csv

# Edit the file and mark items as Compliant/Non-Compliant/Partial
nano templates/my_governance.csv
```

**Governance items cover:**
- Asset management policies
- Access control procedures
- Incident response plans
- Business continuity planning
- Security awareness training

### Step 2: Process Governance Responses

```bash
# Convert governance responses to CSF format
python tools/governance_check.py \
  --input templates/my_governance.csv \
  --output output/governance_results.csv \ governance_heatmap.csv
```

# Coming Soon: Nuclei Scan to CSF Assessment

This feature is still under development. 

### Step 1: Run Nuclei Scan

```bash
# Use your custom targets
python tools/nuclei_scan_tool.py \
  --profile baseline_web \
  --targets data/my_targets.txt
```

### Step 2: Convert Scan to CSF Format

```bash
# Map Nuclei findings to NIST CSF subcategories
python tools/nuclei_convert_tool.py \
  --input scans/nuclei_output.json \
  --output output/nuclei_csf_mapped.csv
```

### Step 5: Generate Final Assessment

```bash
# Combine technical + governance into CSF assessment
python tools/assess.py \
  --nuclei output/nuclei_csf_mapped.csv \
  --governance output/governance_results.csv \
  --output output/csf_assessment.csv
```

### View Your Results

```bash
# View the final CSF assessment
cat output/csf_assessment.csv

# Or open in a spreadsheet application
open output/csf_assessment.csv  # macOS
xdg-open output/csf_assessment.csv  # Linux
```

**The assessment includes:**
- ✅ CSF Function (Identify, Protect, Detect, Respond, Recover)
- ✅ CSF Category and Subcategory
- ✅ Compliance status (Compliant/Non-Compliant/Partial)
- ✅ Evidence from automated scans
- ✅ Manual governance findings
- ✅ Risk priorities

---

## Troubleshooting

### Common Issues

#### "Poetry not found"

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add to PATH (Linux/macOS)
export PATH="$HOME/.local/bin:$PATH"

# Restart your shell
exec $SHELL
```

#### "Nuclei command not found"

```bash
# Verify Go installation
go version

# Check GOPATH
echo $GOPATH

# Add Go bin to PATH
export PATH="$PATH:$(go env GOPATH)/bin"
```

#### "Module not found" errors

```bash
# Ensure you're in the Poetry environment
poetry shell

# Or prefix commands with poetry run
poetry run python tools/nuclei_scan_tool.py --help

# Clear cache and reinstall
poetry env remove python
poetry install
```

#### "Permission denied" on scans

```bash
# Create output directories if missing
mkdir -p scans output

# Fix permissions
chmod -R 755 scans/ output/
```

#### "Nuclei templates not updating"

```bash
# Force template update
nuclei -update-templates -update-template-dir ~/nuclei-templates

# Clear cache
rm -rf ~/.cache/nuclei
nuclei -update-templates
```

#### Scan produces no results

Common causes:
- **Targets unreachable**: Verify network connectivity
- **Firewall blocking**: Check firewall rules
- **Wrong profile**: Try `comprehensive` profile for broader coverage
- **Templates outdated**: Run `nuclei -update-templates`

```bash
# Test connectivity
ping scanme.nmap.org

# Run verbose scan
nuclei -u https://example.com -v
```

---

## Next Steps

Congratulations! You've completed your first CSF assessment with CSFLite.

### Learn More

- **[Usage Guide](USAGE_GUIDE.md)** *(coming soon)* - Detailed workflows and best practices
- **[Examples](EXAMPLES.md)** *(coming soon)* - Real-world assessment scenarios
- **[Tool Reference](tools/)** *(coming soon)* - Detailed tool documentation

### Explore the Mappings

- `data/nuclei_csf_lookup.json` - See how Nuclei templates map to CSF
- `data/csf_lookup.csv` - Full CSF subcategory reference
- `docs/top_25_sub_categories.md` - Understand CSFLite's focus areas

### Customize Your Assessments

- **Create custom profiles**: Edit `data/profiles.yaml`
- **Adjust mappings**: Modify `data/nuclei_csf_lookup.json`
- **Add governance items**: Extend `templates/governance_checks_template.csv`

---

## Getting Help

### Documentation

- **Project Docs**: `docs/` directory
- **Development Roadmap**: `roadmap/development_roadmap.md`

### Support

This project is in early development. For questions or issues:
1. Check existing documentation in `docs/`
2. Review the troubleshooting section above
3. Open an issue on GitHub (after v1.0 release)

---

## What's Next?

You're now ready to:
- ✅ Run assessments on your production systems
- ✅ Generate compliance evidence for audits
- ✅ Track security improvements over time
- ✅ Communicate risk to stakeholders using NIST CSF language

**Pro Tip**: Schedule regular assessments (monthly/quarterly) and track CSF compliance trends over time.

---

*Last updated: 2026-01-13*