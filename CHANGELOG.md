# Changelog

## v1.2 — EXP001 Pre-Run Experiment Plan Filed and Stage 1 PASSED

**Date:** 2026-04-28T05:44:17Z UTC
**Stage:** Stage 1 — Pre-run experiment plan
**Status:** PASSED

### Added

- Filed and human-approved `experiments/EXP001/PRE_RUN_PLAN.md`: five-station Oregon multi-terrain transect (AST, SLE, MFR, SXT, RDM), 90-day summer 2024 window, HRRR/ASOS sources, four lead times, temporal train/validation/test split, full baselines, thresholds, sensitivity checks, and proxy-risk criteria. All fields filled before any residual inspection.
- Appended `pre_run_experiment_plan` JSONL entry to `logs/append_only_log.jsonl` (entry 4).
- Updated `02_STAGE_GATE_PLAN.md` Stage 1 status from `IN_PROGRESS` to `PASSED`; Stage 2 unblocked.
- Added D004 to `DECISIONS.md`.

### Not changed

- No data pipeline code added.
- No residuals inspected.
- No validation claims created.
- No correction-claim lane created.
- No station selected based on residual behavior.

## v2.1 — Second-Pass Audit Cleanup

Applied targeted cleanup from the second-pass audit report.

### Included changes
- Replaced the `residual_preinspection_attestation: false` pre-run template trap with a placeholder that must be set to `true` only after confirming no residual inspection occurred.
- Added temporal split requirements for time-correlated meteorological validation; random splits are prohibited for SUPPORTED_PATTERN eligibility.
- Hardened `schemas/pre_run_plan.schema.json` to require `train_validation_test_split`, `sensitivity_checks`, and `proxy_risk_screening_criteria` with temporal/proxy-risk guidance.
- Added ASOS airport siting bias as an expected proxy-risk concern.
- Added HRRR grid-point-versus-station elevation mismatch as a proxy-risk concern.
- Added diurnal and seasonal/month stratification checks to minimum v0 sensitivity guidance.
- Added a current stage status table showing Stage 0 `PASSED`, Stage 1 `IN_PROGRESS`, and Stages 2–7 `NOT_STARTED`.
- Appended an append-only correction entry normalizing Stage 0 status to canonical `PASSED`.
- Updated `mrde-prerun-plan-writer` skill description and `MRDE_CONTEXT.md` current-stage language.
- Marked `ONE_PASS_CHECK.md` as a single-use review artifact, not live governance.
- Updated `README.md` current revision/status wording to reflect Stage 0 `PASSED` and Stage 1 `IN_PROGRESS`.

### Not changed
- No data pipeline code added.
- No data sources selected.
- No station list selected.
- No residuals inspected.
- No validation claims created.
- No correction-claim lane created.

## Packaging pass — 2026-04-28T04:39:22Z UTC

### Added

- Added `01_MASTER_COMPLETION_CONTRACT.md` as root project completion contract.
- Added `02_STAGE_GATE_PLAN.md` for full project stage gates.
- Added `10_PUBLIC_LANGUAGE_RULES.md` for public claim control.
- Added Antigravity-oriented `AGENTS.md`, `GEMINI.md`, `.agent/rules`, `.agent/skills`, `.agent/workflows`, and `.agent/knowledge` scaffold.
- Added `plans/`, `experiments/`, `logs/`, and `schemas/` scaffolds.
- Archived original all-in-one control packet in `archive/`.

### Refactored

- Split the uploaded `MRDE_CONTROL_PACKET_CANONICAL_v1.1_ALL_IN_ONE.md` into repository-facing files.
- Renumbered split files to insert the master completion contract and stage gate plan without losing the original packet content.


## Post-Claude minor-revision cleanup — 2026-04-28T04:51:26Z UTC

### Changed

