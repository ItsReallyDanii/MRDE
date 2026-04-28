# 09 — Implementation Roadmap and v0 Success Criteria

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
