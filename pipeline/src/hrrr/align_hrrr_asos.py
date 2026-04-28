import json
import csv
import os
from datetime import datetime, timedelta
from pathlib import Path

# Paths
BASE_DIR = Path("c:/Users/slyki/Downloads/MRDE_Antigravity_Control_Package_v3/MRDE_Antigravity_Control_Package")
HRRR_MANIFEST = BASE_DIR / "data/processed/manifests/hrrr_extraction_manifest.jsonl"
ASOS_DIR = BASE_DIR / "data/raw/asos"
METADATA_JSON = BASE_DIR / "data/processed/station_metadata/exp001_terrain_landcover.json"
OUT_RESIDUAL = BASE_DIR / "data/processed/residuals/exp001_residual_table.jsonl"
OUT_MANIFEST = BASE_DIR / "data/processed/manifests/stage3_residual_manifest.jsonl"

WINDOW_START = datetime(2024, 6, 1, 0, 0, 0)
WINDOW_END = datetime(2024, 8, 30, 0, 0, 0)

TRAIN_END = datetime(2024, 7, 30, 23, 59, 59)
VAL_END = datetime(2024, 8, 14, 23, 59, 59)
TEST_END = datetime(2024, 8, 29, 23, 59, 59)

def get_temporal_split(dt):
    if WINDOW_START <= dt <= TRAIN_END:
        return "train"
    elif dt <= VAL_END:
        return "validation"
    elif dt <= TEST_END:
        return "test"
    return None

def load_metadata():
    with open(METADATA_JSON, "r") as f:
        meta = json.load(f)
    
    station_meta = {}
    for st in meta.get("stations", []):
        sid = st["station_id"]
        station_meta[sid] = {
            "terrain_class": st["terrain_class"],
            "elevation_mismatch_gt_50m": st.get("elevation_mismatch_gt_50m", False),
            "sxt_proxy_risk_flag": True if sid == "SXT" else False
        }
    return station_meta

def f_to_c(f_val):
    return (f_val - 32.0) * 5.0 / 9.0

def load_asos():
    asos_data = {}
    for csv_file in ASOS_DIR.glob("*.csv"):
        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                st = row["station"]
                val_str = row["valid"]
                tmpf_str = row["tmpf"]
                
                if tmpf_str == "M" or not tmpf_str:
                    continue
                try:
                    tmpf = float(tmpf_str)
                    if tmpf < -76 or tmpf > 140: # -60C to 60C
                        continue
                except ValueError:
                    continue
                
                try:
                    dt = datetime.strptime(val_str, "%Y-%m-%d %H:%M")
                except ValueError:
                    continue
                
                if st not in asos_data:
                    asos_data[st] = []
                asos_data[st].append((dt, f_to_c(tmpf)))
                
    for st in asos_data:
        asos_data[st].sort(key=lambda x: x[0])
    return asos_data

def find_closest_obs(obs_list, target_dt, max_diff_mins=10):
    closest_obs = None
    min_diff = timedelta(minutes=9999)
    for obs_dt, tmpc in obs_list:
        diff = abs(obs_dt - target_dt)
        if diff <= timedelta(minutes=max_diff_mins):
            if diff < min_diff:
                min_diff = diff
                closest_obs = (obs_dt, tmpc)
        elif obs_dt > target_dt + timedelta(minutes=max_diff_mins):
            break
    return closest_obs

def run_alignment():
    print("Loading metadata...")
    meta = load_metadata()
    print("Loading ASOS data...")
    asos_data = load_asos()
    
    os.makedirs(OUT_RESIDUAL.parent, exist_ok=True)
    os.makedirs(OUT_MANIFEST.parent, exist_ok=True)
    
    matched_count = 0
    missing_count = 0
    total_count = 0
    excluded_count = 0
    
    out_records = []
    
    print("Aligning HRRR and ASOS...")
    with open(HRRR_MANIFEST, "r") as fin, open(OUT_RESIDUAL, "w") as fout:
        for line in fin:
            if not line.strip():
                continue
            rec = json.loads(line)
            
            st = rec["station_id"]
            valid_time_str = rec["valid_time"]
            valid_dt = datetime.strptime(valid_time_str, "%Y-%m-%dT%H:%M:%SZ")
            
            # Boundary exclusion
            if valid_dt < WINDOW_START or valid_dt >= WINDOW_END:
                excluded_count += 1
                continue
                
            total_count += 1
            split = get_temporal_split(valid_dt)
            
            fcst_tmp = rec["t2m_c"]
            obs_list = asos_data.get(st, [])
            closest = find_closest_obs(obs_list, valid_dt, max_diff_mins=10)
            
            out_rec = {
                "experiment_id": "EXP001",
                "station_id": st,
                "cycle_time": rec["cycle_time"],
                "lead_time_h": rec["lead_time_h"],
                "forecast_valid_time": valid_time_str,
                "temporal_split": split,
                "forecast_t2m_c": fcst_tmp,
                "terrain_class": meta[st]["terrain_class"],
                "elevation_mismatch_gt_50m": meta[st]["elevation_mismatch_gt_50m"],
                "sxt_proxy_risk_flag": meta[st]["sxt_proxy_risk_flag"],
                "nlcd_land_cover_class": None,
                "land_cover_status": "BLOCKED_FOR_NLCD_DOWNLOAD"
            }
            
            if closest:
                obs_dt, obs_tmp = closest
                out_rec["observed_valid_time"] = obs_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                out_rec["observed_t2m_c"] = round(obs_tmp, 3)
                residual = fcst_tmp - obs_tmp
                out_rec["residual_c"] = round(residual, 3)
                out_rec["abs_residual_c"] = round(abs(residual), 3)
                matched_count += 1
            else:
                out_rec["observed_valid_time"] = None
                out_rec["observed_t2m_c"] = None
                out_rec["residual_c"] = None
                out_rec["abs_residual_c"] = None
                missing_count += 1
                
            fout.write(json.dumps(out_rec) + "\n")
            
    print(f"Excluded records (outside boundary): {excluded_count}")
    print(f"Total valid records: {total_count}")
    print(f"Matched records: {matched_count}")
    print(f"Missing records (no obs within 10 min): {missing_count}")
    
    with open(OUT_MANIFEST, "w") as fman:
        json.dump({
            "stage": "Phase_3A",
            "experiment_id": "EXP001",
            "total_valid_hrrr_forecasts": total_count,
            "excluded_forecasts": excluded_count,
            "matched_residuals": matched_count,
            "missing_observations": missing_count,
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }, fman)

if __name__ == "__main__":
    run_alignment()
