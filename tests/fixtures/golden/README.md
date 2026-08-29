# Golden recordings

Reference output produced by the CLI pipeline, frozen so Phase 4 has something to test against.

Phase 4 replaces the CLI with a web application and retires `governance_check.py`. The Phase 4
acceptance criterion "scoring output matches the CLI output for the same responses" cannot be
checked after that point, because nothing will produce CLI output any more. These files are that
output, recorded while the CLI still exists.

| File | Role |
|---|---|
| `governance_checklist.csv` | Input. All 25 subcategories, covering Yes, Partial and No |
| `governance_assessment.csv` | Recorded assessment output |
| `governance_heatmap.csv` | Recorded heatmap output |

`tests/test_golden_pipeline.py` runs the pipeline and compares serialised bytes, not dicts, so
number formatting, column order and row order are all covered.

## Dependencies

The recording depends on `data/csf_lookup.csv`. Reweighting a subcategory changes the expected
output and the test will fail. That is the intended behaviour, not a brittle test — spec §10 says
reweighting "requires only changing this file", and this is what makes that change visible.

## Re-recording

Only when the behaviour change is deliberate. Re-record and commit the new files in the same commit
as the change that caused it, so review sees both together.

```
poetry run python tools/governance_check.py \
  --governance_checklist tests/fixtures/golden/governance_checklist.csv \
  --governance_assessment_csv tests/fixtures/golden/governance_assessment.csv \
  --governance_heatmap tests/fixtures/golden/governance_heatmap.csv
```

Never loosen the comparison to make a failure go away.
