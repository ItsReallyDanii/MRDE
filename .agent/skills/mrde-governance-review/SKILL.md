---
name: mrde-governance-review
description: Use when checking whether a proposed change, prompt, file edit, implementation plan, or agent action violates MRDE governance, scope, claim tiers, or stage gates.
---

# MRDE Governance Review

## Purpose

Use this skill to audit whether a proposed action is allowed under MRDE governance before any implementation or document change.

## Required context files

Read in this order:

1. `README.md` for the authority-order reference only
2. `01_MASTER_COMPLETION_CONTRACT.md`
3. `00_PROJECT_IDENTITY_AND_GLOSSARY.md`
4. `06_EVALUATION_CLAIMS_AND_ASSUMPTIONS.md`
5. `07_SYSTEM_BOUNDARIES_AND_GOVERNANCE.md`
6. `04_SCOPE_LOCK_AND_V0_DEFINITION.md`
7. `05_DATA_ENGINEERING_AND_PROVENANCE.md`
8. `02_STAGE_GATE_PLAN.md`
9. `AGENTS.md`, `GEMINI.md`, `.agent/rules/MRDE_ALWAYS_ON_RULES.md`

## Procedure

1. Identify the requested action and current stage.
2. Classify the action as one of: documentation, planning, data ingestion, residual inspection, hypothesis generation, validation, claim review, public language, or scope amendment.
3. Check whether the action is allowed in the current stage using `02_STAGE_GATE_PLAN.md` and `09_IMPLEMENTATION_ROADMAP_AND_V0_SUCCESS.md`.
4. Check whether the action violates any hard boundary in `07_SYSTEM_BOUNDARIES_AND_GOVERNANCE.md`.
5. Check whether the action would change station list, metrics, thresholds, baselines, scope, data sources, or claim tiers.
6. If files conflict, apply the authority order from `README.md`.
7. Return the smallest safe recommendation: allow, block, require human approval, or convert to template-only.

## Output format

Return:

- `verdict`: ALLOWED / BLOCKED / NEEDS_HUMAN_APPROVAL / TEMPLATE_ONLY
- `stage`: current stage
- `reason`: concise rule-based reason
- `files_checked`: list
- `conflicts_found`: list
- `risk_flags`: list
- `required_log_entry`: yes/no

## Hard stops

Stop if the request asks to:

- inspect residuals before pre-run plan approval;
- change locked experiment definitions after inspection;
- claim forecast improvement in v0;
- delete or hide failed results;
- upgrade claims without human review;
- bypass the authority order.
