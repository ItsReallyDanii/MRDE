# 02 — Stage Gate Plan

## Purpose

This file turns MRDE from a loose idea into a bounded stage-gated project. It prevents endless version drift by defining what each stage is allowed to do, what it must produce, and when it stops.

## Stage status values

Use exactly one status per stage:

- `NOT_STARTED`
- `IN_PROGRESS`
- `PASSED`
- `FAILED`
- `BLOCKED`
- `SUPERSEDED`


## Current stage status

| Stage | Status | Meaning |
|---|---|---|
| Stage 0 — Governance placement | `PASSED` | Control files, agent scaffold, templates, schemas, and baseline log entry exist; no residuals have been inspected. |
| Stage 1 — Pre-run experiment plan | `PASSED` | `experiments/EXP001/PRE_RUN_PLAN.md` filled, human-approved, and logged as a valid `pre_run_experiment_plan` entry at 2026-04-28T05:44:17Z. |
| Stage 2 — Deterministic data pipeline | `PASSED` | Stage 2 complete. Limitations: NLCD deferred; SXT flagged. |
| Stage 3 — Residual table and baselines | `NOT_STARTED` | Blocked until Stage 2 passes. |
| Stage 4 — Candidate pattern analysis | `NOT_STARTED` | Blocked until Stage 3 passes. |
| Stage 5 — Validation | `NOT_STARTED` | Blocked until Stage 4 passes. |
| Stage 6 — Human claim review | `NOT_STARTED` | Blocked until Stage 5 produces a reviewable claim-tier recommendation. |
| Stage 7 — Final research artifact | `NOT_STARTED` | Blocked until Stage 6 is complete. |

## Stage 0 — Governance placement

**Goal:** Place the control packet and agent scaffold into a repository.

**Allowed:** doc organization, consistency review, schema/template creation.  
**Forbidden:** data ingestion, residual inspection, claim-making.

**Exit criteria:**

- root control files exist;
- `AGENTS.md` and `GEMINI.md` exist;
- `.agent/rules`, `.agent/skills`, `.agent/workflows`, and `.agent/knowledge` exist;
- `CHANGELOG.md` and `DECISIONS.md` exist;
- no code has inspected forecast/observation residuals.

## Stage 1 — Pre-run experiment plan

**Goal:** Lock the first experiment before seeing residuals.

**Exit criteria:**

- geography selected;
- 3–5 stations selected by blind metadata-only criteria;
- 90-day window selected;
- forecast and observation sources locked;
- lead times locked;
- temporal/spatial alignment locked;
- QC policy locked;
- baselines, metrics, thresholds, allowed metadata groupings, and sensitivity checks locked;
- human approval logged.

## Stage 2 — Deterministic data pipeline

**Goal:** Reproducibly ingest public forecast, observation, terrain, and land-cover data.

**Exit criteria:**

- every source has access date and provenance;
- local files have hashes or snapshot identifiers where feasible;
- station metadata is frozen;
- data ingestion can be replayed.

## Stage 3 — Residual table and baselines

**Goal:** Compute forecast-observation mismatches and required baselines.

**Exit criteria:**

- residual table exists;
- raw forecast, persistence, climatology if available, station/lead-time bias, and metadata-agnostic baselines are computed where applicable;
- metrics are deterministic and replayable.

## Stage 4 — Candidate pattern analysis

**Goal:** Generate and log candidate hypotheses without moving the goalposts.

**Exit criteria:**

- every candidate has an ID;
- rejected/failed hypotheses are preserved;
- post-hoc findings are marked SPECULATIVE;
- no agent changes locked experiment rules.

## Stage 5 — Validation

**Goal:** Test candidate patterns against frozen baselines, thresholds, holdouts, and sensitivity checks.

**Exit criteria:**

- validation results exist;
- multiple-comparison correction is applied if required;
- proxy-risk assessment is complete;
- strongest-baseline requirement is checked;
- claim-tier recommendation is made but not self-approved by the agent.

## Stage 6 — Human claim review

**Goal:** Approve, downgrade, or reject claim tier.

**Exit criteria:**

- human review entry exists;
- decision is logged;
- limitations are recorded;
- public wording is checked against `10_PUBLIC_LANGUAGE_RULES.md`.

## Stage 7 — Final research artifact

**Goal:** Produce a research-grade repo/report.

**Exit criteria:**

- final report includes methods, provenance, results, failures, limits, and non-claims;
- reproducibility instructions exist;
- no operational or correction claims appear unless a separate future branch allows them.
