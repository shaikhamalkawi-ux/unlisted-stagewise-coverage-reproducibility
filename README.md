# Stagewise Coverage Reproducibility Package

Reproducibility repository for the manuscript:

**Before Ranking Begins: A Multi-Year Study of Coverage Loss in EPSS-Based Vulnerability Triage**

Active artifact baseline: **UNLISTED39 / Stagewise Coverage Reproducibility Package v1.1.0**.

This repository reproduces the paper's stagewise coverage and miss-location measurements from a compact derived event summary. It does **not** rank vulnerabilities and does **not** claim to predict exploitation.

## Reproduce the reported result

Python 3 standard library only:

```bash
python run_stagewise_coverage.py reported_public_event_input.csv.gz --output-dir reproduced_output
python test_reported_results.py
```

Expected locked counts:

- cohort = 749
- source-observable = 475
- source-unobservable = 274
- Top-100 / Top-500 / Top-1000 capture = 14 / 29 / 41
- Top-1% capture = 69
- Top-1000 misses = 708
- source-stage misses = 274
- observable but not captured = 434

The original uncompressed derived input is 72,318 bytes with SHA-256:

`10a9d3c4b0e53511d017afb567cf45798e63f97228902b6ea703c9b1f7ecd762`

The repository stores the same input as `reported_public_event_input.csv.gz`.

## Interpretation boundary

- Outcome = future CISA KEV admission, not exploit onset.
- Source absence = absence from the declared historical EPSS path.
- Selection != remediation or enterprise risk reduction.
- The 38.70% / 61.30% miss split is pipeline-location accounting, not causal attribution.
- The public event summary reproduces the stagewise accounting only; it is not the complete 174-snapshot replication archive.

## Repository contents

- `run_stagewise_coverage.py` — reference implementation
- `test_reported_results.py` — locked-result regression test
- `reported_public_event_input.csv.gz` — compressed derived 749-event public accounting input
- `event_summary_schema.csv/.json` — compact event-summary schema
- `full_decision_record_schema.csv` — fuller decision-record specification
- `enterprise_adapter_template.csv` — empty enterprise extension template
- `reported_output/` — expected outputs
- `REPRODUCTION_STDOUT.json` — expected console result
- `TEST_STATUS.txt` — package test status
- `CITATION.cff` — citation metadata
- `LICENSE.txt` — MIT license
- `THIRD_PARTY_DATA_NOTICE.md` — third-party source notice

## Fail-closed behavior

The implementation rejects incomplete or internally inconsistent input rather than returning a partial result, including missing required columns, duplicate outcome IDs, invalid Boolean fields, non-positive capacities, empty input, and source-unobservable outcomes carrying finite ranks.

## Enterprise-field context

The enterprise template is intentionally empty. Product documentation shows that relevant lifecycle fields can exist in enterprise exports; this establishes field availability, not field validation:

- Tenable: https://docs.tenable.com/vulnerability-management/Content/Explore/findings-columns.htm
- Tenable export keys: https://docs.tenable.com/vulnerability-management/Content/Explore/export-findings-csv-keys.htm
- Rapid7 bulk export: https://docs.rapid7.com/insightvm/bulk-export-api/
- Rapid7 vulnerability workflow: https://docs.rapid7.com/insightvm/working-with-vulnerabilities/
- Qualys vulnerability status: https://docs.qualys.com/en/vm/latest/scans/vulnerability_status.htm

## Verification status

Clean local execution before repository publication:

`REPORTED_RESULTS_TEST: PASS`
