# 05 — Data Engineering and Provenance

## Purpose

This file defines the engineering assumptions required before any valid MRDE run.

## Required data sources for v0

Forecasts:

- HRRR preferred
- GFS only as fallback or separate experiment

Observations:

- ASOS/METAR preferred
- GHCNh/ISD only if explicitly logged

Context:

- SRTM or NED for elevation/terrain
- NLCD preferred for land cover
- MODIS only if explicitly logged as fallback or extension

## Required provenance fields

Every run must record:

- forecast product name;
- forecast model version/cycle if available;
- forecast issue time;
- forecast lead time;
- observation source;
- observation timestamp;
- station ID;
- station coordinates;
- station metadata snapshot or source reference;
- QC policy used;
- terrain data source and version;
- land-cover source and version;
- spatial interpolation rule;
- temporal alignment rule;
- data access date;
- local cached file hashes where feasible;
- code commit hash or frozen code snapshot identifier.

## Time-alignment rule

The experiment plan must define temporal tolerance before residual computation.

Default v0 rule:

- Forecast valid time should align to observation within ±10 minutes when possible.
- If a different tolerance is used, it must be logged before data inspection.
- Sunrise/sunset periods should be flagged because small time offsets may create artificial temperature residuals.

## Spatial alignment rule

The experiment plan must define how gridded forecast values map to station observations.

Allowed v0 approaches:

- nearest HRRR grid point;
- bilinear interpolation;
- both, if one is pre-defined as primary and the other as sensitivity check.

The selected method must be frozen before validation.

For HRRR-to-station comparisons, the elevation of the selected HRRR grid point must be documented alongside the station's actual elevation. Elevation differences greater than 50 m should be flagged as a potential proxy-risk confound unless a stricter experiment-specific threshold is declared in the pre-run plan. If grid-point-versus-station elevation difference correlates with the residual pattern, it must be assessed as a candidate non-terrain explanation before any SUPPORTED_PATTERN claim.

## Observation QC rule

The experiment plan must define:

- missing-data handling;
- flagged observation handling;
- despiking rule;
- flatline detection rule;
- minimum completeness threshold;
- station exclusion rule.

Default v0 minimum:

- exclude missing or explicitly bad flagged observations;
- require at least 90% usable records after QC;
- flag flatlined values for review;
- do not impute target observations for validation metrics.

## Model-cycle and version-change rule

Residuals spanning major model version, cycle, or QC-regime changes must be stratified or treated as separate experiments.

No pattern may be labeled SUPPORTED if it vanishes when results are stratified by model version/cycle or known QC regime.

If a model-cycle change occurs during the run window:

1. record the change;
2. split pre/post periods as strata;
3. flag for human review;
4. do not pool across the change for SUPPORTED claims unless stratified results remain stable.

## Data inspection rule

Before any exploratory residual inspection, a pre-run experiment plan must exist in the append-only log.

No station swaps, region expansion, metric changes, or threshold changes may occur after residual inspection without closing the run and creating a new experiment ID.

---
