"""
MRDE EXP001 -- Phase 2E: Build Terrain and Land Cover Metadata
Stage 2 Phase 2E

Driver script that assembles station_metadata/exp001_terrain_landcover.json
by combining:
  - Station coordinates from pipeline/config/exp001_stations.yaml
  - HRRR grid coordinates from data/processed/manifests/hrrr_extraction_manifest.jsonl
  - Elevation from local DEM or online USGS EPQS
  - NLCD 2021 class from local NLCD (Online is BLOCKED)

Modes:
  --dry-run               Validate inputs, print plan.
  --online                Use USGS EPQS for elevation. (NLCD will block).
  --elevation-raster PATH Elevation raster.
  --nlcd-raster PATH      NLCD 2021 raster.
  --output PATH           Override default output path.

FORBIDDEN: no raster downloads, no residuals, no ASOS-HRRR alignment.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone
import urllib.error

import yaml

# ---------------------------------------------------------------------------
# Sibling module imports
# ---------------------------------------------------------------------------
_SRC_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

from terrain.extract_elevation import sample_elevation  # noqa: E402
from landcover.extract_nlcd import (  # noqa: E402
    sample_nlcd_class,
    NLCD_STATIC_YEAR_CAVEAT,
)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_REPO = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
STATIONS_FILE = os.path.join(_REPO, "pipeline", "config", "exp001_stations.yaml")
HRRR_MANIFEST = os.path.join(
    _REPO, "data", "processed", "manifests", "hrrr_extraction_manifest.jsonl"
)
DEFAULT_OUTPUT = os.path.join(
    _REPO, "data", "processed", "station_metadata", "exp001_terrain_landcover.json"
)

SXT_RISK_NOTE = (
    "SXT (Sexton Summit) is a non-airport mountain-summit ASOS at ~1171m. "
    "Phase 2C completeness was 22.0% (475/2160 hourly slots). "
    "Elevation mismatch to the 2.5km HRRR grid is expected to be significant. "
    "SXT does not meet 90% completeness threshold; Stage 3 claim eligibility "
    "requires operator review before inclusion."
)


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------
def load_stations() -> dict:
    if not os.path.exists(STATIONS_FILE):
        print(f"ERROR: Stations config not found: {STATIONS_FILE}", file=sys.stderr)
        sys.exit(1)
    with open(STATIONS_FILE, "r") as f:
        cfg = yaml.safe_load(f)
    return {s["station_id"]: s for s in cfg["stations"]}


def load_hrrr_grids() -> dict:
    if not os.path.exists(HRRR_MANIFEST):
        print(f"ERROR: HRRR manifest not found: {HRRR_MANIFEST}", file=sys.stderr)
        sys.exit(1)
    grids = {}
    with open(HRRR_MANIFEST, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                row = json.loads(line)
                sid = row["station_id"]
                if sid not in grids:
                    grids[sid] = {
                        "grid_lat": row["grid_lat"],
                        "grid_lon": row["grid_lon"],
                    }
            except Exception:
                continue
    return grids


# ---------------------------------------------------------------------------
# Dry-run output
# ---------------------------------------------------------------------------
def run_dry_run(stations: dict, hrrr_grids: dict) -> None:
    print("\n[DRY RUN] Input files:")
    print(f"  Stations config  : {STATIONS_FILE}  [OK]")
    print(f"  HRRR manifest    : {HRRR_MANIFEST}  [OK]")
    print(f"  Expected output  : {DEFAULT_OUTPUT}")
    print()

    print("[DRY RUN] Station -> HRRR Grid coordinate pairs:")
    for sid, scfg in stations.items():
        grid = hrrr_grids.get(sid, {})
        elev = scfg.get("elevation_m", "N/A")
        s_lat = scfg["latitude"]
        s_lon = scfg["longitude"]
        g_lat = grid.get("grid_lat", "MISSING")
        g_lon = grid.get("grid_lon", "MISSING")
        offset = ""
        if isinstance(g_lat, float) and isinstance(g_lon, float):
            dlat = abs(s_lat - g_lat)
            dlon = abs(s_lon - g_lon)
            offset = f"  dlat={dlat:.4f}deg dlon={dlon:.4f}deg"
        risk = "  ** PROXY RISK FLAG ACTIVE **" if sid == "SXT" else ""
        print(
            f"  {sid:<5}  station=({s_lat}, {s_lon}, {elev}m)  "
            f"grid=({g_lat}, {g_lon}){offset}{risk}"
        )

    print("\n[DRY RUN] No output written.")


# ---------------------------------------------------------------------------
# Real extraction
# ---------------------------------------------------------------------------
def run_extraction(
    stations: dict,
    hrrr_grids: dict,
    elevation_raster: str,
    nlcd_raster: str,
    online: bool,
    output_path: str,
) -> None:

    if not online:
        missing = []
        if not elevation_raster or not os.path.exists(elevation_raster):
            missing.append(f"  Elevation raster not found: {elevation_raster}")
        if not nlcd_raster or not os.path.exists(nlcd_raster):
            missing.append(f"  NLCD raster not found: {nlcd_raster}")
        if missing:
            print("ERROR: Missing rasters in local mode:\n", file=sys.stderr)
            for m in missing:
                print(m, file=sys.stderr)
            sys.exit(2)

    results = []
    generated_at = datetime.now(timezone.utc).isoformat()
    nlcd_blocked = False

    for sid, scfg in stations.items():
        grid = hrrr_grids.get(sid, {})
        if not grid:
            continue

        s_lat = scfg["latitude"]
        s_lon = scfg["longitude"]
        g_lat = grid["grid_lat"]
        g_lon = grid["grid_lon"]

        print(f"  {sid}: sampling elevation at station ({s_lat}, {s_lon})...", end=" ", flush=True)
        s_elev = sample_elevation(s_lat, s_lon, raster_path=elevation_raster, online=online)
        print(f"-> {s_elev.get('elevation_m')} m", end="  ")

        print(f"grid ({g_lat}, {g_lon})...", end=" ", flush=True)
        g_elev = sample_elevation(g_lat, g_lon, raster_path=elevation_raster, online=online)
        print(f"-> {g_elev.get('elevation_m')} m")

        elev_mismatch = None
        elev_mismatch_gt50 = None
        if s_elev["elevation_m"] is not None and g_elev["elevation_m"] is not None:
            elev_mismatch = round(abs(s_elev["elevation_m"] - g_elev["elevation_m"]), 2)
            elev_mismatch_gt50 = elev_mismatch > 50.0

        print(f"  {sid}: sampling NLCD at station...", end=" ", flush=True)
        s_nlcd = sample_nlcd_class(s_lat, s_lon, raster_path=nlcd_raster, online=online)
        if s_nlcd.get("error") == "BLOCKED_FOR_NLCD_DOWNLOAD":
            nlcd_blocked = True
            print("-> BLOCKED", end="  ")
        else:
            print(f"-> {s_nlcd.get('class_code')}", end="  ")

        print("grid...", end=" ", flush=True)
        g_nlcd = sample_nlcd_class(g_lat, g_lon, raster_path=nlcd_raster, online=online)
        if g_nlcd.get("error") == "BLOCKED_FOR_NLCD_DOWNLOAD":
            print("-> BLOCKED")
        else:
            print(f"-> {g_nlcd.get('class_code')}")

        record = {
            "station_id": sid,
            "terrain_class": scfg.get("terrain_class", "unknown"),
            "station_lat": s_lat,
            "station_lon": s_lon,
            "station_elevation_m_config": scfg.get("elevation_m"),
            "hrrr_grid_lat": g_lat,
            "hrrr_grid_lon": g_lon,
            "station_elevation_m_dem": s_elev["elevation_m"],
            "station_elevation_dem_error": s_elev.get("error"),
            "hrrr_grid_elevation_m_dem": g_elev["elevation_m"],
            "hrrr_grid_elevation_dem_error": g_elev.get("error"),
            "elevation_mismatch_m": elev_mismatch,
            "elevation_mismatch_gt_50m": elev_mismatch_gt50,
            "station_nlcd_2021_code": s_nlcd.get("class_code"),
            "station_nlcd_2021_label": s_nlcd.get("class_label"),
            "station_nlcd_error": s_nlcd.get("error"),
            "hrrr_grid_nlcd_2021_code": g_nlcd.get("class_code"),
            "hrrr_grid_nlcd_2021_label": g_nlcd.get("class_label"),
            "hrrr_grid_nlcd_error": g_nlcd.get("error"),
            "proxy_risk_note": SXT_RISK_NOTE if sid == "SXT" else None,
            "elevation_source_path": "ONLINE_USGS_EPQS" if online else os.path.abspath(elevation_raster) if elevation_raster else None,
            "nlcd_source_path": "BLOCKED" if nlcd_blocked else os.path.abspath(nlcd_raster) if nlcd_raster else None,
            "raster_crs_elevation": s_elev.get("raster_crs"),
            "raster_crs_nlcd": s_nlcd.get("raster_crs"),
            "access_date": generated_at,
        }
        results.append(record)

    # NLCD fallback printing
    if nlcd_blocked:
        print("\n" + "!" * 60)
        print("WARNING: land_cover_status is BLOCKED_FOR_NLCD_DOWNLOAD")
        print("NLCD 2021 point queries are unavailable or unreliable.")
        print("To complete Phase 2E metadata, manually download the NLCD raster:")
        print("  1. Go to https://www.mrlc.gov/viewer/")
        print("  2. Draw box around Oregon (Lat 42-46.5, Lon -124.5 to -121)")
        print("  3. Download NLCD 2021 Land Cover GeoTIFF")
        print("  4. Re-run script using --nlcd-raster")
        print("!" * 60)

    output = {
        "metadata_version": "1.0",
        "experiment_id": "EXP001",
        "stage": "Phase_2E",
        "generated_at": generated_at,
        "land_cover_status": "BLOCKED_FOR_NLCD_DOWNLOAD" if nlcd_blocked else "COMPLETE",
        "caveats": [NLCD_STATIC_YEAR_CAVEAT],
        "stations": results,
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nPartial output written: {output_path}" if nlcd_blocked else f"\nOutput written: {output_path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--online", action="store_true", help="Use online point-query where possible")
    parser.add_argument("--elevation-raster", type=str, default=None)
    parser.add_argument("--nlcd-raster", type=str, default=None)
    parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    print("=" * 60)
    print("MRDE EXP001 Phase 2E: Terrain & Land Cover Metadata")
    print("=" * 60)

    stations = load_stations()
    hrrr_grids = load_hrrr_grids()

    if args.dry_run:
        run_dry_run(stations, hrrr_grids)
        return

    if not args.online and (not args.elevation_raster or not args.nlcd_raster):
        print(
            "ERROR: Real local extraction requires both --elevation-raster and --nlcd-raster.\n"
            "Use --online for point-query mode.",
            file=sys.stderr,
        )
        sys.exit(2)

    run_extraction(stations, hrrr_grids, args.elevation_raster, args.nlcd_raster, args.online, args.output)


if __name__ == "__main__":
    main()
