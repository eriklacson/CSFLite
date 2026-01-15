# Nuclei to NIST CSF v2.0 Rule-Based Mapping

## Overview

This document describes the deterministic, rule-based mapping system for transforming Nuclei security findings into NIST Cybersecurity Framework (CSF) v2.0 subcategory mappings.

## Architecture

### Components

1. **CSF Rule Mapper (`tools/csf_rule_mapper.py`)**
   - Core mapping engine
   - Processes findings using rule-based logic
   - Enriches results with CSF metadata

2. **Nuclei JSON Converter (`tools/nuclei_json_converter.py`)**
   - Converts raw Nuclei output to standardized format
   - Preserves template tags for rule matching

3. **CLI Tool (`tools/nuclei_csf_mapper_tool.py`)**
   - Command-line interface for batch processing
   - Supports CSV, JSON, and JSONL output

4. **Mapping Rules (`data/mapping_rules.yaml`)**
   - Declarative rule definitions
   - Template-specific overrides

## Data Flow

```
Raw Nuclei Output (JSON/JSONL)
    ↓
nuclei_json_converter.py
    ↓ (preserves tags)
Converted Findings
    ↓
csf_rule_mapper.py
    ↓ (applies rules + overrides + enrichment)
Mapped CSF Records (CSV/JSONL/JSON)
```

## Input Format

### Raw Nuclei Finding

```json
{
  "template-id": "tls-version",
  "host": "example.com",
  "matched-at": "example.com:443",
  "timestamp": "2025-01-01T00:00:00Z",
  "info": {
    "name": "TLS Version - Detect",
    "severity": "medium",
    "tags": ["ssl", "tls"],
    "description": "TLS version detection"
  }
}
```

### Converted Finding (Intermediate)

```json
{
  "templateID": "tls-version",
  "host": "example.com",
  "matched-at": "example.com:443",
  "severity": "medium",
  "timestamp": "2025-01-01T00:00:00Z",
  "matcher-name": "TLS Version - Detect",
  "description": "TLS version detection",
  "tags": ["ssl", "tls"]
}
```

## Output Format

### Mapped CSF Record

```json
{
  "timestamp": "2025-01-01T00:00:00Z",
  "host": "example.com",
  "templateID": "tls-version",
  "severity": "medium",
  "matcher_name": "TLS Version - Detect",
  "description": "TLS version detection",
  "subcat_id": "PR.IR-01",
  "confidence": "High",
  "rationale": "Transport security (TLS/HSTS/Headers): TLS config + secure transport signals",
  "csf_function": "Protect",
  "csf_subcategory_name": "Communications and control networks are protected",
  "weight": 1.2,
  "recommendation": "Disable insecure protocols and enforce TLS 1.2+"
}
```

## Mapping Logic

### Rule Matching

Rules are evaluated in order. Each rule specifies conditions (`when`) and mappings (`map`):

```yaml
- name: "Transport security (TLS/HSTS/Headers)"
  when:
    any_tag: [ssl, tls, hsts, headers]
    min_severity: medium
  map:
    csf_subcats: [PR.IR-01]
    confidence: High
    rationale: "TLS config + secure transport signals"
```

**Conditions:**
- `any_tag`: At least one tag must match
- `all_tag`: All tags must be present
- `min_severity`: Minimum severity level (info < low < medium < high < critical)

**Result:**
- Finding matches if ALL conditions are met
- Multiple rules can match a single finding
- Each matched rule generates one or more CSF subcategory mappings

### Override Precedence

Template-specific overrides take precedence over rules:

```yaml
overrides:
  - template_id: networking/open-ports
    csf_subcats: [ID.AM-02, ID.AM-03, DE.CM-01]
    confidence: Medium
    rationale: "Open ports discovery evidences inventory/flows"
```

If a finding's `templateID` matches an override, **only** the override is applied (rules are skipped).

### CSF Function Enrichment

Each subcategory ID is enriched with metadata from `csf_lookup.csv`:

| Subcategory ID | CSF Function | Name | Weight | Recommendation |
|----------------|--------------|------|--------|----------------|
| PR.IR-01 | Protect | Communications and control networks are protected | 1.2 | Disable insecure protocols and enforce TLS 1.2+ |

The CSF Function is extracted from the subcategory prefix:
- `ID.*` → Identify
- `PR.*` → Protect
- `DE.*` → Detect
- `RS.*` → Respond
- `RC.*` → Recover
- `GV.*` → Govern

### Template Cache (Optional)

If findings lack tags, a template cache can enrich them:

```json
{
  "tls-version": {
    "tags": ["ssl", "tls"],
    "severity": "info"
  }
}
```

The mapper looks up the `templateID` and uses cached tags if missing from the finding.

## Usage

### CLI Tool

```bash
python tools/nuclei_csf_mapper_tool.py \
  --input scans/nuclei_converted.json \
  --output-csv output/csf_mapped.csv \
  --output-jsonl output/csf_mapped.jsonl \
  --mapping-rules data/mapping_rules.yaml \
  --csf-lookup data/csf_lookup.csv \
  --verbose
```

**Options:**
- `--input`: Input file (JSON or JSONL)
- `--output-csv`: Output CSV file
- `--output-jsonl`: Output JSONL file
- `--output-json`: Output JSON file
- `--mapping-rules`: Path to mapping_rules.yaml (default: `data/mapping_rules.yaml`)
- `--csf-lookup`: Path to csf_lookup.csv (default: `data/csf_lookup.csv`)
- `--template-cache`: Optional template cache JSON
- `--verbose`: Enable detailed output

