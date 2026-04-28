# One-Pass Check

> **Single-use review artifact:** This file records the package review state for the v2/v3 scaffold pass. It is not a live governance document, does not override the authority order, and should not be treated as current project law after later revision passes. Live project status belongs in `02_STAGE_GATE_PLAN.md`, `CHANGELOG.md`, `DECISIONS.md`, and `logs/append_only_log.jsonl`.


## Passed by construction

- Original all-in-one control packet is archived.
- Stable project docs are separated from mutable experiment docs.
- Antigravity-facing files exist separately from scientific control docs.
- `01_MASTER_COMPLETION_CONTRACT.md` fills the whole-project finish-line gap.
- `02_STAGE_GATE_PLAN.md` defines stage movement and blockers.
- Experiment templates do not contain fake results.
- Append-only log file exists and now contains a Stage 0 changelog baseline entry.
- JSON schemas exist for logs, pre-run plan, and claim review.
- Skills are scoped to review/planning/validation support, not autonomous discovery.
- Skills now have differentiated task-specific procedures.
- Workflows now have differentiated stage-gate, experiment-run, and claim-review procedures.
- Correction claims remain blocked in v0.
- `CLAUDE_REVIEW_PROMPT.md` is archived, not root-authority-adjacent.
- `schemas/claim_review.schema.json` no longer contains undocumented `NO_CLAIM`.

## Needs human or IDE validation

- Confirm Antigravity loads `.agent/skills/*/SKILL.md` as expected.
- Confirm workflow filenames and frontmatter match current Antigravity requirements.
- Confirm whether `AGENTS.md`, `GEMINI.md`, or both should be authoritative in your installed Antigravity version.
- Confirm whether `.agent/rules/` is loaded automatically or should be referenced from `AGENTS.md`/`GEMINI.md`.
- Confirm whether any official Antigravity naming convention requires adjustment.
- Confirm Claude/Sonnet agrees that the specialized skills/workflows are now operational rather than decorative.

## Do not do yet

- Do not write data-ingestion code.
- Do not inspect HRRR/ASOS residuals.
- Do not select stations based on observed mismatch behavior.
- Do not create a correction-claim branch.
