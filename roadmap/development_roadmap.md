# CSFLite Roadmap

**Vision:** Bridge security strategy ↔ implementation for SMEs by turning raw vuln data into NIST CSF v2.0–aligned governance guide — fast.

## Versioning
SemVer. Minor releases can add features; patch = fixes only. CLI flags marked “experimental” may change in minors.
S
---

##
**v0.1.0-alpha**
- ✅ MVP CLI (fixed data paths) → `data/mock_heatmap.csv`
- ✅ Top-25 CSF subcategories with weights
- ✅ Initial `nuclei-csf` index (≥30 mappings)
- ✅ Tests: multi-map & severity precedence
- ✅ CI: black/ruff/bandit/pytest green
- ✅ README Quickstart + sample output
- ✅ License: **MIT**
## Quickstart (MVP)

Configurable CLI flags (--scan/--lookup/--index/--out) arrive in v0.2.


**TO-DO ASAP**
- CLI flags: `--scan/--lookup/--index/--out`
- Config file support (`csf_lite.toml`) + env overrides
- PDF exporter (simple Python HTML→PDF or wkhtmltopdf)

**FUTURE DEVELOPMENTS**
- Industry profiles (weights): SaaS, Finlite, Agency
- Governance checks expanded to Top-25 with remediations
- Better logging + `--verbose`
- Packaging polish; pre-release to PyPI (optional)