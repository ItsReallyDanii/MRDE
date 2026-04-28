"""
MRDE EXP001 — HRRR 2m Temperature Extraction (Zarr backend)
Stage 2 Phase 2D

Uses hrrrzarr on AWS S3 (no eccodes/cfgrib required).
Extracts TMP:2m at 5 locked stations, all cycle times in the EXP001 window,
lead times 1h, 3h, 6h, 12h.

Strategy:
- Pre-compute nearest grid (row, col) for each station from the HRRR_chunk_index.
- For each (date, cycle_hour), open the fcst.zarr store (lazy/remote).
- Slice out TMP at (lead_idx, row, col) for each station — single element reads.
- Append to JSONL manifest incrementally (resumable).
- No raw grib2 files downloaded or retained.

FORBIDDEN: no residuals, no ASOS alignment, no mismatch columns.
"""
import json
import os
import threading
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone

import numpy as np
import s3fs
import yaml
import zarr

warnings.filterwarnings("ignore", category=UserWarning)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_REPO = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
MANIFEST_DIR = os.path.join(_REPO, "data", "processed", "manifests")
EXTRACT_MANIFEST = os.path.join(MANIFEST_DIR, "hrrr_extraction_manifest.jsonl")
ERROR_LOG = os.path.join(MANIFEST_DIR, "hrrr_extraction_errors.jsonl")
STATIONS_FILE = os.path.join(_REPO, "pipeline", "config", "exp001_stations.yaml")

# ---------------------------------------------------------------------------
# EXP001 locked parameters
# ---------------------------------------------------------------------------
WINDOW_START = datetime(2024, 6, 1, 0, 0, 0, tzinfo=timezone.utc)
WINDOW_END_EXCL = datetime(2024, 8, 30, 0, 0, 0, tzinfo=timezone.utc)
LEAD_TIMES = [1, 3, 6, 12]       # fxx hours
MAX_WORKERS = 8                   # parallel cycle/lead extractions
ZARR_BASE = "hrrrzarr/sfc"
GRID_ZARR = "hrrrzarr/grid/HRRR_chunk_index.zarr"


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------
_write_lock = threading.Lock()


