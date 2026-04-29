# Smart Tool Contracts

This document outlines proposed programmatic wrappers ("Smart Tools") designed to enforce MRDE governance boundaries automatically during agentic execution. These are theoretical definitions that agents must respect if/when implemented.

## 1. MRDE Test Runner
**Purpose:** Ensure all tests pass before any pipeline code or documentation updates are merged.
**Contract:**
- Must execute the full suite of unit and integration tests.
- Must verify that test logs are properly formatted.
- Agents may run this tool but cannot bypass its output or suppress failures.

## 2. Schema Contract Validator
**Purpose:** Prevent arbitrary or unauthorized changes to data and log schemas.
**Contract:**
- Must diff proposed schema changes against `schemas/` definitions.
- Must reject changes unless the active task explicitly permits schema modification.
- Agents cannot modify data files or bypass schema rules.

## 3. Residual Preinspection Guard
**Purpose:** Prevent p-hacking, overfitting, and unauthorized data exploration.
**Contract:**
- Must block any read access or statistical summary of residual data until a valid `pre_run_plan` exists in the append-only log.
- Returns an explicit access denial if the log entry is missing.

## 4. Diff Scope Gate
**Purpose:** Limit the agent's file system impact to exactly what was requested.
**Contract:**
- Reviews the Git diff of the agent's work.
- Flags unauthorized file changes (e.g., changes to pipeline code when the task was a doc-only patch) before allowing a merge.
- Forces the agent to revert out-of-scope modifications.

## 5. Log Summarizer
**Purpose:** Provide structured, objective summaries of experiment or test logs without injecting narrative interpretation.
**Contract:**
- Consumes raw logs and produces deterministic summaries (e.g., pass/fail counts, explicit error messages).
- Must strip out any language that implies a discovery or proven result.

## 6. Claim Language Gate
**Purpose:** Enforce the MRDE strict public language rules.
**Contract:**
- Scans all agent-generated text (PR descriptions, documentation, log summaries) for prohibited words (`SUPPORTED`, `VALIDATED`, `PROVEN`, `DISCOVERED`).
- Automatically downgrades offending terms to `AMBIGUOUS` or requires the agent to rewrite the text.
- Agents must not independently mark any result as `SUPPORTED`, `VALIDATED`, `PROVEN`, or `DISCOVERED`. Claim-tier upgrades require explicit human approval and the applicable pre-registered validation evidence.
- Overclaiming is strictly rejected.

## 7. Claim Terms Policy Exception
Policy/control documents may mention restricted claim terms when defining governance rules. Agent-generated result summaries, PR descriptions, reports, and scientific interpretations must not use those terms unless explicitly authorized.
