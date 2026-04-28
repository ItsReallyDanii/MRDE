# AGENTS.md — MRDE Shared Agent Rules

## Project identity

MRDE is a public-data-only, validation-first research framework for detecting, testing, and conservatively tiering terrain/context-conditioned forecast-observation mismatch patterns.

## Authority order

`README.md` hosts the full authority order for human reference. If instructions conflict, obey this order:

1. `01_MASTER_COMPLETION_CONTRACT.md`
2. `00_PROJECT_IDENTITY_AND_GLOSSARY.md`
3. `06_EVALUATION_CLAIMS_AND_ASSUMPTIONS.md`
4. `07_SYSTEM_BOUNDARIES_AND_GOVERNANCE.md`
5. `04_SCOPE_LOCK_AND_V0_DEFINITION.md`
6. `05_DATA_ENGINEERING_AND_PROVENANCE.md`
7. `02_STAGE_GATE_PLAN.md`
8. Antigravity agent files: `AGENTS.md`, `GEMINI.md`, `.agent/**`
9. Experiment files under `experiments/**`
10. Appendices and future-branch notes
11. Current user instruction, only if it does not violate items 1–10.

## Always-on rules

- Do not inspect residual data unless a pre-run experiment plan exists.
- Do not change stations, metrics, thresholds, baselines, or scope after data inspection.
- Do not claim forecast improvement in MRDE v0.
- Do not create operational or safety-critical weather claims.
- Do not delete failed, rejected, ambiguous, or contradictory results.
- Do not silently overwrite experiment logs; append correction entries instead.
- Do not upgrade claim tiers without human review.
- Treat a clean FAILED result as a valid project output.
- Prefer deterministic scripts, schemas, logs, and reproducible outputs over narrative explanation.

## Agent role

The agent may propose, draft, check, scaffold, and summarize. The agent may not promote claims, change locked scientific rules, or present exploratory patterns as confirmed findings.

## Required output behavior

For every material change, report:

- files changed;
- reason for change;
- validation/check performed;
- whether any governance rule was touched;
- whether the next stage is blocked or allowed.
