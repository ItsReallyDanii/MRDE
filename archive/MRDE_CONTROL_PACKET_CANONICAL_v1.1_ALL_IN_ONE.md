# MRDE CONTROL PACKET — CANONICAL v1 ALL-IN-ONE

# FILE: README.md

# Microclimate Residual Discovery Engine (MRDE) — Control Packet

**Status:** Canonical governance draft v1.1  
**Purpose:** Preserve the project’s signal architecture before implementation.  
**Scope:** Project control, governance, validation rules, and research-loop constraints.  
**Not:** Code, a weather model, a safety-critical tool, legal advice, or a final research paper.

## One-sentence identity

**MRDE is a public-data-only, validation-first research framework that detects, tests, and conservatively tiers terrain- and context-conditioned patterns in weather forecast-observation mismatches, starting with 2-meter temperature residuals joined to terrain and land-cover metadata, without making operational forecast-improvement or safety-critical claims.**

## Authority order

If files conflict, apply this authority order:

1. `00_PROJECT_IDENTITY_AND_GLOSSARY.md`
2. `04_EVALUATION_CLAIMS_AND_ASSUMPTIONS.md`
3. `05_SYSTEM_BOUNDARIES_AND_GOVERNANCE.md`
4. `02_SCOPE_LOCK_AND_V0_DEFINITION.md`
5. `03_DATA_ENGINEERING_AND_PROVENANCE.md`
6. All appendices and future-branch notes

## Packet file map

| File | Purpose |
|---|---|
| `00_PROJECT_IDENTITY_AND_GLOSSARY.md` | Identity, non-identity, glossary, language posture |
| `01_DISCOVERY_WITHIN_DISCOVERY.md` | Parent framework and branch relationship |
| `02_SCOPE_LOCK_AND_V0_DEFINITION.md` | v0 scope, geography/station frame, non-expansion rules |
| `03_DATA_ENGINEERING_AND_PROVENANCE.md` | Data sources, versioning, time alignment, QC, model-cycle rules |
| `04_EVALUATION_CLAIMS_AND_ASSUMPTIONS.md` | Claim tiers, baselines, thresholds, pre-run plan, assumptions |
| `05_SYSTEM_BOUNDARIES_AND_GOVERNANCE.md` | Agent permissions, human gates, stop rules, no correction claims in v0 |
| `06_APPEND_ONLY_LOG_SCHEMA.md` | Required JSONL schema and review entries |
| `07_IMPLEMENTATION_ROADMAP_AND_V0_SUCCESS.md` | Execution order and v0 success/failure criteria |
| `APPENDIX_PRIOR_ART.md` | Prior-art summary, non-legal posture |
| `APPENDIX_FUTURE_BRANCHES.md` | Deferred branches with contamination warning |
| `CHANGELOG.md` | Control-packet version history |

## Current stage

The project is ready for **repository placement as a governance/control packet**. It is **not ready for coding** until the v0 experiment plan is logged under the schema in `06_APPEND_ONLY_LOG_SCHEMA.md`.

## Immediate next action after placing this packet

Create a repository or folder and commit this packet as the first governance artifact. Then draft a pre-run v0 experiment plan before any data inspection.

---

# FILE: 00_PROJECT_IDENTITY_AND_GLOSSARY.md

# 00 — Project Identity and Glossary

## Project name

**Microclimate Residual Discovery Engine (MRDE)**

## Parent framework

**Discovery-within-Discovery**

## Canonical identity

MRDE is a public-data-only, validation-first research framework that detects, tests, and conservatively tiers terrain- and context-conditioned patterns in weather forecast-observation mismatches, starting with 2-meter temperature residuals joined to terrain and land-cover metadata, without making operational forecast-improvement or safety-critical claims.

## What MRDE is

MRDE is:

- a residual-pattern validation framework;
- a public-data-only independent-research branch;
- a first executable test branch under Discovery-within-Discovery;
- a governance-first project designed to prevent overclaiming, cherry-picking, and uncontrolled agentic exploration;
- a way to test whether terrain/context metadata is statistically associated with repeatable forecast-observation mismatch patterns.

## What MRDE is not

MRDE is not:

