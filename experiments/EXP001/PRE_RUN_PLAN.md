# EXP001 — Pre-Run Experiment Plan

> Fill this before any residual inspection. After residual inspection, do not change locked fields for this experiment ID.

```yaml
log_schema_version: "1.1"
entry_type: pre_run_experiment_plan
experiment_id: EXP001
created_at:
operator:
self_review_allowed:
research_question:
geographic_region:
station_list:
  - station_id:
    station_name:
    latitude:
    longitude:
    selection_reason:
time_window:
  start:
  end:
forecast_source:
observation_source:
lead_times:
residual_definition: forecast_temperature_minus_observed_temperature
forecast_variable: 2-meter temperature
observation_variable: 2-meter temperature
time_alignment_rule:
spatial_alignment_rule:
qc_policy:
terrain_source:
land_cover_source:
train_validation_test_split: # Must specify a temporal split, not a random split, for time-correlated meteorological observations.
metrics:
baselines:
supported_thresholds:
minimum_sample_floor:
maximum_hypothesis_families:
allowed_analyses:
sensitivity_checks:
human_approval:
notes:
max_ambiguous_iterations:
primary_metric_and_threshold:
  metric:
  threshold:
proxy_risk_screening_criteria:
station_selection_filter_criteria:
# Set to true only after confirming no residual data, plots, summaries, or target-window mismatch outputs have been inspected.
residual_preinspection_attestation: "FILL_THIS_AS_TRUE_ONLY_AFTER_CONFIRMING_NO_RESIDUALS_INSPECTED"
strongest_baseline_id:
allowed_metadata_groupings:
  -
rigorous_stability_metric_definition:
```

## Lock statement

I attest that this plan was created before residual inspection and that station selection was not based on observed residual behavior.

Before this plan is submitted or logged as a `pre_run_experiment_plan`, `residual_preinspection_attestation` must be set to `true`. If any residual data, residual plots, residual summaries, or target-window mismatch outputs have already been inspected, this EXP001 plan is invalid and must not be used for SUPPORTED_PATTERN eligibility.

The `train_validation_test_split` must use a temporal split, such as a held-out trailing time window or another pre-declared time-block split. Random splits across time-correlated meteorological observations are prohibited for validation metrics or SUPPORTED_PATTERN eligibility.

- Operator:
- Date:
- Human approval:
