# Stagewise Coverage Reproducibility Package

This repository reproduces the paper's stagewise coverage and miss-location measurements from a compact event summary. It does not rank vulnerabilities and does not claim to predict exploitation.

## Accompanying manuscript

**Before Ranking Begins: A Multi-Year Study of Coverage Loss in EPSS-Based Vulnerability Triage**

Active reproducibility baseline: **UNLISTED39 / Stagewise Coverage Reproducibility Package v1.1.0**

## Reproduce the reported public result

```bash
python run_stagewise_coverage.py reported_public_event_input.csv --output-dir reproduced_output
python test_reported_results.py
```

Expected counts:

- 749 outcomes
- 475 source-observable
- 274 source-unobservable
- Top-100 / Top-500 / Top-1000 capture = 14 / 29 / 41
- Top-1% capture = 69
- Top-1000 misses = 708
- 274 misses outside the eligible source population
- 434 source-observable but not captured

The implementation uses the Python 3 standard library only and fails closed on incomplete or internally inconsistent input.

## Interpretation boundary

The outcome is future CISA KEV admission, not exploit onset. Source absence means absence from the declared historical EPSS path. Selection is not remediation or enterprise risk reduction. The 38.70% / 61.30% miss split is pipeline-location accounting, not causal attribution.

## Repository structure

- `run_stagewise_coverage.py` — reference implementation
- `test_reported_results.py` — locked-result regression test
- `reported_public_event_input.csv` — derived 749-event public accounting input
- `event_summary_schema.csv/.json` — compact event-summary schema
- `full_decision_record_schema.csv` — fuller decision-record specification
- `enterprise_adapter_template.csv` — empty enterprise extension template
- `reported_output/` — expected reported outputs
- `SHA256SUMS.csv` — integrity manifest
- `CITATION.cff` — citation metadata
- `LICENSE.txt` — MIT license
- `THIRD_PARTY_DATA_NOTICE.md` — source-data notice

## Enterprise-field context

Current product documentation indicates that enterprise exports can carry relevant lifecycle fields. These sources establish field availability, not scientific validation:

- Tenable findings columns: https://docs.tenable.com/vulnerability-management/Content/Explore/findings-columns.htm
- Tenable CSV export keys: https://docs.tenable.com/vulnerability-management/Content/Explore/export-findings-csv-keys.htm
- Rapid7 bulk export API: https://docs.rapid7.com/insightvm/bulk-export-api/
- Rapid7 vulnerability workflow: https://docs.rapid7.com/insightvm/working-with-vulnerabilities/
- Qualys vulnerability status: https://docs.qualys.com/en/vm/latest/scans/vulnerability_status.htm

## Reproducibility status

Local clean execution before repository publication:

`REPORTED_RESULTS_TEST: PASS`
