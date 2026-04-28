import json
import os
import math
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path("c:/Users/slyki/Downloads/MRDE_Antigravity_Control_Package_v3/MRDE_Antigravity_Control_Package")
OUT_RESIDUAL = BASE_DIR / "data/processed/residuals/exp001_residual_table.jsonl"
BASELINE_METRICS = BASE_DIR / "data/processed/baselines/exp001_baseline_metrics.json"

def compute_metrics(errors):
    if not errors:
        return {"mae": None, "rmse": None, "bias": None, "n": 0}
    bias = sum(errors) / len(errors)
    mae = sum(abs(e) for e in errors) / len(errors)
    rmse = math.sqrt(sum(e*e for e in errors) / len(errors))
    return {"mae": round(mae, 3), "rmse": round(rmse, 3), "bias": round(bias, 3), "n": len(errors)}

def run_baselines():
    os.makedirs(BASELINE_METRICS.parent, exist_ok=True)
    
    obs_dict = {}
    records = []
    
    with open(OUT_RESIDUAL, "r") as f:
        for line in f:
            if not line.strip(): continue
            rec = json.loads(line)
            records.append(rec)
            
            if rec["observed_t2m_c"] is not None:
                vt = datetime.strptime(rec["forecast_valid_time"], "%Y-%m-%dT%H:%M:%SZ")
                obs_dict[(rec["station_id"], vt)] = rec["observed_t2m_c"]
                
    # 1. Training Phase: Compute bias offsets strictly on train split
    station_bias_sum = defaultdict(float)
    station_bias_count = defaultdict(int)
    
    lts_bias_sum = defaultdict(float)
    lts_bias_count = defaultdict(int)
    
    for rec in records:
        if rec["residual_c"] is None: continue
        if rec.get("temporal_split") != "train":
            continue
            
        vt = datetime.strptime(rec["forecast_valid_time"], "%Y-%m-%dT%H:%M:%SZ")
        st = rec["station_id"]
        res = rec["residual_c"] # forecast - observed
        lt = rec["lead_time_h"]
        tod_bin = vt.hour # 0-23
        
        station_bias_sum[st] += res
        station_bias_count[st] += 1
        
        lts_bias_sum[(st, lt, tod_bin)] += res
        lts_bias_count[(st, lt, tod_bin)] += 1
        
    station_biases = {st: station_bias_sum[st] / station_bias_count[st] for st in station_bias_count}
    lts_biases = {str((st, lt, tod_bin)): lts_bias_sum[(st, lt, tod_bin)] / lts_bias_count[(st, lt, tod_bin)] for (st, lt, tod_bin) in lts_bias_count}
    
    # 2. Evaluation Phase
    eval_errors = {
        "train": {"raw": [], "pers": [], "st_bias": [], "lts_bias": []},
        "validation": {"raw": [], "pers": [], "st_bias": [], "lts_bias": []},
        "test": {"raw": [], "pers": [], "st_bias": [], "lts_bias": []}
    }
    
    for rec in records:
        if rec["observed_t2m_c"] is None: continue
        split = rec.get("temporal_split")
        if not split or split not in eval_errors: continue
        
        vt = datetime.strptime(rec["forecast_valid_time"], "%Y-%m-%dT%H:%M:%SZ")
        st = rec["station_id"]
        lt = rec["lead_time_h"]
        tod_bin = vt.hour
        
        obs = rec["observed_t2m_c"]
        fcst = rec["forecast_t2m_c"]
        
        # raw hrrr
        eval_errors[split]["raw"].append(fcst - obs)
        
        # persistence
        prev_vt = vt - timedelta(hours=lt)
        prev_obs = obs_dict.get((st, prev_vt))
        if prev_obs is not None:
            eval_errors[split]["pers"].append(prev_obs - obs)
            
        # station bias
        st_bias = station_biases.get(st, 0.0)
        eval_errors[split]["st_bias"].append((fcst - st_bias) - obs)
        
        # lts bias
        lts_key = (st, lt, tod_bin)
        lts_bias = station_bias_sum[st] / station_bias_count[st] if st in station_bias_count else 0.0 # fallback
        if lts_key in lts_bias_count:
            lts_bias = lts_bias_sum[lts_key] / lts_bias_count[lts_key]
        eval_errors[split]["lts_bias"].append((fcst - lts_bias) - obs)
        
    metrics_by_split = {}
    for split, errs in eval_errors.items():
        metrics_by_split[split] = {
            "raw_hrrr_forecast": compute_metrics(errs["raw"]),
            "persistence_baseline": compute_metrics(errs["pers"]),
            "station_wise_mean_bias_baseline": compute_metrics(errs["st_bias"]),
            "lead_time_time_of_day_station_bias_baseline": compute_metrics(errs["lts_bias"])
        }
    
    # Save output
    out_data = {
        "stage": "Phase_3_Baselines",
        "metrics_by_split": metrics_by_split,
        "trained_biases": {
            "station_biases": station_biases,
            "lts_biases_count": len(lts_biases)
        }
    }
    
    with open(BASELINE_METRICS, "w") as f:
        json.dump(out_data, f, indent=2)
        
    print("Baseline metrics computed.")
    for split, met in metrics_by_split.items():
        print(f"\n[{split.upper()}]")
        for k, v in met.items():
            print(f"  {k}: {v}")

if __name__ == "__main__":
    run_baselines()
