"""
MRDE EXP001 — Provenance manifest writer
Stage 2 Phase 2C: records source URL, access date, sha256 for raw files.
FORBIDDEN: no residuals, no forecast-observation comparisons.
"""
import hashlib
import json
import os
from datetime import datetime, timezone


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


def record_raw_source(
    manifest_path: str,
    source_url: str,
    access_date: str,
    local_path: str,
    station_id: str = None,
    extra: dict = None,
) -> str:
    sha256 = sha256_file(local_path)
    entry = {
        "log_schema_version": "1.1",
        "entry_type": "raw_source",
        "experiment_id": "EXP001",
        "source_url": source_url,
        "access_date": access_date,
        "local_path": os.path.abspath(local_path),
        "sha256": sha256,
    }
    if station_id:
        entry["station_id"] = station_id
    if extra:
        entry.update(extra)
    append_jsonl(manifest_path, entry)
    return sha256
