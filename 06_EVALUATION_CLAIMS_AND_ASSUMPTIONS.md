# 06 — Evaluation, Claims, and Assumptions

## Core principle

A claim tier is the output of a validation contract. No claim may be upgraded based only on narrative plausibility or visual pattern quality.

## Critical assumption

Residual = forecast-observation mismatch only.

A residual may reflect forecast model limitation, observation artifact, station siting bias, sensor drift, time mismatch, spatial interpolation error, QC failure, terrain mismatch, data join bug, or model version change.

No causal attribution is permitted without additional mechanistic evidence. Before assigning SUPPORTED_PATTERN status, the operator must perform a proxy-risk assessment, including correlation/proxy screening for context features where possible. If material proxy risk remains unresolved under the pre-run criteria, the claim must be downgraded to AMBIGUOUS.

ASOS/METAR stations are typically collocated with airports. Station microenvironment characteristics, including paved surface fraction, proximity to tarmac, wind exposure, irrigation, local thermal mass, and other siting factors, must be documented as potential proxy confounds when terrain or land-cover class is the feature of interest.

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
- Benjamini-Hochberg FDR or Bonferroni must be specified before validation;
- time-series validation splits must be temporal, such as a held-out trailing time window or another pre-declared time-block split. Random splits across time-correlated meteorological observations are prohibited for validation metrics or SUPPORTED_PATTERN eligibility.

Minimum v0 sensitivity checks:

- one time-alignment tolerance variant;
- one leave-one-station-out check, with a stronger pre-declared stability metric required when station count is below 10;
- one baseline-comparison stability check;
- one stratification check by time-of-day bin, such as daytime versus nighttime using local solar time;
- one stratification check by season or month, unless infeasible for the selected window, in which case the infeasibility must be logged before validation.

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
- no unresolved data-artifact explanation remains, including unresolved station-siting, airport microenvironment, grid-to-point elevation mismatch, temporal autocorrelation leakage, QC, or model-cycle explanations;
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
