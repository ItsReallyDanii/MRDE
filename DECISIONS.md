# Decisions

## D001 — Treat current control packet as Part 1, not total project completion

**Date:** 2026-04-28T04:39:22Z UTC  
**Decision:** The original MRDE governance/control packet is considered complete enough for its own scope, but not equivalent to full MRDE project completion.  
**Reason:** The full project requires stage gates, deterministic data pipeline, residual computation, validation, claim review, and final artifact.  
**Impact:** Added `01_MASTER_COMPLETION_CONTRACT.md` and `02_STAGE_GATE_PLAN.md`.

## D002 — Use stable control docs plus mutable experiment docs

**Date:** 2026-04-28T04:39:22Z UTC  
**Decision:** Stable docs define allowed behavior; experiment docs define actual run choices and results.  
**Reason:** Prevents overfitting to unknown results while avoiding vague under-specified instructions.  
**Impact:** Added `experiments/EXP001/` templates and append-only log schema.

## D003 — Use Antigravity as controlled executor, not autonomous scientist

**Date:** 2026-04-28T04:39:22Z UTC  
**Decision:** Antigravity may create/review docs, templates, schemas, and later deterministic code under approved stage gates. It may not upgrade claims, alter locked experiment rules, or make correction claims.  
**Reason:** Aligns agent behavior with MRDE's governance principle: LLM proposes, evaluator scores, human promotes.

## D004 — EXP001 Oregon five-station multi-terrain transect selected as MRDE v0 pilot

**Date:** 2026-04-28T05:44:17Z UTC
**Decision:** EXP001 uses five Oregon ASOS/METAR-network stations (AST, SLE, MFR, SXT, RDM) covering coastal, Willamette Valley, interior southern valley, mountain/pass, and high-desert terrain classes over a locked 90-day window (2024-06-01 through 2024-08-30, end-exclusive) with HRRR forecasts at 1h/3h/6h/12h lead times.
**Reason:** Stations selected by metadata-only blind filter spanning four terrain/context classes across Oregon; no residuals, forecast errors, or mismatch behavior inspected. Satisfies Stage 1 exit criteria per `02_STAGE_GATE_PLAN.md` and `04_SCOPE_LOCK_AND_V0_DEFINITION.md`.
**Impact:** `experiments/EXP001/PRE_RUN_PLAN.md` filed and logged; Stage 1 marked `PASSED`; Stage 2 unblocked.
