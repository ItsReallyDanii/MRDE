# AGENTS.md — MRDE Shared Agent Rules

## Project Identity
MRDE is a public-data-only, validation-first research framework for detecting, testing, and conservatively tiering terrain/context-conditioned forecast-observation mismatch patterns. MRDE is a residual discovery / research-control repository, not a weather model.

## Authority Order
`README.md` hosts the full authority order for human reference. If instructions conflict, obey this order:
1. `01_MASTER_COMPLETION_CONTRACT.md`
2. `00_PROJECT_IDENTITY_AND_GLOSSARY.md`
3. `06_EVALUATION_CLAIMS_AND_ASSUMPTIONS.md`
4. `07_SYSTEM_BOUNDARIES_AND_GOVERNANCE.md`
5. `04_SCOPE_LOCK_AND_V0_DEFINITION.md`
6. `05_DATA_ENGINEERING_AND_PROVENANCE.md`
7. `02_STAGE_GATE_PLAN.md`
8. `docs/agentic_execution/MRDE_AGENT_BOUNDARIES.md`
9. Agent rules (e.g., this file, `docs/agentic_execution/JULES_USAGE_POLICY.md`)
10. Current user instructions

## Always-on Agent Rules

- **Residual Preinspection Guard**: No residual analysis or data inspection is allowed before a completed, human-approved, append-only logged pre-run experiment plan exists.
- **Diff-Review Gates**: Unauthorized or out-of-scope file changes (e.g., modifying pipeline code or schemas without explicit instructions) must be flagged before any merge.
- **Claim-Language Guard**: Overclaiming must be downgraded to `AMBIGUOUS` unless strictly supported by pre-registered validation. Do not mark any result as `SUPPORTED`, `VALIDATED`, `PROVEN`, or `DISCOVERED` under any circumstance.
- **Allowed Actions**: Write code, run tests, summarize logs, prepare PRs.
- **Disallowed Actions**: Decide scientific truth, execute claim-tier upgrades, change locked scientific rules, present exploratory patterns as confirmed findings.

## Required Output Behavior
For every material change, report:
- files changed;
- reason for change;
- validation/check performed;
- whether any governance rule was touched;
- whether the next stage is blocked or allowed.