- a new weather model;
- an operational forecast product;
- a safety-critical prediction or warning system;
- a claim that NOAA/NWS/NASA products are wrong or unreliable;
- a claim that AI has discovered weather laws;
- a commercial microclimate alert system;
- a proprietary sensor-network product;
- a replacement for official public weather products;
- legal advice or patent freedom-to-operate analysis.

## Expansion rule

MRDE v0 begins with **2-meter temperature forecast-observation mismatches** only. Expansion beyond 2-meter temperature, HRRR/ASOS-style data, or terrain/land-cover metadata requires a human-gated scope amendment and a new experiment ID.

## Glossary

**Discovery-within-Discovery**  
The broader research philosophy: finding meaningful secondary patterns inside existing scientific or operational data systems by analyzing residuals, metadata, timing, failures, gaps, ordering, topology, and mismatch behavior.

**Residual**  
For MRDE v0, a residual means a forecast-observation mismatch. It does not automatically mean forecast error or causal model failure.

**Forecast-observation mismatch**  
The numeric difference or structured discrepancy between a public forecast value and an observed public measurement after defined spatial/temporal alignment rules.

**Context feature**  
A non-target feature used to describe conditions around a residual. Examples: elevation, slope, aspect, land cover, time of day, forecast lead time, station metadata.

**Terrain-conditioned pattern**  
A residual pattern statistically associated with terrain/context features. This term does not imply causality.

**Holdout**  
A pre-defined data subset not used for exploratory model fitting or hypothesis generation. Holdout data may only be used for validation under the logged experiment plan.

**Validation**  
The process of testing a candidate pattern against pre-defined metrics, baselines, splits, and thresholds.

**SUPPORTED**  
A claim tier assigned only when pre-registered thresholds, held-out validation, baseline comparisons, statistical controls, and human review are satisfied.

**Agentic loop**  
A bounded LLM-assisted loop that may propose candidate features, groupings, or hypotheses, but may not alter baselines, splits, data sources, claim tiers, or governance rules.

**Human gate**  
A required human approval point. Human approval must be logged in the append-only log.

**Sensitivity check**  
A required robustness check testing whether a candidate pattern is stable under limited, pre-defined perturbations. v0 minimum sensitivity checks: one time-alignment tolerance variant, one leave-one-station-out check, and one baseline-comparison stability check. For station sets where N < 10, a standard leave-one-station-out check is insufficient alone for a SUPPORTED_PATTERN claim; a more rigorous stability metric must be declared in the pre-run experiment plan.

**Correction claim**  
Any claim that a rule, model, or feature improves forecast accuracy. Correction claims are out of scope for MRDE v0.

## Language posture

Preferred language:

- forecast-observation mismatch
- residual pattern
- terrain-conditioned residual pattern
- metadata-conditioned discrepancy
- held-out validation
- candidate hypothesis
- supported/ambiguous/failed finding

Avoid:

- AI discovered weather truth
- hidden laws
- deterministic microclimate signal
- proves the forecast model is wrong
- operational forecast improvement
- safety-critical prediction
- superior weather model
- causal explanation without additional mechanism and validation

---

# FILE: 01_DISCOVERY_WITHIN_DISCOVERY.md

# 01 — Discovery-within-Discovery

## Umbrella thesis

Many public scientific and operational systems contain secondary signals in their residuals, metadata, timing, failures, gaps, ordering, topology, and mismatch patterns.

Instead of trying to directly replace large scientific models, the framework studies the artifacts, discrepancies, and operational traces those systems leave behind.

## General template

1. Identify an existing public system.
2. Collect predictions, observations, metadata, logs, or quality flags.
3. Compute mismatches or secondary signals.
4. Attach contextual features.
5. Mine candidate repeatable patterns.
6. Test those patterns on held-out data.
7. Assign claim tiers.
8. Preserve positive, ambiguous, and failed findings.

## MRDE’s position

MRDE is one branch:

- Parent framework: Discovery-within-Discovery
- Intermediate branch: Residual Discovery Engine
- First executable branch: Microclimate Residual Discovery Engine

MRDE must not consume the whole umbrella. Weather/microclimate is the first controlled validation target, not the entire framework.

## Generic future-branch requirements

Any future Discovery-within-Discovery branch must define:

- target system;
- residual/mismatch definition;
- public data sources;
- baseline comparisons;
- holdout strategy;
- claim tiers;
- human gates;
- stop rules;
- append-only logging;
- anti-overclaim language.

