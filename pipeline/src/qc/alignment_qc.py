import json
import os
from pathlib import Path

BASE_DIR = Path("c:/Users/slyki/Downloads/MRDE_Antigravity_Control_Package_v3/MRDE_Antigravity_Control_Package")
OUT_RESIDUAL = BASE_DIR / "data/processed/residuals/exp001_residual_table.jsonl"
QC_REPORT = BASE_DIR / "data/processed/qc_reports/exp001_alignment_qc.json"

def run_qc():
    os.makedirs(QC_REPORT.parent, exist_ok=True)
    
    total_records = 0
    matched = 0
    missing = 0
    sxt_missing = 0
    sxt_total = 0
    station_counts = {}
    temporal_splits = {"train": 0, "validation": 0, "test": 0, "null_unknown_other": 0}
    
    with open(OUT_RESIDUAL, "r") as f:
        for line in f:
            if not line.strip(): continue
            rec = json.loads(line)
            total_records += 1
            st = rec["station_id"]
            
            if st not in station_counts:
                station_counts[st] = {"total": 0, "matched": 0, "missing": 0}
            
            station_counts[st]["total"] += 1
            if st == "SXT":
                sxt_total += 1
                
            if rec.get("residual_c") is not None:
                matched += 1
                station_counts[st]["matched"] += 1
            else:
                missing += 1
                station_counts[st]["missing"] += 1
                if st == "SXT":
                    sxt_missing += 1
                    
            split = rec.get("temporal_split")
            if split in temporal_splits:
                temporal_splits[split] += 1
            else:
                temporal_splits["null_unknown_other"] += 1

    qc_data = {
        "stage": "Phase_3_QC",
        "total_forecast_rows_processed": total_records,
        "total_matched": matched,
        "total_missing": missing,
        "temporal_splits": temporal_splits,
        "station_breakdown": station_counts,
        "sxt_proxy_risk_note": f"SXT had {sxt_missing}/{sxt_total} missing alignments. Station flagged.",
        "pass_qc": True if total_records == 43090 and temporal_splits["null_unknown_other"] == 0 else False
    }
    
    with open(QC_REPORT, "w") as f:
        json.dump(qc_data, f, indent=2)
        
    print(f"Alignment QC completed. Total processed: {total_records}. Expected: 43090.")
    print(f"Matches: {matched}, Missing: {missing}")

if __name__ == "__main__":
    run_qc()
