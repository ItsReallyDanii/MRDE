"""
MRDE EXP001 — ASOS/IEM observation ingestion
Stage 2 Phase 2C

Downloads hourly METAR temperature observations for EXP001 stations.
Window: 2024-06-01T00:00:00Z through 2024-08-30T00:00:00Z (end-exclusive).
Stations: AST, SLE, MFR, SXT, RDM.

FORBIDDEN: no residuals, no forecast data, no mismatch columns.
"""
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone

import requests

# ---------------------------------------------------------------------------
# Paths — all relative to repo root (3 levels above this file)
# ---------------------------------------------------------------------------
_REPO = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
RAW_DIR = os.path.join(_REPO, "data", "raw", "asos")
MANIFEST_DIR = os.path.join(_REPO, "data", "processed", "manifests")
RAW_MANIFEST = os.path.join(MANIFEST_DIR, "raw_source_manifest.jsonl")

# ---------------------------------------------------------------------------
# EXP001 locked parameters
# ---------------------------------------------------------------------------
STATIONS = ["AST", "SLE", "MFR", "SXT", "RDM"]

IEM_BASE = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"
IEM_PARAMS = (
    "?station={station}&data=tmpf&tz=UTC"
    "&year1=2024&month1=6&day1=1"
    "&year2=2024&month2=8&day2=30"
    "&latlon=no&elev=no&missing=M&trace=T&direct=no&report_type=2"
)


# ---------------------------------------------------------------------------
# Provenance helpers (self-contained — no inter-script import required)
# ---------------------------------------------------------------------------
def sha256_file(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def append_jsonl(path: str, entry: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------
def download_station(station_id: str) -> str:
    url = IEM_BASE + IEM_PARAMS.format(station=station_id)
    access_date = datetime.now(timezone.utc).isoformat()
    print(f"  [{station_id}] GET {url[:80]}...")

    resp = requests.get(url, timeout=120)
    resp.raise_for_status()

    os.makedirs(RAW_DIR, exist_ok=True)
    local_path = os.path.join(RAW_DIR, f"{station_id}_20240601_20240830.csv")
    with open(local_path, "w", encoding="utf-8", newline="") as f:
        f.write(resp.text)

    sha256 = sha256_file(local_path)
    entry = {
        "log_schema_version": "1.1",
        "entry_type": "raw_source",
        "experiment_id": "EXP001",
        "stage": "Phase_2C",
        "station_id": station_id,
        "source_url": url,
        "access_date": access_date,
        "local_path": os.path.abspath(local_path),
        "file_bytes": os.path.getsize(local_path),
        "sha256": sha256,
    }
    append_jsonl(RAW_MANIFEST, entry)
    print(f"  [{station_id}] {os.path.getsize(local_path):,} bytes  sha256={sha256[:16]}...")
    return local_path


def main() -> None:
    print("=" * 60)
    print("MRDE EXP001 Phase 2C: ASOS Observation Download")
    print("=" * 60)
    errors = []
    for station in STATIONS:
        try:
            download_station(station)
            time.sleep(1)  # polite delay between IEM requests
        except Exception as exc:
            print(f"  ERROR [{station}]: {exc}")
            errors.append((station, str(exc)))
    if errors:
        print(f"\nERRORS: {errors}")
        sys.exit(1)
    print("\nAll downloads complete.")


if __name__ == "__main__":
    main()