## Current active branch

Only MRDE v0 is active. All other branches are deferred unless explicitly activated through human-gated scope amendment.

---

# FILE: 02_SCOPE_LOCK_AND_V0_DEFINITION.md

# 02 — Scope Lock and v0 Definition

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

# FILE: 03_DATA_ENGINEERING_AND_PROVENANCE.md

# 03 — Data Engineering and Provenance

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

# FILE: 04_EVALUATION_CLAIMS_AND_ASSUMPTIONS.md

# 04 — Evaluation, Claims, and Assumptions

## Core principle

A claim tier is the output of a validation contract. No claim may be upgraded based only on narrative plausibility or visual pattern quality.

## Critical assumption

Residual = forecast-observation mismatch only.

A residual may reflect forecast model limitation, observation artifact, station siting bias, sensor drift, time mismatch, spatial interpolation error, QC failure, terrain mismatch, data join bug, or model version change.

No causal attribution is permitted without additional mechanistic evidence. Before assigning SUPPORTED_PATTERN status, the operator must perform a proxy-risk assessment, including correlation/proxy screening for context features where possible. If material proxy risk remains unresolved under the pre-run criteria, the claim must be downgraded to AMBIGUOUS.

## Pre-run experiment plan requirement

Before data inspection, every experiment must create a pre-run experiment plan entry in the append-only log.

The pre-run entry must include:

- experiment ID;
- research question;
- geographic region;
- station list;
- time window;
- forecast source;
- observation source;
- lead times;
- residual definition;
- time-alignment rule;
- spatial-alignment rule;
- QC policy;
- train/validation/test split;
- metrics;
- baselines;
- thresholds for SUPPORTED;
- allowed analyses;
- maximum hypothesis families;
- sensitivity checks;
- human approval status.

No claim may be labeled SUPPORTED unless thresholds were explicitly set in the pre-run experiment plan. If no experiment-specific thresholds are defined before data inspection, the strongest possible claim tier is AMBIGUOUS.

## Required baselines

Every candidate pattern must be compared against:

1. raw public forecast;
2. persistence baseline;
3. climatology baseline when available;
4. simple station-wise or lead-time bias correction;
5. metadata-agnostic model when relevant.

To achieve SUPPORTED_PATTERN status, a candidate pattern must satisfy the pre-registered validation criterion against the strongest baseline defined in the pre-run experiment plan, using the pre-registered primary metric and threshold. Success against only a subset of weaker baselines is insufficient.

## Metrics

Minimum v0 metrics:

- bias / mean error;
- MAE;
- RMSE;
- residual magnitude by station;
- residual magnitude by terrain/context group;
- baseline-relative skill where appropriate.

## Statistical controls

The experiment plan must specify mandatory statistical controls before data inspection.

Default v0 minimum:

- one paired nonparametric test or permutation test for pattern difference;
- multiple-comparison correction if more than one hypothesis family or feature grouping is tested;
- Benjamini-Hochberg FDR or Bonferroni must be specified before validation.

The agent may not choose the weakest statistical test after seeing results. The pre-run experiment plan must explicitly list all allowed metric combinations and metadata-grouping variables (e.g., specific land-cover classes, elevation bins). Any grouping or metric not pre-registered is strictly prohibited for use in SUPPORTED status claims.

## Claim tiers

### SPECULATIVE

A candidate pattern or hypothesis generated from exploratory analysis.

### AMBIGUOUS

A pattern shows some support but fails one or more validation requirements.

### SUPPORTED_PATTERN

A residual-pattern claim may be labeled SUPPORTED_PATTERN only if all requirements below are met:

- pre-run thresholds were set before data inspection;
- held-out validation passes;
- baseline comparisons are reported;
- p-adjusted ≤ 0.05 where statistical testing applies;
- at least one independent holdout split supports the pattern;
- minimum sample/station floor from the pre-run plan is satisfied;
- nontrivial effect is demonstrated, with default safeguard of Cohen's d ≥ 0.2 or ≥10% residual-magnitude separation between compared groups unless stricter experiment thresholds are specified;
- no unresolved data-artifact explanation remains;
- sensitivity checks do not reverse the conclusion;
- human approval is logged.

