"""
MRDE EXP001 — ASOS QC Precheck  (v2 — hourly-slot completeness)
Stage 2 Phase 2C

Completeness is measured by COVERED HOURLY SLOTS, not raw row count.
A slot is covered if at least one valid temperature observation maps to it
via nearest-hour rounding (ties round up: e.g. :30 → next hour).

Expected slots: 2160  (90 days × 24 hours,
    2024-06-01T00:00:00Z through 2024-08-29T23:00:00Z inclusive)

FORBIDDEN: no residuals, no forecasts, no mismatch columns, no imputation.
"""
import csv
import json
import os
from datetime import datetime, timedelta, timezone

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_REPO = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
RAW_DIR = os.path.join(_REPO, "data", "raw", "asos")
REPORT_DIR = os.path.join(_REPO, "data", "processed", "qc_reports")
MANIFEST_DIR = os.path.join(_REPO, "data", "processed", "manifests")

# ---------------------------------------------------------------------------
# EXP001 locked parameters
# ---------------------------------------------------------------------------
STATIONS = ["AST", "SLE", "MFR", "SXT", "RDM"]
WINDOW_START = datetime(2024, 6, 1, 0, 0, 0, tzinfo=timezone.utc)
WINDOW_END_EXCL = datetime(2024, 8, 30, 0, 0, 0, tzinfo=timezone.utc)

# Hourly slots: 2024-06-01 00:00 UTC ... 2024-08-29 23:00 UTC  (inclusive)
EXPECTED_HOURLY_ROWS = 90 * 24  # 2160

TEMP_MIN_C = -60.0
TEMP_MAX_C = 60.0
FLATLINE_MIN_HOURS = 6


# ---------------------------------------------------------------------------
# Helper: generate full set of expected hourly slots
# ---------------------------------------------------------------------------
def _build_slot_set() -> set:
    slots = set()
    t = WINDOW_START
    while t < WINDOW_END_EXCL:
        slots.add(t)
        t += timedelta(hours=1)
    return slots


EXPECTED_SLOTS: set = _build_slot_set()
assert len(EXPECTED_SLOTS) == EXPECTED_HOURLY_ROWS, (
    f"Slot count mismatch: {len(EXPECTED_SLOTS)} != {EXPECTED_HOURLY_ROWS}"
)


def nearest_hour(dt: datetime) -> datetime:
    """Round a datetime to the nearest hour (half-up ties → next hour)."""
    discard = timedelta(
        minutes=dt.minute, seconds=dt.second, microseconds=dt.microsecond
    )
    dt_floor = dt - discard
    if discard >= timedelta(minutes=30):
        dt_floor += timedelta(hours=1)
    return dt_floor


def f_to_c(f: float) -> float:
    return (f - 32.0) * 5.0 / 9.0


