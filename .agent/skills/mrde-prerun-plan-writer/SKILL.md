---
name: mrde-prerun-plan-writer
description: Use specifically when creating, filling, or auditing `experiments/EXP001/PRE_RUN_PLAN.md` or a `pre_run_experiment_plan` append-only log entry before any residual data inspection.
---

# MRDE Pre-Run Plan Writer

## Purpose

Use this skill to draft or audit `experiments/EXP001/PRE_RUN_PLAN.md` and the corresponding `pre_run_experiment_plan` JSONL entry before any residual data inspection.

## Required context files

Read in this order:

1. `01_MASTER_COMPLETION_CONTRACT.md`
2. `04_SCOPE_LOCK_AND_V0_DEFINITION.md`
3. `05_DATA_ENGINEERING_AND_PROVENANCE.md`
4. `06_EVALUATION_CLAIMS_AND_ASSUMPTIONS.md`
5. `08_APPEND_ONLY_LOG_SCHEMA.md`
6. `schemas/pre_run_plan.schema.json`
7. `experiments/EXP001/PRE_RUN_PLAN.md`

## Required pre-run fields

The plan must explicitly define:

- `experiment_id`
- `research_question`
- `geographic_region`
- `station_list`
- `time_window`
- `forecast_source`
- `observation_source`
- `lead_times`
- `residual_definition`
- `time_alignment_rule`
- `spatial_alignment_rule`
- `qc_policy`
- `terrain_source`
- `land_cover_source`
- `train_validation_test_split`
- `metrics`
- `baselines`
- `supported_thresholds`
- `minimum_sample_floor`
- `maximum_hypothesis_families`
- `allowed_analyses`
- `sensitivity_checks`
- `human_approval`
- `max_ambiguous_iterations`
- `primary_metric_and_threshold`
- `proxy_risk_screening_criteria`
- `station_selection_filter_criteria`
- `residual_preinspection_attestation`
- `strongest_baseline_id`
- `allowed_metadata_groupings`
- `rigorous_stability_metric_definition` when station count is below 10

## Procedure

1. Confirm no residual data, residual plots, residual summaries, or target-window mismatch outputs have been inspected.
2. For a submitted or logged plan, confirm `residual_preinspection_attestation: true`. If the field is `false`, output BLOCKED. If the field is still a template placeholder, output TEMPLATE_ONLY / NEEDS_HUMAN_APPROVAL.
3. Confirm station selection uses blind metadata-only criteria via `station_selection_filter_criteria`.
4. Confirm `strongest_baseline_id` is defined and appears in `baselines`.
5. Confirm `train_validation_test_split` uses a temporal split, not a random split.
6. Confirm `primary_metric_and_threshold` is defined before data inspection.
7. Confirm allowed metadata groupings are explicit and finite.
8. Confirm station count is 3–5 for v0 and region is pre-specified.
9. Confirm correction claims and operational forecast claims are excluded.
10. Produce a filled plan or an audit report listing missing fields.
11. Prepare a matching append-only `pre_run_experiment_plan` entry if all required fields are present.

## Output format

Return:

- `verdict`: ALLOWED / BLOCKED / TEMPLATE_ONLY / NEEDS_HUMAN_APPROVAL
- `missing_required_fields`: list
- `residual_preinspection_attestation`: true/false/unknown
- `station_selection_filter_status`: valid/invalid/unknown
- `strongest_baseline_status`: valid/invalid/unknown
- `supported_threshold_status`: valid/invalid/unknown
- `safe_to_begin_stage_1`: yes/no
- `required_log_entry`: yes/no

## Hard stops

Stop if:

- residual data has already been inspected without a plan;
- `residual_preinspection_attestation` is false or unknown;
- station selection depends on residual behavior;
- thresholds are missing but the plan seeks SUPPORTED eligibility;
- the plan attempts correction claims in v0.
