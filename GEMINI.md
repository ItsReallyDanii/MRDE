# GEMINI.md — Antigravity-Specific MRDE Instructions

## Purpose

This file is for Antigravity-specific behavior. Shared cross-tool rules live in `AGENTS.md`.

## Antigravity operating mode

Use Antigravity as a controlled project executor inside MRDE's scientific contract.

Preferred workflow:

1. Produce or update an implementation plan before changing files.
2. Produce or update a task list.
3. Touch only files allowed by the current stage.
4. Produce a walkthrough/proof artifact after work.
5. Stop if a governance rule blocks the requested action.

## Stage restrictions

Current package stage: **Stage 0 / Stage 1 setup**.

Allowed:

- organize docs;
- create/revise templates;
- write schemas;
- draft pre-run plan skeletons;
- check consistency;
- create safe scaffolding.

Blocked:

- data ingestion;
- residual computation;
- candidate mining from observed residuals;
- station replacement after residual inspection;
- public claims;
- correction-claim code or docs.

## Terminal and file safety

- Do not run destructive commands without explicit human approval.
- Do not delete source control, logs, data, or experiment outputs.
- Do not read secrets, credentials, private unrelated files, or ignored files.
- Do not execute external network calls unless the task explicitly requires it and the plan records the source.

## Required review artifact

After each Antigravity task, create or update a walkthrough artifact using `plans/WALKTHROUGH_TEMPLATE.md`.
