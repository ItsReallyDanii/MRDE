# 08 — Append-Only Log Schema

## Purpose

The append-only log preserves the experiment trail, including failures, human approvals, claim-tier changes, and governance decisions.

Logs should be JSONL-compatible and versioned.

## Required field: schema version

Every log entry must include:

```yaml
log_schema_version: "1.1"
```

## Entry types

Allowed entry types:

- `pre_run_experiment_plan`
- `data_ingestion`
- `residual_computation`
- `candidate_hypothesis`
- `validation_result`
- `sensitivity_check`
- `claim_tier_assignment`
- `human_review`
- `stop_rule_triggered`
- `failed_result_retest_request`
- `scope_amendment`
- `changelog_entry`

## Pre-run experiment plan schema

```yaml
log_schema_version: "1.1"
entry_type: pre_run_experiment_plan
experiment_id:
created_at:
operator:
self_review_allowed:
research_question:
geographic_region:
station_list:
time_window:
forecast_source:
observation_source:
lead_times:
residual_definition:
time_alignment_rule:
spatial_alignment_rule:
qc_policy:
terrain_source:
land_cover_source:
train_validation_test_split:
metrics:
baselines:
supported_thresholds:
minimum_sample_floor:
maximum_hypothesis_families:
allowed_analyses:
sensitivity_checks:
human_approval:
notes:
max_ambiguous_iterations: integer
primary_metric_and_threshold:
  metric: string
  threshold: float
proxy_risk_screening_criteria: string
station_selection_filter_criteria: string or object
residual_preinspection_attestation: boolean
strongest_baseline_id: string
allowed_metadata_groupings:
  - string
rigorous_stability_metric_definition: string
```

## Candidate hypothesis schema

```yaml
log_schema_version: "1.1"
entry_type: candidate_hypothesis
experiment_id:
hypothesis_id:
created_at:
proposed_by:
hypothesis_text:
features_used:
station_subset:
allowed_tier_before_validation: SPECULATIVE
related_failed_hypotheses:
notes:
rejection_status: string (e.g., "active", "failed_validation", "rejected_due_to_leakage")
rejection_reason: string
```

## Validation result schema

```yaml
log_schema_version: "1.1"
entry_type: validation_result
experiment_id:
hypothesis_id:
created_at:
evaluator_version:
code_commit_or_snapshot:
data_snapshot_ids:
metrics:
baseline_results:
statistical_tests:
multiple_comparison_correction:
heldout_split_used:
sensitivity_checks_completed:
result_summary:
recommended_claim_tier:
notes:
total_hypothesis_tests_conducted: integer
multiple_comparison_correction_applied: string (e.g., "Bonferroni", "Benjamini-Hochberg", "None")
p_value_raw: float
p_value_adjusted: float
correction_family_size: integer
baseline_comparison_matrix:
  - baseline_id: string
    metric_value: float
    p_value: float
    improvement_over_baseline: float
proxy_risk_assessment_status: string (e.g., "resolved", "unresolved_material_risk", "not_applicable")
```

## Human review schema

```yaml
log_schema_version: "1.1"
entry_type: human_review
experiment_id:
hypothesis_id:
reviewer:
reviewer_role:
self_review: true_or_false
decision:
claim_tier_approved:
reason:
required_followup:
created_at:
statistical_integrity_confirmed: boolean
```

## Failed-result retest schema

```yaml
log_schema_version: "1.1"
entry_type: failed_result_retest_request
new_experiment_id:
new_hypothesis_id:
prior_experiment_id:
prior_hypothesis_id:
reason_for_retest:
parameter_changes:
human_approval:
created_at:
```

## Append-only rule

Never overwrite prior entries. If an entry is wrong, create a correction entry referencing the original entry ID.

## Reproducibility requirement

Every result must be replayable from append-only log entries, frozen code commit or snapshot, exact data snapshot identifiers, recorded alignment/QC rules, and recorded evaluator version.

---
