# MRDE Agent Boundaries

This document defines the strict authority boundaries among all actors operating within the MRDE framework.

## 1. Human (Lead Researcher / Reviewer)
- **Authority:** Absolute.
- **Responsibilities:**
  - Approve pre-run experiment plans.
  - Approve schema changes.
  - Interpret results and validate final claims.
  - Provide explicit instructions that may override agent defaults (provided they do not violate master scientific rules).
  - Resolve `AMBIGUOUS` states flagged by the Claim Language Gate.

## 2. ChatGPT / Orchestrator
- **Authority:** High-level planning and reasoning, but zero direct execution or file modification without an executor agent.
- **Responsibilities:**
  - Assist the Human in designing experiments.
  - Generate task prompts for Jules based on Human intent.
  - Ensure all task definitions adhere to MRDE governance.

## 3. Jules / Code Agent (The Executor)
- **Authority:** Limited exclusively to execution within requested scope.
- **Responsibilities:**
  - Write, modify, and test pipeline code as directed.
  - Prepare PRs and summarize logs.
  - Format and structure documentation.
- **Strict Boundaries:**
  - Cannot read residual data without a logged pre-run plan.
  - Cannot evaluate scientific truth.
  - Agents must not independently mark any result as `SUPPORTED`, `VALIDATED`, `PROVEN`, or `DISCOVERED`. Claim-tier upgrades require explicit human approval and the applicable pre-registered validation evidence.
  - Cannot modify out-of-scope files (enforced by Diff Scope Gate).

## 4. Repository Docs (The Law)
- **Authority:** Foundational. Overrides all agent behaviors.
- **Responsibilities:**
  - Host the inviolable source of truth for MRDE rules (e.g., `01_MASTER_COMPLETION_CONTRACT.md`, `AGENTS.md`).
  - Provide the structural definition for what constitutes a valid discovery, test, or log.
  - Agents must constantly read and defer to these docs before acting.

## 5. Claim Terms Policy Exception
Policy/control documents may mention restricted claim terms when defining governance rules. Agent-generated result summaries, PR descriptions, reports, and scientific interpretations must not use those terms unless explicitly authorized.