def parse_dt(ts: str):
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(ts.strip(), fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def append_jsonl(path: str, entry: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Per-station QC
# ---------------------------------------------------------------------------
def check_station(station_id: str) -> dict:
    filepath = os.path.join(RAW_DIR, f"{station_id}_20240601_20240830.csv")
    if not os.path.exists(filepath):
        return {
            "station_id": station_id,
            "error": f"Raw file not found: {filepath}",
            "overall_phase_2c_verdict": "NO_GO",
        }

    raw_row_count = 0        # all non-header, non-comment rows
    malformed_count = 0
    missing_temp_count = 0
    impossible_count = 0
    duplicate_count = 0

    seen_ts: dict = {}       # raw timestamp dedup
    valid_obs: list = []     # dicts: {dt, tmp_c}  — passed all checks, in-window

    # ── Parse raw CSV ───────────────────────────────────────────────────────
    with open(filepath, "r", encoding="utf-8") as fh:
        header = None
        for raw_line in fh:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(",")]

            # Detect header row by presence of "valid" column name
            if header is None:
                if "valid" in line.lower():
                    header = parts
                continue

            raw_row_count += 1

            if len(parts) < len(header):
                malformed_count += 1
                continue

            row = dict(zip(header, parts))

            # ── Timestamp ───────────────────────────────────────────────────
            dt = parse_dt(row.get("valid", ""))
            if dt is None:
                malformed_count += 1
                continue

            # Window filter (end-exclusive)
            if dt < WINDOW_START or dt >= WINDOW_END_EXCL:
                continue

            # Duplicate raw-timestamp check
            ts_key = dt.isoformat()
            if ts_key in seen_ts:
                duplicate_count += 1
                continue
            seen_ts[ts_key] = True

            # ── Temperature ─────────────────────────────────────────────────
            tmpf_raw = row.get("tmpf", "M")
            if tmpf_raw in ("M", "", "Tr", None):
                missing_temp_count += 1
                continue

            try:
                tmp_c = f_to_c(float(tmpf_raw))
            except ValueError:
                malformed_count += 1
                continue

            if tmp_c < TEMP_MIN_C or tmp_c > TEMP_MAX_C:
                impossible_count += 1
                continue

            valid_obs.append({"dt": dt, "tmp_c": round(tmp_c, 2)})

    # ── Sort valid observations by time ─────────────────────────────────────
    valid_obs.sort(key=lambda r: r["dt"])

    # ── Hourly-slot coverage ─────────────────────────────────────────────────
    # Map each valid observation to its nearest hourly slot, then count
    # unique covered slots that are within the expected set.
    covered_slots: set = set()
    for obs in valid_obs:
        slot = nearest_hour(obs["dt"])
        if slot in EXPECTED_SLOTS:
            covered_slots.add(slot)

    usable_hourly_slots = len(covered_slots)
    completeness = usable_hourly_slots / EXPECTED_HOURLY_ROWS  # always <= 1.0
    passes_90 = completeness >= 0.90

    # ── Flatline detection (on sorted valid_obs, not slots) ──────────────────
    flatline_flags = []
    if valid_obs:
        run_start = 0
        run_temp = valid_obs[0]["tmp_c"]
        for i in range(1, len(valid_obs)):
            if valid_obs[i]["tmp_c"] != run_temp:
                run_len = i - run_start
                if run_len >= FLATLINE_MIN_HOURS:
                    flatline_flags.append({
                        "start": valid_obs[run_start]["dt"].isoformat(),
                        "end": valid_obs[i - 1]["dt"].isoformat(),
                        "duration_hours": run_len,
                        "tmp_c": run_temp,
                    })
                run_start = i
                run_temp = valid_obs[i]["tmp_c"]
        # Last run
        run_len = len(valid_obs) - run_start
        if run_len >= FLATLINE_MIN_HOURS:
            flatline_flags.append({
                "start": valid_obs[run_start]["dt"].isoformat(),
                "end": valid_obs[-1]["dt"].isoformat(),
                "duration_hours": run_len,
                "tmp_c": run_temp,
            })

    # ── Verdict ─────────────────────────────────────────────────────────────
    if passes_90:
        verdict = "GO"
        notes = (
            f"Passes 90% completeness threshold "
            f"({usable_hourly_slots}/{EXPECTED_HOURLY_ROWS} slots = {completeness:.1%})."
        )
    else:
        verdict = "GO_WITH_CAUTION"
        notes = (
            f"Below 90% threshold "
            f"({usable_hourly_slots}/{EXPECTED_HOURLY_ROWS} slots = {completeness:.1%}). "
            "Human review required before Stage 3 eligibility."
        )
        if station_id == "SXT":
            notes += (
                " SXT mountain-pass non-airport ASOS: low observation volume expected. "
                "Proxy-risk flag remains active per exp001_stations.yaml. "
                "Operator must decide GO/NO-GO for SXT before Stage 3."
            )

    return {
        "station_id": station_id,
        "total_expected_hourly_slots": EXPECTED_HOURLY_ROWS,
        "raw_rows_in_window": sum(
            1 for o in valid_obs  # in-window rows that passed QC
        ) + missing_temp_count + impossible_count,  # approximate; see notes
        "raw_row_count_all": raw_row_count,
        "valid_obs_in_window": len(valid_obs),
        "usable_hourly_slots": usable_hourly_slots,
        "completeness_rate": round(completeness, 4),
        "pass_90pct_threshold": passes_90,
        "missing_temp_count": missing_temp_count,
        "malformed_count": malformed_count,
        "duplicate_timestamp_count": duplicate_count,
        "impossible_temperature_count": impossible_count,
        "flatline_flag_count": len(flatline_flags),
        "flatline_flags": flatline_flags,
        "notes": notes,
        "overall_phase_2c_verdict": verdict,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    print("=" * 60)
    print("MRDE EXP001 Phase 2C: ASOS QC Precheck  (v2 slot-based)")
    print("=" * 60)
    print(f"Expected hourly slots per station: {EXPECTED_HOURLY_ROWS}")

    os.makedirs(REPORT_DIR, exist_ok=True)
    os.makedirs(MANIFEST_DIR, exist_ok=True)

    results = []
    for station in STATIONS:
        print(f"  Checking {station}...", end=" ", flush=True)
        r = check_station(station)
        results.append(r)
        print(
            f"covered_slots={r.get('usable_hourly_slots', 'ERR')}  "
            f"completeness={r.get('completeness_rate', 0):.1%}  "
            f"pass={r.get('pass_90pct_threshold')}  "
            f"verdict={r.get('overall_phase_2c_verdict')}"
        )

    overall = (
        "GO"
        if all(r.get("pass_90pct_threshold", False) for r in results)
        else "GO_WITH_CAUTION"
    )

    report = {
        "log_schema_version": "1.1",
        "entry_type": "qc_precheck_report",
        "precheck_version": "2",
        "completeness_method": "hourly_slot_coverage",
        "experiment_id": "EXP001",
        "stage": "Phase_2C",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "window_start": "2024-06-01T00:00:00Z",
        "window_end_exclusive": "2024-08-30T00:00:00Z",
        "expected_hourly_slots_per_station": EXPECTED_HOURLY_ROWS,
        "slot_assignment_method": (
            "nearest_hour_rounding: obs at HH:00-HH:29 → HH:00; "
            "HH:30-HH:59 → (HH+1):00"
        ),
        "qc_rules": {
            "temp_range_c": [TEMP_MIN_C, TEMP_MAX_C],
            "flatline_threshold_hours": FLATLINE_MIN_HOURS,
            "completeness_threshold": 0.90,
            "imputation": "FORBIDDEN",
            "completeness_cap": "100% (slot-based; cannot exceed 1 slot per hour)",
        },
        "stations": results,
        "overall_phase_2c_verdict": overall,
    }

    report_path = os.path.join(REPORT_DIR, "exp001_obs_qc_precheck.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\nQC report: {report_path}")

    # Overwrite ASOS obs manifest with corrected values
    manifest_path = os.path.join(MANIFEST_DIR, "asos_obs_manifest.jsonl")
    # Truncate existing file before re-writing
    open(manifest_path, "w").close()
    generated_at = report["generated_at"]
    for r in results:
        entry = {
            "log_schema_version": "1.1",
            "entry_type": "asos_obs_summary",
            "precheck_version": "2",
            "experiment_id": "EXP001",
            "stage": "Phase_2C",
            "station_id": r["station_id"],
            "usable_hourly_slots": r.get("usable_hourly_slots", 0),
            "total_expected_hourly_slots": EXPECTED_HOURLY_ROWS,
            "completeness_rate": r.get("completeness_rate", 0),
            "pass_90pct_threshold": r.get("pass_90pct_threshold", False),
            "overall_phase_2c_verdict": r.get("overall_phase_2c_verdict"),
            "generated_at": generated_at,
        }
        append_jsonl(manifest_path, entry)
    print(f"ASOS manifest (corrected): {manifest_path}")
    print(f"\nOverall Phase 2C verdict: {overall}")


if __name__ == "__main__":
    main()
