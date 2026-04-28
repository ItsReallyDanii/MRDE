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
