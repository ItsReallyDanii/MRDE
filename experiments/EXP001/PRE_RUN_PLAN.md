# EXP001 — Pre-Run Experiment Plan

> Fill this before any residual inspection. After residual inspection, do not change locked fields for this experiment ID.

```yaml
log_schema_version: "1.1"
entry_type: pre_run_experiment_plan
experiment_id: EXP001
created_at: "2026-04-28T05:44:17Z"
operator: "Daniel Sleiman"
self_review_allowed: true
# Self-review is allowed for internal v0 progression only and must be logged.
# Public SUPPORTED_PATTERN language requires later independent or external review.

research_question: >
  Do 2-meter temperature forecast-observation residuals from HRRR show repeatable
  associations with predefined terrain/elevation/land-cover classes across five
  Oregon ASOS/METAR-network stations during a locked 90-day summer 2024 window
  (2024-06-01 through 2024-08-30, end-exclusive)?

geographic_region: >
  Oregon, USA. A multi-terrain transect covering four predefined terrain/context
  classes: Oregon coast (coastal low-elevation), Willamette Valley (inland valley),
  interior southern valley and mountain/pass (Cascades / southern mountains), and
  central Oregon high desert. Defined before any data inspection.

station_list:
  - station_id: "AST"
    station_name: "Astoria Regional Airport / Clatsop County"
    latitude: 46.1580
    longitude: -123.8787
    elevation_m: 8
    terrain_class: "coastal_low_elevation"
    selection_reason: >
      Active Oregon ASOS/METAR-network station with long public archive.
      Represents coastal low-elevation terrain class. Selected on metadata,
      geography, and terrain/land-cover representativeness only; no residual
      data, forecast errors, or mismatch behavior was inspected.

  - station_id: "SLE"
    station_name: "Salem / McNary Field"
    latitude: 44.9095
    longitude: -123.0029
    elevation_m: 61
    terrain_class: "willamette_valley"
    selection_reason: >
      Active Oregon ASOS/METAR-network station with long public archive.
      Represents Willamette Valley interior-valley terrain class. Selected
      on metadata, geography, and terrain/land-cover representativeness only;
      no residual data, forecast errors, or mismatch behavior was inspected.

  - station_id: "MFR"
    station_name: "Rogue Valley International / Medford / Jackson County"
    latitude: 42.3742
    longitude: -122.8735
    elevation_m: 405
    terrain_class: "interior_southern_valley"
    selection_reason: >
      Active Oregon ASOS/METAR-network station with long public archive.
      Represents interior southern-valley terrain class. Selected on metadata,
      geography, and terrain/land-cover representativeness only; no residual
      data, forecast errors, or mismatch behavior was inspected.

  - station_id: "SXT"
    station_name: "Sexton Summit ASOS"
    latitude: 42.6106
    longitude: -123.3692
    elevation_m: 1175
    terrain_class: "mountain_pass"
    selection_reason: >
      Active Oregon ASOS/METAR-network station with long public archive.
      Represents Cascades mountain/pass terrain class with high terrain
      complexity and significant HRRR grid-to-station elevation mismatch
      potential. Selected on metadata, geography, and elevation only; no
      residual data, forecast errors, or mismatch behavior was inspected.

  - station_id: "RDM"
    station_name: "Roberts Field / Redmond"
    latitude: 44.2541
    longitude: -121.1500
    elevation_m: 938
    terrain_class: "central_high_desert"
    selection_reason: >
      Active Oregon ASOS/METAR-network station with long public archive.
      Represents central Oregon high-desert terrain class. Selected on
      metadata, geography, and terrain/land-cover representativeness only;
      no residual data, forecast errors, or mismatch behavior was inspected.

station_selection_filter_criteria: >
  Select active Oregon ASOS/METAR-network stations satisfying all of the
  following metadata-only criteria: (1) publicly archived continuous hourly
  observations available for the full study window 2024-06-01 through
  2024-08-30 with no known archive gap or station decommissioning; (2) at
  least 90% usable hourly observations expected after standard QC; (3)
  geographic coverage spanning at least four predefined Oregon terrain/context
  classes (coastal, valley, interior valley, mountain/pass, high desert);
  (4) station metadata (ID, coordinates, elevation) publicly documented.
  Selection was based only on station metadata, geography, elevation, and
  terrain/land-cover representativeness. No residuals, forecast errors,
  model performance summaries, or prior mismatch behavior were inspected
  at any point during station selection.

time_window:
  start: "2024-06-01T00:00:00Z"
  end: "2024-08-30T00:00:00Z"
  interpretation: "end-exclusive 90-day window"

forecast_source: >
  NOAA/NCEP High-Resolution Rapid Refresh (HRRR) CONUS, 3-km grid.
  Preferred model cycle: most recent operationally available cycle for each
  valid time. Model version and cycle details must be documented at data
  access time. If a HRRR model-cycle or version change occurred during the
  window, pre/post periods must be stratified and flagged for human review
  before pooling.

forecast_variable: "2-meter temperature"

observation_source: >
  NOAA/NCEI ASOS/AWOS hourly surface observations via METAR format.
  Primary archive: IEM ASOS download or NCEI LCD/DSI-3505.
  Access date and archive version must be recorded at data download time.

observation_variable: "2-meter temperature"

lead_times:
  - "1h"
  - "3h"
  - "6h"
  - "12h"

residual_definition: "forecast_temperature_minus_observed_temperature"

terrain_source: >
  SRTM (Shuttle Radar Topography Mission) 1-arc-second, or NED 1/3 arc-second
  if SRTM unavailable. Source version and access date must be recorded.

land_cover_source: >
  NLCD (National Land Cover Database) 2021 or most recent available release.
  MODIS MCD12Q1 as fallback only if NLCD is unavailable for a station
  footprint; fallback use must be logged. Source version and access date
  must be recorded.

time_alignment_rule: >
  Use the nearest available observation within +-10 minutes of the HRRR
  forecast valid time. If multiple observations qualify within the tolerance
  window, use the one with the smallest absolute timestamp difference. If no
  observation qualifies, mark the row as missing. Do not impute missing
  observations for validation or test metrics. Sunrise/sunset transition
  periods must be flagged for review as small time offsets may produce
  artificial temperature residuals.

spatial_alignment_rule: >
  Primary: nearest HRRR 3-km grid point to the station's reported
  latitude/longitude. Sensitivity check: bilinear interpolation of the four
  surrounding grid points, if computationally practical. The bilinear result
  is a sensitivity check only; the nearest-grid-point result is the primary.
  For every station-grid pairing, document the absolute elevation difference
  between the HRRR grid point's reported terrain height and the station's
  reported elevation. Flag all station-grid pairs where absolute elevation
  mismatch exceeds 50 meters as a potential proxy-risk confound requiring
  proxy-risk review before SUPPORTED_PATTERN claim eligibility.

qc_policy: >
  Exclude observations meeting any of the following criteria: (1) METAR
  quality flag indicating bad or missing data; (2) missing or null temperature
  value; (3) temperature value physically impossible (outside -60 C to 60 C);
  (4) duplicate timestamp for the same station; (5) source-file parsing
  failure. Require at least 90% usable hourly observations per station over
  the full 90-day window for a station to be eligible as primary. A station
  falling below 90% completeness must be logged and flagged for human review;
  it may not contribute to SUPPORTED_PATTERN claims unless the deficiency is
  reviewed and approved. Do not impute missing temperature values for
  validation or test metrics. Flatlined values (same temperature for >= 6
  consecutive hours) must be flagged and reviewed before inclusion.

train_validation_test_split: >
  Temporal split only. Random splits are prohibited for time-correlated
  meteorological observations.
  Train / exploratory calibration: days 1-60
    (2024-06-01T00:00:00Z through 2024-07-30T23:59:59Z).
  Validation: days 61-75
    (2024-07-31T00:00:00Z through 2024-08-14T23:59:59Z).
  Locked test: days 76-90
    (2024-08-15T00:00:00Z through 2024-08-29T23:59:59Z,
    end-exclusive at window close).
  Baselines and bias estimates may only be trained on the train window.
  No test-set results may be reviewed until validation is complete.

metrics:
  - signed_residual_bias
  - absolute_residual_magnitude
  - MAE
  - RMSE
  - residual_magnitude_by_station
  - residual_magnitude_by_lead_time
  - residual_magnitude_by_predefined_terrain_elevation_land_cover_group

baselines:
  - id: raw_hrrr_forecast
    description: >
      Raw HRRR 2-meter temperature forecast with no correction.
      Primary public forecast baseline.
  - id: persistence_baseline
    description: >
      Persistence forecast: previous valid observation carried forward
      as the prediction.
  - id: station_wise_mean_bias_baseline
    description: >
      Station-specific mean signed residual computed on train window
      only, applied as a bias offset for validation/test.
  - id: lead_time_time_of_day_station_bias_baseline
    description: >
      Mean signed residual stratified by station x lead time x
      time-of-day bin, computed on train window only.
      Designated strongest baseline.

strongest_baseline_id: "lead_time_time_of_day_station_bias_baseline"

primary_metric_and_threshold:
  metric: "between_group_absolute_residual_magnitude_separation_on_locked_test_set_versus_strongest_baseline"
  threshold: >
    All three conditions must be met simultaneously on the locked test set:
    (1) at least 10% absolute residual magnitude separation between the
        highest-residual and lowest-residual predefined terrain/context groups;
    (2) Cohen's d >= 0.2 between compared groups;
    (3) BH-adjusted p <= 0.05 where hypothesis testing applies.
    Meeting only one or two conditions is insufficient for SUPPORTED_PATTERN.

supported_thresholds: >
  A candidate pattern may only be labeled SUPPORTED_PATTERN if ALL of the
  following are satisfied:
  1. The pattern was explicitly pre-registered in this plan's allowed_analyses
     and allowed_metadata_groupings.
  2. The primary metric threshold is met on the locked test set (>=10%
     residual-magnitude separation AND Cohen's d >= 0.2 AND BH-adjusted
     p <= 0.05 where applicable).
  3. BH-adjusted p <= 0.05 where hypothesis testing is used.
  4. Cohen's d >= 0.2 or another pre-logged nontrivial effect-size floor is met.
  5. Effect direction does not reverse under any required sensitivity check.
  6. The strongest baseline (lead_time_time_of_day_station_bias_baseline)
     comparison is passed; success against weaker baselines alone is insufficient.
  7. Proxy-risk review does not invalidate the finding (no unresolved airport
     microenvironment, elevation mismatch, QC, or model-cycle confound remains).
  8. Minimum sample floor is met (see minimum_sample_floor).
  9. Human approval is logged.
  Correction claims and operational forecast-improvement claims are out of
  scope for EXP001 / MRDE v0.

minimum_sample_floor: >
  At least 1,000 matched forecast-observation rows total across all stations
  on the locked test set. At least 150 rows per tested terrain/context group
  for SUPPORTED_PATTERN eligibility. Any group below 150 rows may be reported
  descriptively but may not be labeled SUPPORTED_PATTERN.

maximum_hypothesis_families: 2

allowed_analyses: >
  Only the following analyses are pre-approved for SUPPORTED_PATTERN
  eligibility claims:
  (1) Terrain/elevation-conditioned residual magnitude comparison: compare
      mean absolute residual or MAE across predefined terrain/elevation
      classes (coastal_low_elevation, willamette_valley,
      interior_southern_valley, mountain_pass, central_high_desert) on
      the locked test set.
  (2) Land-cover-conditioned residual magnitude comparison: compare mean
      absolute residual or MAE across predefined NLCD land-cover classes
      collocated with each station on the locked test set.
  Descriptive summaries, bias tables, lead-time residual profiles, and
  time-of-day stratification are permitted as exploratory outputs on the
  train window only and must be labeled SPECULATIVE if reported. Post-hoc
  patterns identified during exploratory analysis may not be evaluated for
  SUPPORTED_PATTERN status on the same data used to find them.

allowed_metadata_groupings:
  - elevation_class
  - terrain_class
  - nlcd_land_cover_class
  - lead_time
  - time_of_day_bin

sensitivity_checks: >
  All required v0 sensitivity checks must be run before any SUPPORTED_PATTERN
  claim:
  (1) Time-alignment tolerance variant: repeat primary analysis using
      +-5-minute tolerance and compare direction/magnitude.
  (2) Spatial alignment variant: if bilinear interpolation is practical,
      repeat primary analysis and compare direction/magnitude versus
      nearest-grid-point result. Infeasibility must be logged before
      validation.
  (3) Leave-one-station-out stability: repeat primary analysis five times,
      each time excluding one station. Stability criterion defined in
      rigorous_stability_metric_definition.
  (4) Baseline-comparison stability: confirm pattern holds against all four
      declared baselines, not only the weakest.
  (5) Time-of-day stratification: repeat primary analysis split by daytime
      (local solar time 06:00-18:00) vs. nighttime bins.
  (6) Month/season stratification: repeat primary analysis split by June,
      July, August separately. Infeasibility must be logged before
      validation if data volume does not support this split.

rigorous_stability_metric_definition: >
  Because station count is 5 (below 10), a stricter stability criterion
  applies for leave-one-station-out checks. A candidate is considered stable
  only if: (a) the sign/direction of the primary group effect remains the
  same in at least 4 of 5 leave-one-station-out checks, AND (b) the effect
  magnitude does not collapse below 50% of the full-sample effect in more
  than one leave-one-station-out check. Failure to meet either condition
  downgrades the candidate to AMBIGUOUS.

proxy_risk_screening_criteria: >
  Before SUPPORTED_PATTERN eligibility, the following proxy-risk factors
  must be flagged, documented, and reviewed:
  (1) Airport microenvironment effects: all five stations are ASOS collocated
      with airports; paved surface fraction, tarmac proximity, wind exposure,
      and thermal-mass effects must be documented as potential confounds when
      terrain/land-cover class is the feature of interest.
  (2) Station-grid elevation mismatch >50 m: if absolute elevation difference
      between HRRR grid point and station exceeds 50 m, assess whether
      elevation mismatch correlates with residual pattern before
      SUPPORTED_PATTERN label. SXT (mountain/pass, 1175 m) is flagged as
      high-risk for this confound.
  (3) Coastal exposure vs. inland contrast: AST coastal station may have
      sea-breeze or marine-layer dynamics not attributable to terrain per se;
      must be documented and assessed.
  (4) Mountain/pass representativeness: SXT at a highway pass may not
      represent broad Cascades terrain; must be noted.
  (5) Land-cover mismatch between station measurement footprint and HRRR
      grid cell footprint: document for each station.
  (6) Missing-data concentration: assess whether missing data concentrates
      in specific stations, times of day, or weather regimes that could
      bias results.
  (7) Model-cycle and source-availability issues: if HRRR archive gaps or
      version changes exist in the window, stratify and flag before pooling.
  (8) QC inconsistencies: assess whether QC exclusions cluster by station
      or time period in a way that could bias group comparisons.

max_ambiguous_iterations: 2

human_approval: true
approved_at: "2026-04-28T05:44:17Z"

notes: >
  EXP001 is the first MRDE v0 pilot experiment. Five-station Oregon
  multi-terrain transect selected entirely by metadata-only criteria. No
  residual data, forecast-observation mismatch tables, model-error
  summaries, or station-specific residual behavior was inspected at any
  point during plan drafting. Correction claims and operational
  forecast-improvement claims are out of scope for v0. Self-review is
  allowed for internal v0 progression but must be logged; public
  SUPPORTED_PATTERN language requires later independent or external review.
  Draft produced by Antigravity (advisory only) from operator-provided
  choices. Human approval confirmed by explicit operator message at
  2026-04-28T05:44:17Z.

# Value is bare boolean true. Do not quote.
residual_preinspection_attestation: true
```

## Lock Statement

I attest that this plan was created before residual inspection and that station selection was not based on observed residual behavior.

Before this plan is submitted or logged as a `pre_run_experiment_plan`, `residual_preinspection_attestation` must be set to `true`. If any residual data, residual plots, residual summaries, or target-window mismatch outputs have already been inspected, this EXP001 plan is invalid and must not be used for SUPPORTED_PATTERN eligibility.

The `train_validation_test_split` must use a temporal split, such as a held-out trailing time window or another pre-declared time-block split. Random splits across time-correlated meteorological observations are prohibited for validation metrics or SUPPORTED_PATTERN eligibility.

- Operator: Daniel Sleiman
- Date: 2026-04-28T05:44:17Z
- Human approval: true — confirmed by explicit operator message "approved — write the files" at 2026-04-28T05:44:17Z
