---
name: mrde-validation-reviewer
description: Use after validation outputs exist to check metrics, baselines, holdouts, statistical controls, sensitivity checks, and proxy-risk assessment.
---

# MRDE Validation Reviewer

## Purpose

Use this skill only after validation outputs exist. It checks whether a candidate pattern can be recommended for SPECULATIVE, AMBIGUOUS, SUPPORTED_PATTERN, or FAILED status without changing the locked validation rules.

## Required context files

Read in this order:

1. `06_EVALUATION_CLAIMS_AND_ASSUMPTIONS.md`
2. `08_APPEND_ONLY_LOG_SCHEMA.md`
3. `experiments/EXP001/PRE_RUN_PLAN.md`
4. `experiments/EXP001/VALIDATION_REPORT.md`
5. `experiments/EXP001/CLAIM_REVIEW.md` if present
6. `logs/append_only_log.jsonl`

## SUPPORTED_PATTERN checklist

A candidate may be recommended as `SUPPORTED_PATTERN` only if all are true:

1. Pre-run thresholds were set before data inspection.
2. Held-out validation passes.
3. Baseline comparisons are reported.
4. Strongest baseline requirement passes using `strongest_baseline_id`.
5. Statistical testing passes where applicable, including adjusted p-value threshold.
6. Minimum sample/station floor from the pre-run plan is satisfied.
7. Nontrivial effect is demonstrated using the pre-registered primary metric/threshold.
8. No unresolved data-artifact explanation remains.
9. Sensitivity checks do not reverse the conclusion.
10. Proxy-risk assessment is resolved or not material under the pre-run criteria.
11. Human approval is logged before final claim-tier promotion.

## Required validation artifacts

Check that the validation result includes:

- `baseline_comparison_matrix`
- `proxy_risk_assessment_status`
- `p_value_raw`
- `p_value_adjusted`
- `multiple_comparison_correction_applied`
- `heldout_split_used`
- `sensitivity_checks_completed`
- `evaluator_version`
- `code_commit_or_snapshot`
- `data_snapshot_ids`

## Procedure

1. Confirm a pre-run plan exists and predates data inspection.
2. Confirm validation uses the locked metrics, baselines, thresholds, splits, and groupings.
3. Evaluate each SUPPORTED_PATTERN checklist item as PASS / FAIL / UNKNOWN.
4. Inspect `baseline_comparison_matrix`; strongest baseline must pass for SUPPORTED_PATTERN.
5. Inspect `proxy_risk_assessment_status`; unresolved material risk blocks SUPPORTED_PATTERN.
6. Inspect `p_value_adjusted` and multiple-comparison correction where statistical testing applies.
7. Determine the maximum allowed tier based on failures/unknowns.
8. Do not alter thresholds, metrics, station list, baselines, or splits.

## Output format

Return:

- `verdict`: ALLOWED / BLOCKED / NEEDS_HUMAN_APPROVAL
- `maximum_allowed_tier`: SPECULATIVE / AMBIGUOUS / SUPPORTED_PATTERN / FAILED
- `checklist`: table of PASS / FAIL / UNKNOWN
- `strongest_baseline_status`: PASS / FAIL / UNKNOWN
- `proxy_risk_status`: resolved / unresolved_material_risk / not_applicable / unknown
- `p_adjusted_status`: PASS / FAIL / UNKNOWN / not_applicable
- `human_review_required`: yes/no
- `required_log_entry`: yes/no

## Hard stops

Stop if:

- validation uses thresholds or groupings not pre-registered;
- heldout data leaked;
- strongest baseline fails;
- sensitivity checks reverse the result;
- proxy risk is unresolved but the requested tier is SUPPORTED_PATTERN;
- human review is missing for final promotion.