- Moved `CLAUDE_REVIEW_PROMPT.md` from project root to `archive/CLAUDE_REVIEW_PROMPT.md`.
- Updated `README.md` folder map to include `ONE_PASS_CHECK.md`, `PACKAGE_MANIFEST.md`, and archived review prompt.
- Clarified that `README.md` hosts the authority order but is not itself a governance document.
- Aligned `AGENTS.md` authority order with `README.md`, including experiments, appendices, and current user instruction handling.
- Clarified `.agent/rules/MRDE_ALWAYS_ON_RULES.md` authority-order wording.
- Replaced generic/copy-paste skill procedures with task-specific procedures for governance review, doc change control, pre-run planning, append-only logging, claim-tier auditing, and validation review.
- Replaced generic/copy-paste workflow procedures with stage-gate, experiment-run, and claim-review-specific workflows.
- Removed undocumented `NO_CLAIM` from `schemas/claim_review.schema.json`.
- Added initial Stage 0 `changelog_entry` to `logs/append_only_log.jsonl`.

### Not changed

- No data pipeline code added.
- No data sources selected.
- No station list selected.
- No residuals inspected.
- No validation claims created.
- No correction-claim lane created.

### Preserved from v1.1

# Changelog

## v1.1 — Governance Hardening Patch

### Included hardening changes
- Integrated Station-selection blind lock to prevent post-hoc station picking.
- Required the pre-registered validation criterion to be satisfied against the strongest baseline.
- Implemented Metric and Grouping Freeze to prevent subgroup p-hacking.
- Added requirement for multiple-comparison logging (raw/adjusted p-values).
- Added mandatory logging of rejected/failed hypotheses.
- Integrated Baseline Comparison Matrix for all declared baselines.
- Implemented Proxy-risk assessment requirement for terrain-conditioned claims.
- Added AMBIGUOUS status iteration limit (`max_ambiguous_iterations`).
- Added requirement for rigorous stability metrics for small-N station sets.
- Hardened schema to capture pre-run thresholds, proxy criteria, and human statistical verification.

## v1.0 — Canonical Governance Draft

Initial split control packet created from the MRDE canonical draft and external audit feedback.

### Included hardening changes
- Correction claims forbidden in v0.
- SUPPORTED claims require pre-run thresholds.
- Geography and station frame must be pre-specified.
- Pre-run experiment plan added as required log entry.
- Model/QC version-change stratification rule added.
- Runtime limit set to 10 minutes default, 30 minutes max with human approval.
- `log_schema_version: "1.1"` added to required log schema.
- Station-selection criteria added.
- Sensitivity-check definition added.
- Failed-result retest policy added.
- Prior art and future branches moved to appendices.
- Precedence/authority order added in README.

### Next expected version

v1.2 should only be created after the first v0 pre-run experiment plan is drafted or if an additional governance correction is required.


## v2.2 — Stage 2 Data Pipeline Closeout

**Date:** 2026-04-28T08:08:17Z UTC
**Stage:** Stage 2 — Deterministic data pipeline
**Status:** PASSED (with NLCD deferred)

### Added
- Station metadata freeze completed.
- ASOS ingestion and QC completed.
- HRRR extraction completed.
- Elevation metadata completed via USGS EPQS online query.
- NLCD land cover explicitly blocked and deferred (Decision D005).
- SXT flagged for low ASOS completeness and elevation mismatch preserved.

### Not changed
- No residuals computed.
- No ASOS-HRRR alignment performed.
- No Stage 3 work started.

## v2.2 — Stage 2 Data Pipeline Closeout

**Date:** 2026-04-28T08:08:32Z UTC
**Stage:** Stage 2 — Deterministic data pipeline
**Status:** PASSED (with NLCD deferred)

### Added
- Station metadata freeze completed.
- ASOS ingestion and QC completed.
- HRRR extraction completed.
- Elevation metadata completed via USGS EPQS online query.
- NLCD land cover explicitly blocked and deferred (Decision D005).
- SXT flagged for low ASOS completeness and elevation mismatch preserved.

### Not changed
- No residuals computed.
- No ASOS-HRRR alignment performed.
- No Stage 3 work started.
