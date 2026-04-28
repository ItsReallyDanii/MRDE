---
description: Run a stage-gate review for MRDE and decide whether the next stage is allowed, blocked, or requires human approval.
---

# MRDE Stage-Gate Workflow

1. Read `README.md`, `01_MASTER_COMPLETION_CONTRACT.md`, and `02_STAGE_GATE_PLAN.md`.
2. Identify the current stage and requested next stage.
3. Check `AGENTS.md`, `GEMINI.md`, and `.agent/rules/MRDE_ALWAYS_ON_RULES.md` for blockers.
4. Check each exit criterion in `02_STAGE_GATE_PLAN.md` for the current stage against files on disk. List each criterion as `MET`, `UNMET`, or `UNKNOWN`.
5. Check whether the requested transition requires human approval under `07_SYSTEM_BOUNDARIES_AND_GOVERNANCE.md`.
6. Do not modify experiment definitions if data inspection has already occurred.
7. Produce a gate report:
   - current stage
   - requested transition
   - gate verdict: ALLOWED / BLOCKED / NEEDS_HUMAN_APPROVAL
   - criterion table: MET / UNMET / UNKNOWN
   - missing files or fields
   - files safe to edit
   - files forbidden to edit
   - required log entry
8. If a gate passes, append or prepare the required log entry. If blocked, record the blocker without working around it.
9. Write or update a walkthrough using `plans/WALKTHROUGH_TEMPLATE.md`.
