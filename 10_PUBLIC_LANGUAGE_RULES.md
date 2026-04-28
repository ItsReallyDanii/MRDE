# 10 — Public Language Rules

## Purpose

This file controls how MRDE is described in READMEs, reports, summaries, posts, demos, and handoff prompts.

## Safe short description

MRDE is a public-data-only research framework for detecting and validating repeatable forecast-observation mismatch patterns associated with terrain, land cover, timing, and station context.

## Preferred language

Use:

- forecast-observation mismatch;
- residual pattern;
- terrain-conditioned association;
- metadata-conditioned discrepancy;
- held-out validation;
- candidate hypothesis;
- supported/ambiguous/failed finding;
- public-data residual analysis;
- validation-first research scaffold.

## Forbidden or unsafe language in v0

Avoid:

- beats NOAA;
- predicts weather better than official models;
- AI discovered hidden weather laws;
- forecast correction engine;
- microclimate oracle;
- operational weather system;
- safety-critical alerting;
- proves HRRR/NWS/NOAA is wrong;
- causal terrain effect unless separately validated.

## If a pattern is found

Allowed:

> This pilot found a repeatable forecast-observation mismatch pattern associated with pre-declared terrain/context features under locked validation rules.

Not allowed:

> This proves MRDE improves weather forecasting.

## If no pattern is found

Allowed:

> This pilot produced a clean failed result under the pre-registered validation contract. The pipeline remains useful because it preserved provenance, baselines, and negative evidence.

Not allowed:

> The project failed.

## Public release gate

Before public wording is approved, check:

1. Does it claim correction or forecast improvement?
2. Does it imply causality without mechanism?
3. Does it hide failed or ambiguous results?
4. Does it overgeneralize beyond the tested region/window/stations?
5. Does it preserve the non-operational/non-safety-critical boundary?

If any answer is unsafe, block release until revised.