Any candidate pattern that fails the strongest-baseline requirement, fails the specified sensitivity checks, or has unresolved material proxy risk under the pre-run criteria is strictly prohibited from being labeled SUPPORTED_PATTERN and must be downgraded to AMBIGUOUS or FAILED.

### SUPPORTED_CORRECTION

Correction claims are **out of scope for MRDE v0**.

MRDE v0 may report whether a candidate pattern is associated with residual structure, but it may not claim that any rule improves forecast accuracy.

A future correction-claim lane requires a separate human-gated sub-contract and new experiment ID.

### FAILED

A hypothesis is FAILED if it fails validation, underperforms baseline, cannot be reproduced, or is invalidated by sensitivity checks.

FAILED findings must be preserved.

## Post-hoc analysis rule

Any pattern identified via post-hoc exploration must be logged as SPECULATIVE.

It can only be evaluated for SUPPORTED status on new held-out data or a future dataset, not on the same sample used to find it.

## Failed-result reuse policy

A previously FAILED hypothesis may only be retested under a new hypothesis ID with original failure reference, documented retest reason, parameter changes, a new pre-run plan, and human approval.

A failed result may not be quietly iterated into SUPPORTED status.

## Operator/reviewer rule

The same human may act as operator and reviewer only if self-review is explicitly logged.

Human approval does not erase the need for pre-run thresholds, held-out validation, and reproducibility.

---

# FILE: 05_SYSTEM_BOUNDARIES_AND_GOVERNANCE.md

# 05 — System Boundaries and Governance

## Core rule

LLM proposes. Evaluator scores. Human promotes.

## v0 agent status

For MRDE v0, the agentic loop is advisory only.

The agent may suggest features, groupings, and analysis ideas, but may not execute autonomous search, change scope, change data, change metrics, change thresholds, or upgrade claims.

## Agent may do

The agent may propose feature combinations, station groupings, simple residual-pattern hypotheses, stratification ideas, result summaries, failed-path notes, and follow-up tests.

## Agent may not do

The agent may not change held-out split, evaluator metric, data sources, claim tiers, public language, station selection after residual inspection, or governance rules.

The agent may not run reinforcement-learning, AutoML-style, or arbitrary model-family search loops in v0.

## Human gates

Human approval is required for:

- claim-tier upgrade;
- new data source;
- new variable;
- new geographic region;
- station-list change after logging;
- held-out split change;
- validation metric change;
- baseline definition change;
- evaluator change;
- public-facing language;
- causal explanation;
- expansion beyond 2-meter temperature;
- transition from advisory-only agent to bounded proposal mode.

All human approvals must be logged.

## Stop rules

Stop the run or downgrade the claim if:

- no baseline exists;
- no pre-run experiment plan exists;
- data alignment is uncertain;
- residuals are not reproducible;
- held-out data was leaked;
- region/station frame changed after inspection;
- pattern works only on one cherry-picked station/event;
- p-values fail correction after multiple testing;
- observation artifact is plausible and unresolved;
- model/version changes are pooled without stratification;
- code/evaluator cannot be deterministically replayed;
- generated explanation uses causal language without evidence;
- compute/time/token budget is exceeded;
- no improvement or stability after predefined iterations;
- a post-hoc pattern is presented as confirmatory.

A single hypothesis may not undergo more than the `max_ambiguous_iterations` (declared in the pre-run experiment plan) while in AMBIGUOUS status. Any attempt to re-test the same hypothesis after this limit requires a new experiment ID and a new human-gated pre-run plan.

## Runtime limits

| Limit | Value |
|---|---|
| max_candidate_variants_per_session | 25 |
| max_failed_iterations_before_review | 10 |
| max_runtime_per_candidate | 10 minutes |
| absolute_runtime_override | 30 minutes with human approval |
| max_hypothesis_families_per_dataset | must be set in pre-run plan |

Any longer run requires a separate human-gated experiment entry.

## Correction-claim restriction

MRDE v0 does not make forecast-improvement or correction claims.

If a candidate rule appears to reduce forecast error, the result may be logged as exploratory or AMBIGUOUS, but no SUPPORTED_CORRECTION claim may be made in v0.

## Conflict resolution

If an agent recommendation conflicts with any governance file, the governance file wins.

