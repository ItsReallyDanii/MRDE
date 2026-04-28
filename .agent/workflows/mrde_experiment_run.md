---
description: Execute the approved MRDE experiment workflow from pre-run plan through logging, without changing locked rules.
---

# MRDE Experiment Run Workflow

Use only after Stage 0 is complete and a pre-run plan is being prepared or has already been approved.

1. Read `experiments/EXP001/PRE_RUN_PLAN.md`, `08_APPEND_ONLY_LOG_SCHEMA.md`, `05_DATA_ENGINEERING_AND_PROVENANCE.md`, and `09_IMPLEMENTATION_ROADMAP_AND_V0_SUCCESS.md`.
2. Confirm the experiment ID, region, station list, time window, data sources, lead times, QC policy, alignment rules, baselines, metrics, thresholds, sensitivity checks, and allowed metadata groupings are filled.
3. Confirm `residual_preinspection_attestation: true` in the pre-run plan before any data step. If false or unknown, STOP.
4. Confirm station selection was done with the pre-declared `station_selection_filter_criteria` and not residual behavior.
5. Confirm `strongest_baseline_id` is defined and appears in the baseline list.
6. Confirm the required append-only `pre_run_experiment_plan` entry exists or prepare it before data work.
7. For later stages only, follow the pipeline sequence from `09_IMPLEMENTATION_ROADMAP_AND_V0_SUCCESS.md`:
   - deterministic data pipeline
   - residual table and baselines
   - candidate pattern analysis
   - validation and claim-tier assignment
8. At each step, record required provenance fields from `05_DATA_ENGINEERING_AND_PROVENANCE.md`.
9. Do not change locked definitions after residual inspection. If a change is needed, close the run and create a new experiment ID.
10. Produce a run report with allowed/blocked status, missing fields, provenance gaps, and required log entries.
