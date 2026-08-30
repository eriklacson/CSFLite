repo: eriklacson/CSFLite
branch: master

## Last sync
date: 2026-08-30T08:04:40Z

### Updated in this project
- Built the single-tenant web questionnaire replacing the CSV + CLI flow
- Embedded the core 25 governance questions with their heatmap weights
- Embedded the SOC 2 (28q) and HIPAA (9q) supplement questionnaires
- Reproduced the scoring/severity logic and CSV export shapes

## Screen map
| Screen | Built from |
| --- | --- |
| Scope / start | README.md, templates/*.csv |
| Core questionnaire | templates/governance_checks_template.csv, data/heat_map_lookup.csv |
| SOC 2 supplement | templates/soc2-supplement-questionnaire.csv |
| HIPAA supplement | templates/hipaa-supplement-questionnaire.csv |
| Results + export | tools/assess_helpers.py, output/examples/governance_assessment/*.csv |