### Python API

```python
from tools.csf_rule_mapper import CSFRuleMapper

# Initialize mapper
mapper = CSFRuleMapper(
    mapping_rules_path="data/mapping_rules.yaml",
    csf_lookup_path="data/csf_lookup.csv"
)

# Map a single finding
finding = {
    "templateID": "tls-version",
    "host": "example.com",
    "severity": "medium",
    "tags": ["ssl", "tls"]
}

results = mapper.map_finding(finding)

# Map multiple findings
findings = [...]
all_results = mapper.map_findings(findings)
```

### Integration with assess.py

```python
from tools.assess_helpers import map_scan_to_csf_rules

# Load findings
findings = read_scan_json("output/nuclei_converted.json")

# Map using rules
mapped = map_scan_to_csf_rules(
    findings,
    mapping_rules_path="data/mapping_rules.yaml",
    csf_lookup_path="data/csf_lookup.csv"
)
```

## Configuration

### Adding New Rules

Edit `data/mapping_rules.yaml`:

```yaml
rules:
  - name: "Your Rule Name"
    when:
      any_tag: [tag1, tag2]
      min_severity: medium
    map:
      csf_subcats: [PR.AA-01, PR.AA-03]
      confidence: High
      rationale: "Explanation of why this mapping makes sense"
```

### Adding New Overrides

```yaml
overrides:
  - template_id: your/template-id
    csf_subcats: [ID.AM-02]
    confidence: Medium
    rationale: "Specific reason for this template"
```

### Adding CSF Subcategories

Edit `data/csf_lookup.csv`:

```csv
csf_subcategory_id,csf_name,weight,recommendation
PR.AA-01,Identities and credentials are managed,1.5,Enforce strong password policies and implement MFA.
```

## Testing

### Unit Tests

```bash
python -m pytest tests/test_csf_rule_mapper.py -v
```

### Integration Tests

```bash
python -m pytest tests/test_integration_csf_mapping.py -v
```

### Manual Testing

```bash
# Convert raw Nuclei output
python tools/nuclei_convert_tool.py \
  --input scans/nuclei_raw_sample.json \
  --output output/nuclei_converted_test.json

# Map to CSF
python tools/nuclei_csf_mapper_tool.py \
  --input output/nuclei_converted_test.json \
  --output-csv output/test_mapped.csv \
  --output-jsonl output/test_mapped.jsonl \
  --verbose
```

## Output Formats

### CSV

Flat table format suitable for spreadsheets and reporting:

```csv
timestamp,host,templateID,severity,subcat_id,csf_function,confidence,...
2025-01-01T00:00:00Z,example.com,tls-version,medium,PR.IR-01,Protect,High,...
```

### JSONL (Newline-Delimited JSON)

One JSON object per line, suitable for streaming and log processing:

```jsonl
{"timestamp": "...", "host": "...", "subcat_id": "PR.IR-01", ...}
{"timestamp": "...", "host": "...", "subcat_id": "ID.AM-02", ...}
```

### JSON

Standard JSON array format:

```json
[
  {"timestamp": "...", "subcat_id": "PR.IR-01", ...},
  {"timestamp": "...", "subcat_id": "ID.AM-02", ...}
]
```

## Example Workflows

### Basic Workflow

```bash
# Step 1: Run Nuclei scan
nuclei -u https://example.com -o scans/raw_output.json -json

# Step 2: Convert to CSFLite format (with tags)
python tools/nuclei_convert_tool.py \
  --input scans/raw_output.json \
  --output output/converted.json

# Step 3: Map to CSF
python tools/nuclei_csf_mapper_tool.py \
  --input output/converted.json \
  --output-csv output/csf_mapped.csv \
  --output-jsonl output/csf_mapped.jsonl
```

### With Template Cache

```bash
# Create template cache from Nuclei templates
# (This is optional but helpful when findings lack tags)

python tools/nuclei_csf_mapper_tool.py \
  --input output/converted.json \
  --output-csv output/csf_mapped.csv \
  --template-cache data/nuclei_template_cache.json
```

## Design Principles

1. **Determinism**: Same input → same output (no randomness)
2. **Transparency**: All mappings have explicit rationales
3. **Extensibility**: Easy to add new rules and overrides
4. **Confidence Tracking**: Mappings include confidence levels (Low/Medium/High)
5. **Multi-Mapping**: One finding can map to multiple CSF subcategories
6. **Enrichment**: Results include full CSF metadata for downstream analysis

## Confidence Levels

| Level | Meaning |
|-------|---------|
| **High** | Direct, well-established mapping (e.g., TLS findings → PR.IR-01) |
| **Medium** | Reasonable inference (e.g., tech fingerprinting → ID.AM-02) |
| **Low** | Indirect or partial signal (e.g., CVE as threat intel → ID.RA-01) |

## Limitations

- **Out of Scope**: This module handles mapping only. It does NOT:
  - Run Nuclei scans
  - Generate coverage metrics
  - Provide remediation workflows
  - Integrate with CI/CD (handled separately)

- **Tag Dependency**: Mapping quality depends on Nuclei templates having accurate tags
- **Manual Tuning**: Rules may need adjustment based on organizational risk priorities

## References

- [NIST CSF v2.0 Framework](https://www.nist.gov/cyberframework)
- [Nuclei Templates](https://github.com/projectdiscovery/nuclei-templates)
- CSFLite Documentation: `docs/automatable_sub_categories.md`
