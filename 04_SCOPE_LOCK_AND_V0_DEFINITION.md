# 04 — Scope Lock and v0 Definition

## Active scope

**MRDE v0 / Terrain-Residual Sampler**

MRDE v0 tests whether public 2-meter temperature forecast-observation mismatches show repeatable associations with terrain/land-cover metadata.

## v0 research question

Do public 2-meter temperature forecast-observation mismatches exhibit repeatable terrain- or land-cover-associated patterns that generalize across held-out time periods, stations, or regions?

## v0 provisional parameters

| Field | v0 default |
|---|---|
| Variable | 2-meter temperature |
| Forecast source | HRRR preferred |
| Observation source | ASOS/METAR preferred |
| Station count | 3–5 stations |
| Duration | 90 days |
| Forecast lead times | Must be pre-specified in experiment plan |
| Geographic region | Must be pre-specified before data inspection |
| Terrain source | SRTM or NED |
| Land cover source | NLCD preferred, MODIS fallback |
| Agent role | Advisory only |

## Geographic sampling-frame rule

The v0 experiment plan must define a single geographic region before data inspection. Acceptable forms include one state, a small bounding box, or a named terrain corridor.

After initial logging, v0 must not expand, remove, swap, or add stations outside the pre-specified region unless the run is closed and a new experiment ID is created.

## Station-selection criteria

The v0 station list must be selected before residual analysis and must include:

- 3–5 stations;
- at least 90% usable observations after QC for the selected period;
- documented station IDs and coordinates;
- documented station-selection rationale;
- at least two terrain/context classes where feasible, or a logged reason if the pilot uses a lower-diversity region;
- no station selected because of a known residual pattern.

Station selection must be executed via a blind metadata-only filter (e.g., elevation range, station density, or geographic corridor) defined in the pre-run experiment plan. Selection based on computed, visualized, or previously logged residual behavior from the target experiment window is strictly prohibited.

## Deferred from v0

Do not include in v0:

- satellite imagery;
- GOES cloud masks;
- radar/MRMS precipitation;
- flood reports;
- public cameras;
- real-time streaming;
- precipitation residuals;
- wind direction;
- multi-variable modeling;
- autonomous agent search;
- operational or safety-facing outputs.

## Expansion rule

Any expansion beyond v0 scope requires:

1. human-gated approval;
2. new experiment ID;
3. updated pre-run experiment plan;
4. explicit statement that prior v0 claims do not automatically transfer.

---
