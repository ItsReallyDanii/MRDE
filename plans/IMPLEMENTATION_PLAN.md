# Implementation Plan — Stage 0 to Stage 1 Only

## Current implementation boundary

This plan covers governance placement and pre-run planning only. It does not authorize data ingestion, residual computation, or validation code.

## Stage 0 tasks

1. Place control files at repository root.
2. Confirm authority order.
3. Confirm Antigravity files are present.
4. Confirm schemas and templates exist.
5. Run a consistency review.

## Stage 1 tasks

1. Fill `experiments/EXP001/PRE_RUN_PLAN.md`.
2. Select geography and stations by blind metadata-only criteria.
3. Lock time window, lead times, alignment rules, QC policy, baselines, metrics, thresholds, and sensitivity checks.
4. Add human approval entry to `logs/append_only_log.jsonl`.
5. Stop before data ingestion unless Stage 1 passes.

## Explicitly out of scope

- pipeline implementation;
- HRRR download scripts;
- ASOS/METAR parsers;
- residual calculation;
- candidate mining;
- result reporting;
- public claim drafting.
