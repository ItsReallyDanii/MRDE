---
name: mrde-append-log-writer
description: Use when creating JSONL-compatible entries for experiment events, decisions, validation results, stop rules, scope amendments, or human reviews.
---

# MRDE Append-Only Log Writer

## Purpose

Use this skill to create append-only JSONL entries that preserve experiment history without overwriting prior entries.

## Required context files

Read in this order:

1. `08_APPEND_ONLY_LOG_SCHEMA.md`
2. `schemas/append_only_log.schema.json`
3. `schemas/pre_run_plan.schema.json` when `entry_type=pre_run_experiment_plan`
4. `schemas/claim_review.schema.json` when writing claim review or human review entries
5. `logs/append_only_log.jsonl`
6. Relevant experiment files under `experiments/`

## Entry-type procedure

1. Identify the requested `entry_type` before writing anything.
2. Confirm the entry type is one of the allowed schema values:
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
3. Check required fields for that entry type using `08_APPEND_ONLY_LOG_SCHEMA.md`.
4. For `pre_run_experiment_plan`, also validate against `schemas/pre_run_plan.schema.json`.
5. For `validation_result`, require baseline results, statistical tests, multiple-comparison correction, heldout split, sensitivity checks, p-values, baseline comparison matrix, and proxy-risk status when applicable.
6. For `human_review` or `claim_tier_assignment`, validate claim tier against `06_EVALUATION_CLAIMS_AND_ASSUMPTIONS.md` and `schemas/claim_review.schema.json`.
7. Append exactly one JSON object as one JSONL line. Never rewrite, reorder, or delete prior lines.
8. If correcting a prior entry, create a new correction entry referencing the original entry.

## Output format

Return:

- `verdict`: ALLOWED / BLOCKED / NEEDS_HUMAN_APPROVAL
- `entry_type`: string
- `missing_required_fields`: list
- `schema_checked`: list
- `jsonl_entry`: one-line JSON object, if allowed
- `append_only_safe`: yes/no

## Hard stops

Stop if the request asks to:

- overwrite or delete prior log entries;
- create a SUPPORTED claim entry without human review;
- create a result entry without code/data snapshot identifiers where required;
- create a pre-run entry after residual inspection and present it as pre-inspection.
