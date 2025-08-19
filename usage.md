# CSFLite — Usage Guide

## Getting Started

### Requirements

* Python **3.10+**
* Git

### Install
```bash
# clone
git clone https://github.com/eriklacson/CSFLite.git
cd CSFLite

# install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3

# install dependencies and set up virtualenv
poetry install --with dev

# activate the virtual environment
poetry shell
```

---

## Quickstart (MVP)

This version only supports ***nuclie scan results*** and uses **default paths in `./data`**.

```bash
python nuc2csf.py
```

It will **read**:

```
data/mock_scan_output.json
data/nuclei-csf-index.csv
data/csf_lookup.csv
```

…and **write**:

```
output/heatmap.csv
```

> Configurable CLI flags (`--scan/--lookup/--index/--out`) arrive in **v0.2**.
> Until then, keep your inputs in `./data` using the file names above.

---

## What the tool produces

### Output file: `data/heatmap.csv`

**Columns:**

| Column           | Meaning                                              |        |      |             |
| ---------------- | ---------------------------------------------------- | ------ | ---- | ----------- |
| `subcat_id`      | NIST CSF v2.0 subcategory ID (e.g., `PR.AC-01`)      |        |      |             |
| `name`           | Subcategory name                                     |        |      |             |
| `count`          | Number of mapped findings affecting this subcategory |        |      |             |
| `max_severity`   | Highest severity found for the subcategory (`low`, `medium`, `high`, `critical`) |
| `weighted_score` | `weight * (max_sev_weight + ln(1 + count))`          |        |      |             |

**Severity weights (MVP default):**
`low=1 · medium=3 · high=6 · critical=10`

> `weight` comes from `data/csf_lookup.csv` and lets you tune importance per subcategory (e.g., industry bias).

**Example (first 5 rows):**

```csv
subcat_id,name,count,max_severity,weighted_score
PR.AC-01,Access to assets is managed,3,high,9.48
DE.AE-02,Detected events are analysed,1,medium,3.30
PR.DS-01,Data-at-rest is protected,2,critical,12.69
ID.AM-01,Asset inventory is maintained,4,medium,5.79
PR.PS-01,Personnel security policies,1,low,1.69
```

---

## How mapping works (MVP)

1. **Scan output** – `data/mock_scan_output.json` holds findings with `template_id` and `severity`.
2. **Template → CSF mapping** – `data/nuclei-csf-index.csv` maps each Nuclei template to one or more CSF subcategories (`subcat_ids` supports multiple IDs separated by `;`).
3. **Aggregation** – findings are “exploded” across mapped subcategories; each subcategory tallies `count`, chooses the **max severity**, and computes `weighted_score`.
4. **Lookup** – `data/csf_lookup.csv` supplies names and per-subcategory `weight`.

**Unmapped templates:** If a finding’s `template_id` isn’t in the index, it’s ignored in MVP (logged in future versions).

---

## Governance checks (manual)

See `docs/governance_checks.md` for 10 “lite” checks aligned to the top CSF subcategories (each includes a one-line remediation). Use these alongside the heat-map to suggest first actions.

---

## Exporting a 1-page PDF (temporary workflow)

Until the built-in PDF exporter lands:

1. Import `data/mock_heatmap.csv` into the provided Google Sheet template (link in `examples/` or README).
2. The sheet color-codes by severity and shows a compact matrix.
3. **File → Download → PDF** (A4/Letter).
4. Add a short “Top 3 fixes” box before sending to stakeholders.

The native **PDF exporter** ships in **v0.2**.

---

## Troubleshooting

* **`FileNotFoundError: data/...`**
  Make sure the three inputs exist in `./data` with the exact names listed above.

* **CSV looks empty / few rows**
  Confirm your `template_id` values in `mock_scan_output.json` match entries in `nuclei-csf-index.csv`. Start with a small set you’re confident in.


