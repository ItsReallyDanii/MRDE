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
