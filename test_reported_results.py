#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys, tempfile

root=Path(__file__).resolve().parent
input_path=root/"reported_public_event_input.csv.gz"

with tempfile.TemporaryDirectory() as td:
    subprocess.run(
        [sys.executable,str(root/"run_stagewise_coverage.py"),str(input_path),"--output-dir",td],
        check=True,capture_output=True,text=True
    )
    x=json.loads((Path(td)/"coverage_summary.json").read_text())

assert x["cohort_size"]==749 and x["source_observable"]==475 and x["source_unobservable"]==274
expected={100:14,500:29,1000:41}
for p in x["policies"]:
    assert p["captured"]==expected[p["K"]]
assert x["top1pct"]["captured"]==69
p=[p for p in x["policies"] if p["K"]==1000][0]
assert p["total_misses"]==708 and p["source_unobservable_misses"]==274 and p["observable_not_captured"]==434
assert abs(p["source_stage_share_of_misses"]-274/708)<1e-12
assert abs(p["post_source_share_of_misses"]-434/708)<1e-12
print("REPORTED_RESULTS_TEST: PASS")