If governance files conflict, apply the authority order in `README.md`.

---

# FILE: 06_APPEND_ONLY_LOG_SCHEMA.md

# 06 — Append-Only Log Schema

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

# FILE: 07_IMPLEMENTATION_ROADMAP_AND_V0_SUCCESS.md

# 07 — Implementation Roadmap and v0 Success Criteria

## Purpose

This file defines what happens after the control packet is placed in a repository or project folder.

## Phase 0 — Governance placement

Done when:

- this control packet is committed or stored as the canonical governance artifact;
- `CHANGELOG.md` records the initial version;
- no code has been written yet;
- v0 experiment plan has not yet inspected data.

## Phase 1 — Pre-run experiment plan

Done when a `pre_run_experiment_plan` entry exists with region, stations, time window, source definitions, QC policy, alignment rules, baselines, metrics, SUPPORTED thresholds, sensitivity checks, and human approval.

## Phase 2 — Deterministic data pipeline

Done when forecasts, observations, and terrain/land-cover metadata are ingested with logged provenance.

## Phase 3 — Residual table and baselines

Done when forecast-observation mismatches and required baseline metrics are reproducible.

## Phase 4 — Candidate pattern analysis

Done when candidate hypotheses are logged, validation/sensitivity checks are run, claim tiers are assigned through human review, and failed findings are preserved.

## v0 success bar

MRDE v0 is complete when a reproducible pipeline produces either:

1. at least one SUPPORTED_PATTERN or AMBIGUOUS terrain/context-conditioned residual finding; or
2. a fully documented FAILED result;

from a 3–5 station, 90-day HRRR vs ASOS/METAR pilot with frozen baselines, append-only logs, and human sign-off.

A clean FAILED result still counts as v0 completion if the pipeline is reproducible and the failure is properly logged.

## v0 non-success

v0 is not complete if no pre-run plan exists, residuals cannot be reproduced, data alignment is unresolved, stations changed after inspection, claim tiers lack logged thresholds, or the pipeline only produces narrative explanation without metrics.

## No coding condition

Do not write implementation code until Phase 1 is complete.

---

# FILE: APPENDIX_PRIOR_ART.md

# Appendix — Prior Art Notes

## Status

This appendix summarizes prior-art direction only. It is not legal advice nor does it establish freedom to operate.

## Current posture

External reviews found overlap with:

- forecast verification;
- model output statistics and bias correction;
- microclimate modeling;
- terrain-aware forecasting;
- UAV-based urban wind/microclimate systems;
- generic residual learning;
- evaluator-driven LLM/code-search systems such as FunSearch/AlphaEvolve-style loops.

## Safer MRDE lane

MRDE should stay framed as public-data-only, validation-first, residual-pattern analysis, transparent claim-tiering, non-operational, non-safety-critical, and not a commercial correction or alerting product.

## Avoided lanes

Avoid framing MRDE as proprietary microclimate prediction, UAV telemetry wind estimation, operational routing/alerting, commercial forecast correction, legal freedom-to-operate determination, or autonomous scientific discovery without human validation.

## Dossier rule

Detailed literature, patent, and LLM review notes should live in a separate research dossier, not in the core governance files.

---

# FILE: APPENDIX_FUTURE_BRANCHES.md

# Appendix — Future Branches

## Contamination warning

These branches are preserved for strategic continuity only. They are not active MRDE v0 scope.

A future branch may not be treated as active unless a human-gated scope amendment creates a new project branch and experiment plan.

## Deferred branches

### Satellite Metadata Anomaly Engine

Study QA flags, cloud masks, missingness, and satellite product timing.

### Public Data-Quality / Missingness Engine

Study outage patterns, station reliability, data gaps, update delays, and QC behavior.

### Flood / Topography Discrepancy Engine

Study terrain, precipitation, flood reports, and mismatch patterns.

### Forecast Blind-Spot Mapper

Map repeated forecast-observation mismatches by geography, terrain class, season, and lead time.

### Dataset Archaeology Framework

Study scientific datasets as historical/operational systems whose metadata and failure modes contain information.

## Activation requirement

Any branch requires branch identity, data sources, residual/mismatch definition, baselines, holdout strategy, claim tiers, human gates, stop rules, and append-only log compatibility.

---

# FILE: CHANGELOG.md

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