#!/usr/bin/env python3
"""Compute stagewise coverage and miss-location accounting from event summaries."""
from __future__ import annotations
import argparse, csv, json, math
from pathlib import Path
REQUIRED=["outcome_id","future_outcome_type","future_outcome_date","source_provider","decision_schedule","outcome_horizon_days","source_observable","best_conservative_rank_within_horizon"]
def parse_bool(value,field,rownum):
    v=(value or "").strip().lower()
    if v in {"true","1","yes"}: return True
    if v in {"false","0","no"}: return False
    raise ValueError(f"row {rownum}: invalid Boolean in {field}: {value!r}")
def parse_rank(value,rownum):
    v=(value or "").strip()
    if not v: return None
    x=float(v)
    if not math.isfinite(x) or x<1: raise ValueError(f"row {rownum}: invalid rank {value!r}")
    return x
def load_rows(path):
    with Path(path).open(newline="",encoding="utf-8-sig") as fh:
        reader=csv.DictReader(fh); missing=[c for c in REQUIRED if c not in (reader.fieldnames or [])]
        if missing: raise ValueError(f"missing required columns: {missing}")
        rows=[]; seen=set()
        for n,row in enumerate(reader,start=2):
            oid=(row["outcome_id"] or "").strip()
            if not oid: raise ValueError(f"row {n}: blank outcome_id")
            if oid in seen: raise ValueError(f"row {n}: duplicate outcome_id {oid}")
            seen.add(oid); obs=parse_bool(row["source_observable"],"source_observable",n); rank=parse_rank(row["best_conservative_rank_within_horizon"],n)
            if not obs and rank is not None: raise ValueError(f"row {n}: source-unobservable outcome carries a finite rank")
            top1=None
            if "top1pct_captured" in row and (row.get("top1pct_captured") or "").strip(): top1=parse_bool(row["top1pct_captured"],"top1pct_captured",n)
            rows.append({"outcome_id":oid,"observable":obs,"rank":rank,"top1":top1})
    if not rows: raise ValueError("input contains no rows")
    return rows
def compute(rows,capacities):
    N=len(rows); NO=sum(r["observable"] for r in rows); NU=N-NO
    result={"cohort_size":N,"source_observable":NO,"source_unobservable":NU,"source_observability":NO/N,"policies":[]}
    for K in capacities:
        if K<=0: raise ValueError("capacities must be positive integers")
        captured=sum(1 for r in rows if r["observable"] and r["rank"] is not None and r["rank"]<=K)
        visible_miss=NO-captured; misses=N-captured
        result["policies"].append({"policy":f"Top-{K}","K":K,"captured":captured,"total_misses":misses,"source_unobservable_misses":NU,
        "observable_not_captured":visible_miss,"conditional_capture":captured/NO if NO else None,"full_denominator_coverage":captured/N,
        "source_stage_share_of_misses":NU/misses if misses else None,"post_source_share_of_misses":visible_miss/misses if misses else None})
    vals=[r["top1"] for r in rows if r["top1"] is not None]
    if vals and len(vals)==N:
        c=sum(vals); result["top1pct"]={"captured":c,"conditional_capture":c/NO if NO else None,"full_denominator_coverage":c/N}
    return result
def write_outputs(result,outdir):
    outdir=Path(outdir); outdir.mkdir(parents=True,exist_ok=True); (outdir/"coverage_summary.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    with (outdir/"miss_location_by_capacity.csv").open("w",newline="",encoding="utf-8") as fh:
        fields=list(result["policies"][0].keys()); w=csv.DictWriter(fh,fieldnames=fields); w.writeheader(); w.writerows(result["policies"])
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("input_csv",type=Path); ap.add_argument("--output-dir",type=Path,default=Path("coverage_output")); ap.add_argument("--capacities",type=int,nargs="+",default=[100,500,1000]); args=ap.parse_args()
    result=compute(load_rows(args.input_csv),args.capacities); write_outputs(result,args.output_dir); print(json.dumps(result,indent=2))
if __name__=="__main__": main()
