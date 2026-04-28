---
name: mrde-doc-change-control
description: Use when creating, editing, renaming, deprecating, or reorganizing MRDE Markdown/control files.
---

# MRDE Doc Change Control

## Purpose

Use this skill to make document changes without silently changing MRDE scope, authority, claim rules, or experiment history.

## Required context files

Read in this order:

1. `README.md`
2. `01_MASTER_COMPLETION_CONTRACT.md`
3. `02_STAGE_GATE_PLAN.md`
4. `CHANGELOG.md`
5. `DECISIONS.md`
6. File(s) being changed

## Procedure

1. Identify each file to create, edit, move, rename, deprecate, or delete.
2. Classify the reason for the change: clarification, correction, scope amendment, stage transition, result integration, deprecation, or packaging cleanup.
3. Check whether the change touches governance authority, claim tiers, agent boundaries, data rules, validation rules, or public-language rules.
4. If the change touches governance or scope, require an entry in both `CHANGELOG.md` and `DECISIONS.md` unless it is a pure packaging cleanup.
5. If a file is moved or renamed, update `README.md` folder map and `PACKAGE_MANIFEST.md`.
6. If a file is deprecated, do not delete it silently. Move it to `archive/` or mark it as superseded with reason.
7. Return exact changed paths and whether future results are affected.

## Output format

Return:

- `verdict`: ALLOWED / BLOCKED / NEEDS_HUMAN_APPROVAL
- `change_type`: clarification / correction / scope_amendment / stage_transition / result_integration / deprecation / packaging_cleanup
- `files_changed`: list
- `changelog_required`: yes/no
- `decisions_entry_required`: yes/no
- `authority_order_changed`: yes/no
- `result_claims_affected`: yes/no

## Hard stops

Stop if the change would:

- erase or hide failed/ambiguous/rejected results;
- silently alter the meaning of prior experiment results;
- relax claim rules after seeing results;
- change locked experiment definitions after data inspection;
- delete an authority document without a superseding path and decision log.
