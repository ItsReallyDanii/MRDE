"""
MRDE EXP001 -- Phase 2E: Build Terrain and Land Cover Metadata
Stage 2 Phase 2E

Driver script that assembles station_metadata/exp001_terrain_landcover.json
by combining:
  - Station coordinates from pipeline/config/exp001_stations.yaml
  - HRRR grid coordinates from data/processed/manifests/hrrr_extraction_manifest.jsonl
  - Elevation from a local DEM GeoTIFF (via --elevation-raster)
  - NLCD 2021 class from a local NLCD GeoTIFF (via --nlcd-raster)

Modes:
  --dry-run               Validate inputs, print plan, print schema. No output written.
  --elevation-raster PATH Elevation raster (required for real run).
  --nlcd-raster PATH      NLCD 2021 raster (required for real run).
  --output PATH           Override default output path.

FORBIDDEN: no raster downloads, no residuals, no ASOS-HRRR alignment.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

import yaml

# ---------------------------------------------------------------------------
# Sibling module imports (no package install required)
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

# SXT-specific proxy risk flag (ASCII-only)
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
    """Return {station_id: {grid_lat, grid_lon}} from first occurrence in manifest."""
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

    print()
    print("[DRY RUN] Planned output schema:")
    schema = {
        "metadata_version": "1.0",
        "experiment_id": "EXP001",
        "generated_at": "<ISO8601_TIMESTAMP>",
        "caveats": [NLCD_STATIC_YEAR_CAVEAT],
        "stations": [
            {
                "station_id": "<e.g. AST>",
                "terrain_class": "<from exp001_stations.yaml>",
                "station_lat": 0.0,
                "station_lon": 0.0,
                "station_elevation_m_config": "<from yaml>",
                "hrrr_grid_lat": 0.0,
                "hrrr_grid_lon": 0.0,
                "station_elevation_m_dem": "<sampled from DEM>",
                "hrrr_grid_elevation_m_dem": "<sampled from DEM>",
                "elevation_mismatch_m": "<|station_elev - grid_elev|>",
                "elevation_mismatch_gt_50m": "<bool>",
                "station_nlcd_2021_code": "<int>",
                "station_nlcd_2021_label": "<str>",
                "hrrr_grid_nlcd_2021_code": "<int>",
                "hrrr_grid_nlcd_2021_label": "<str>",
                "proxy_risk_note": "<SXT only, else null>",
                "elevation_source_path": "<raster path>",
                "nlcd_source_path": "<raster path>",
                "access_date": "<ISO8601>",
            }
        ],
    }
    print(json.dumps(schema, indent=2))
    print()
    print("[DRY RUN] No output written. To run real extraction:")
    print(
        "  python pipeline/src/metadata/build_terrain_landcover.py \\\n"
        "    --elevation-raster /path/to/dem.tif \\\n"
        "    --nlcd-raster /path/to/nlcd2021.tif"
    )


# ---------------------------------------------------------------------------
# Real extraction
# ---------------------------------------------------------------------------
def run_extraction(
    stations: dict,
    hrrr_grids: dict,
    elevation_raster: str,
    nlcd_raster: str,
    output_path: str,
) -> None:
    # Validate raster paths up front -- fail cleanly with instructions
    missing = []
    if not os.path.exists(elevation_raster):
        missing.append(
            f"  Elevation raster not found: {elevation_raster}\n"
            "  -> Download SRTM 1-arc-sec or USGS 3DEP from:\n"
            "      https://earthexplorer.usgs.gov/\n"
            "      https://apps.nationalmap.gov/downloader/"
        )
    if not os.path.exists(nlcd_raster):
        missing.append(
            f"  NLCD raster not found: {nlcd_raster}\n"
            "  -> Download NLCD 2021 Land Cover from:\n"
            "      https://www.mrlc.gov/data"
        )
    if missing:
        print("ERROR: Required raster files are missing:\n", file=sys.stderr)
        for m in missing:
            print(m, file=sys.stderr)
        sys.exit(2)

    results = []
    generated_at = datetime.now(timezone.utc).isoformat()

    for sid, scfg in stations.items():
        grid = hrrr_grids.get(sid, {})
        if not grid:
            print(f"  WARNING: {sid} has no HRRR grid entry in manifest -- skipping.")
            continue

        s_lat = scfg["latitude"]
        s_lon = scfg["longitude"]
        g_lat = grid["grid_lat"]
        g_lon = grid["grid_lon"]

        print(f"  {sid}: sampling elevation at station ({s_lat}, {s_lon})...", end=" ", flush=True)
        s_elev = sample_elevation(s_lat, s_lon, elevation_raster)
        print(f"-> {s_elev.get('elevation_m')} m", end="  ")

        print(f"grid ({g_lat}, {g_lon})...", end=" ", flush=True)
        g_elev = sample_elevation(g_lat, g_lon, elevation_raster)
        print(f"-> {g_elev.get('elevation_m')} m")

        # Elevation mismatch
        elev_mismatch = None
        elev_mismatch_gt50 = None
        if s_elev["elevation_m"] is not None and g_elev["elevation_m"] is not None:
            elev_mismatch = round(abs(s_elev["elevation_m"] - g_elev["elevation_m"]), 2)
            elev_mismatch_gt50 = elev_mismatch > 50.0

        print(f"  {sid}: sampling NLCD at station...", end=" ", flush=True)
        s_nlcd = sample_nlcd_class(s_lat, s_lon, nlcd_raster)
        print(f"-> {s_nlcd.get('class_code')} ({s_nlcd.get('class_label')})", end="  ")

        print("grid...", end=" ", flush=True)
        g_nlcd = sample_nlcd_class(g_lat, g_lon, nlcd_raster)
        print(f"-> {g_nlcd.get('class_code')} ({g_nlcd.get('class_label')})")

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
            "elevation_source_path": os.path.abspath(elevation_raster),
            "nlcd_source_path": os.path.abspath(nlcd_raster),
            "raster_crs_elevation": s_elev.get("raster_crs"),
            "raster_crs_nlcd": s_nlcd.get("raster_crs"),
            "access_date": generated_at,
        }
        results.append(record)

    output = {
        "metadata_version": "1.0",
        "experiment_id": "EXP001",
        "stage": "Phase_2E",
        "generated_at": generated_at,
        "caveats": [NLCD_STATIC_YEAR_CAVEAT],
        "stations": results,
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nOutput written: {output_path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="MRDE EXP001 Phase 2E: Terrain and Land Cover Metadata"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs and print planned work. No rasters required.",
    )
    parser.add_argument(
        "--elevation-raster",
        type=str,
        default=None,
        help="Path to a local DEM GeoTIFF (SRTM or USGS 3DEP). Required for real run.",
    )
    parser.add_argument(
        "--nlcd-raster",
        type=str,
        default=None,
        help="Path to the local NLCD 2021 GeoTIFF. Required for real run.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=DEFAULT_OUTPUT,
        help=f"Output JSON path (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("MRDE EXP001 Phase 2E: Terrain & Land Cover Metadata")
    print("=" * 60)

    stations = load_stations()
    hrrr_grids = load_hrrr_grids()

    print(f"Loaded {len(stations)} stations, {len(hrrr_grids)} HRRR grid entries.")

    if args.dry_run:
        run_dry_run(stations, hrrr_grids)
        return

    # Real run: both raster paths are required
    if not args.elevation_raster or not args.nlcd_raster:
        print(
            "ERROR: Real extraction requires both --elevation-raster and --nlcd-raster.\n"
            "Use --dry-run to validate without rasters.",
            file=sys.stderr,
        )
        sys.exit(2)

    run_extraction(stations, hrrr_grids, args.elevation_raster, args.nlcd_raster, args.output)


if __name__ == "__main__":
    main()
