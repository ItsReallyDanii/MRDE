# 01 — Master Completion Contract

## Purpose

This file defines the full MRDE project finish line. It is the root contract for all project docs, Antigravity rules, skills, workflows, implementation plans, experiment files, and public claims.

## Root project question

Can we build an AI-assisted system that discovers microclimate / weather forecast blind spots from public data by identifying, validating, and conservatively tiering repeatable forecast-observation mismatch patterns?

## Part 1 question

Can we first define a legally/academically safer, validation-first research framework that prevents overclaiming before touching data?

## Relationship between Part 1 and the full project

Part 1 is the governance/control layer. It is necessary but not sufficient. The full project is not complete until MRDE has executed at least one reproducible pilot under the governance rules and produced a properly tiered outcome.

## Overall completion definition

MRDE is complete at the research-system level when all of the following exist:

1. A stable governance/control packet.
2. A master completion contract.
3. Antigravity/agent rules that enforce the governance contract.
4. A pre-run experiment plan logged before any residual inspection.
5. A deterministic public-data pipeline for forecasts, observations, and context metadata.
6. A reproducible residual table.
7. Required baselines and metrics.
8. Append-only candidate hypothesis logging.
9. Validation results assigning SPECULATIVE, AMBIGUOUS, SUPPORTED_PATTERN, or FAILED.
10. A human-reviewed claim decision.
11. A final report preserving successes, ambiguities, failures, assumptions, and limitations.

A clean FAILED result counts as completion if the pipeline and validation contract worked.

## What finding a pattern means

A valid v0 finding means only this:

> Under a locked experiment plan, a terrain/context condition was repeatedly associated with a forecast-observation mismatch pattern that survived the required validation checks.

It does not mean:

- MRDE predicts weather better than NOAA/NWS or HRRR;
- MRDE discovered a causal weather law;
- MRDE can fill missing weather data like a jigsaw puzzle;
- MRDE is an operational forecast product;
- MRDE can make forecast-correction claims in v0.

## Claim ladder

| Level | Meaning | Allowed in v0? |
|---|---|---:|
| Residual pattern | A mismatch association exists under locked rules | Yes |
| Replicated residual pattern | Pattern appears in independent regions/windows | Future |
| Mechanistic explanation | A plausible physical or data-system explanation is supported | Future |
| Correction candidate | A rule might improve forecast accuracy | No |
| Validated correction layer | Out-of-sample forecast improvement is demonstrated | No |
| Operational forecast product | Real-world forecast use | No |

## Stage completion gates

| Gate | Output | Completion condition |
|---|---|---|
| Gate 0 | Governance package | Docs exist and conflicts resolved by authority order |
| Gate 1 | Pre-run experiment plan | Region, stations, dates, metrics, baselines, thresholds, and approval logged before data inspection |
| Gate 2 | Data pipeline | Forecasts, observations, terrain, land-cover, and metadata are reproducibly ingested |
| Gate 3 | Residual table | Forecast-observation mismatches are computed with QC and alignment provenance |
| Gate 4 | Candidate hypotheses | Hypotheses are logged append-only and cannot be silently revised |
| Gate 5 | Validation | Baselines, holdouts, stats, sensitivity checks, and proxy-risk review are complete |
| Gate 6 | Claim review | Human review assigns or rejects claim tier |
| Gate 7 | Final artifact | Repo/report preserves methods, results, failures, limits, and non-claims |

## Termination conditions

Terminate, pause, or mark the current run FAILED if any of the following occur:

- no valid pre-run plan exists before residual inspection;
- station selection is contaminated by residual behavior;
- data cannot be reproducibly accessed or aligned;
- required baselines cannot be computed;
- heldout data is leaked;
- code/evaluator cannot be replayed;
- agent changes scope, metrics, thresholds, stations, or claim tiers without approval;
- cost/time/token budget is exceeded;
- results remain AMBIGUOUS beyond the declared iteration limit;
- a correction or operational claim is introduced in v0.

## Revision policy

This file changes only for:

1. Clarification of ambiguous language.
2. Correction of unsafe or contradictory governance.
3. Human-approved scope amendment.
4. Addition of a future branch after v0.
5. A result-driven lesson that affects future governance but does not rewrite prior claims.

All changes must be logged in `CHANGELOG.md` and `DECISIONS.md`.