def append_jsonl(path: str, entry: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with _write_lock:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def load_stations() -> list[dict]:
    with open(STATIONS_FILE, "r") as f:
        cfg = yaml.safe_load(f)
    return [
        {"station_id": s["station_id"], "lat": s["latitude"], "lon": s["longitude"]}
        for s in cfg["stations"]
    ]


def load_done_keys() -> set:
    done = set()
    if not os.path.exists(EXTRACT_MANIFEST):
        return done
    with open(EXTRACT_MANIFEST, "r", encoding="utf-8") as f:
        for line in f:
            try:
                e = json.loads(line)
                done.add((e["cycle_time"], e["lead_time_h"], e["station_id"]))
            except Exception:
                pass
    return done


# ---------------------------------------------------------------------------
# One-time grid index computation
# ---------------------------------------------------------------------------
def build_station_grid_index(stations: list[dict], fs: s3fs.S3FileSystem) -> dict:
    """
    For each station, find the nearest HRRR grid (row, col) using
    hrrrzarr/grid/HRRR_chunk_index.zarr which stores full lat/lon for every
    grid point.
    Returns: {station_id: {'row': int, 'col': int, 'grid_lat': float, 'grid_lon': float}}
    """
    print("  Loading HRRR grid coordinates (one-time)...")
    store = s3fs.S3Map(GRID_ZARR, s3=fs)
    ci = zarr.open(store, mode="r")
    lat2d = ci["latitude"][:]   # shape (1059, 1799)
    lon2d = ci["longitude"][:]  # shape (1059, 1799)

    idx_map = {}
    for stn in stations:
        dist2 = (lat2d - stn["lat"]) ** 2 + (lon2d - stn["lon"]) ** 2
        flat_k = int(dist2.argmin())
        row, col = np.unravel_index(flat_k, lat2d.shape)
        idx_map[stn["station_id"]] = {
            "row": int(row),
            "col": int(col),
            "grid_lat": round(float(lat2d[row, col]), 5),
            "grid_lon": round(float(lon2d[row, col]), 5),
        }
        print(
            f"    {stn['station_id']}: row={row} col={col} "
            f"lat={lat2d[row,col]:.4f} lon={lon2d[row,col]:.4f}"
        )
    return idx_map


# ---------------------------------------------------------------------------
# Per-cycle extraction
# ---------------------------------------------------------------------------
def extract_cycle(
    cycle_dt: datetime,
    fxx_list: list[int],
    idx_map: dict,
    stations: list[dict],
    done_keys: set,
    fs: s3fs.S3FileSystem,
) -> tuple[int, int]:
    """
    Open one fcst.zarr store, extract TMP at requested lead times for all stations.
    Returns (success_count, fail_count).
    """
    date_str = cycle_dt.strftime("%Y%m%d")
    hour_str = cycle_dt.strftime("%H")
    cycle_iso = cycle_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    zarr_key = f"{ZARR_BASE}/{date_str}/{date_str}_{hour_str}z_fcst.zarr"
    access_time = datetime.now(timezone.utc).isoformat()

    # Check if all requested fxx/stations are already done
    needed = [
        (fxx, s["station_id"])
        for fxx in fxx_list
        for s in stations
        if (cycle_iso, fxx, s["station_id"]) not in done_keys
    ]
    if not needed:
        return 0, 0

    try:
        store = s3fs.S3Map(zarr_key, s3=fs)
        z = zarr.open(store, mode="r")
        tmp_arr = z["2m_above_ground/TMP/2m_above_ground/TMP"]
        # shape: (48, 1059, 1799) — lead_index is fxx-1 (f01 → index 0)
        fp = z["2m_above_ground/TMP/forecast_period"][:]  # hours: [1, 2, ..., 48]
    except Exception as exc:
        for fxx, sid in needed:
            append_jsonl(
                ERROR_LOG,
                {
                    "cycle": cycle_iso, "fxx": fxx, "station": sid,
                    "error": f"zarr open: {exc}",
                    "ts": access_time,
                },
            )
        return 0, len(needed)

    success = fail = 0
    for fxx in fxx_list:
        valid_dt = cycle_dt + timedelta(hours=fxx)
        valid_iso = valid_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Find lead index in forecast_period array
        lead_idx_arr = np.where(fp == fxx)[0]
        if len(lead_idx_arr) == 0:
            for s in stations:
                if (cycle_iso, fxx, s["station_id"]) in done_keys:
                    continue
                append_jsonl(
                    ERROR_LOG,
                    {"cycle": cycle_iso, "fxx": fxx, "error": f"fxx={fxx} not in forecast_period", "ts": access_time},
                )
                fail += 1
            continue
        lead_idx = int(lead_idx_arr[0])

        for stn in stations:
            if (cycle_iso, fxx, stn["station_id"]) in done_keys:
                continue
            grid = idx_map[stn["station_id"]]
            try:
                t2m_k = float(tmp_arr[lead_idx, grid["row"], grid["col"]])
                t2m_c = round(t2m_k - 273.15, 3)
                append_jsonl(
                    EXTRACT_MANIFEST,
                    {
                        "log_schema_version": "1.1",
                        "entry_type": "hrrr_forecast_point",
                        "experiment_id": "EXP001",
                        "stage": "Phase_2D",
                        "station_id": stn["station_id"],
                        "cycle_time": cycle_iso,
                        "lead_time_h": fxx,
                        "valid_time": valid_iso,
                        "grid_lat": grid["grid_lat"],
                        "grid_lon": grid["grid_lon"],
                        "t2m_c": t2m_c,
                        "source_zarr": zarr_key,
                        "access_time": access_time,
                    },
                )
                success += 1
            except Exception as exc:
                append_jsonl(
                    ERROR_LOG,
                    {
                        "cycle": cycle_iso, "fxx": fxx,
                        "station": stn["station_id"],
                        "error": str(exc), "ts": access_time,
                    },
                )
                fail += 1

    return success, fail


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    import sys
    test_mode = "--test" in sys.argv

    print("=" * 60)
    print("MRDE EXP001 Phase 2D: HRRR 2m Temp Extraction (Zarr)")
    print("=" * 60)
    os.makedirs(MANIFEST_DIR, exist_ok=True)

    fs = s3fs.S3FileSystem(anon=True)
    stations = load_stations()
    print(f"Stations: {[s['station_id'] for s in stations]}")

    idx_map = build_station_grid_index(stations, fs)
    done_keys = load_done_keys()
    print(f"Already extracted: {len(done_keys)} station-cycle-fxx records")

    # Build list of cycle datetimes
    cycles = []
    t = WINDOW_START
    while t < WINDOW_END_EXCL:
        cycles.append(t)
        t += timedelta(hours=1)

    if test_mode:
        cycles = cycles[:3]
        print(f"[TEST MODE] Running {len(cycles)} cycles only")

    total_cycles = len(cycles)
    print(f"Cycles to process: {total_cycles}  workers={MAX_WORKERS}")

    total_ok = total_fail = 0

    def job(cycle_dt):
        return extract_cycle(cycle_dt, LEAD_TIMES, idx_map, stations, done_keys, fs)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(job, c): c for c in cycles}
        for i, fut in enumerate(as_completed(futures), 1):
            ok, fail = fut.result()
            total_ok += ok
            total_fail += fail
            if i % 200 == 0 or i == total_cycles:
                print(
                    f"  Cycles {i}/{total_cycles} | "
                    f"records ok={total_ok} fail={total_fail}"
                )

    print(f"\nExtraction complete: ok={total_ok}  fail={total_fail}")
    print(f"Manifest: {EXTRACT_MANIFEST}")


if __name__ == "__main__":
    main()
