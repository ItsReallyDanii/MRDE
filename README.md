# Microclimate Residual Discovery Engine (MRDE)

**Status:** Governance-first research-system scaffold, packaged for Antigravity-assisted work.  
**Source:** Refactored from `archive/MRDE_CONTROL_PACKET_CANONICAL_v1.1_ALL_IN_ONE.md`.  
**Package generated:** 2026-04-28T04:39:22Z UTC.  
**Revision pass:** 2026-04-28T05:18:00Z UTC — second-pass audit cleanup applied; Stage 0 `PASSED`, Stage 1 `IN_PROGRESS`.

## One-sentence identity

MRDE is a public-data-only, validation-first research framework that detects, tests, and conservatively tiers terrain- and context-conditioned patterns in weather forecast-observation mismatches, starting with 2-meter temperature residuals joined to terrain and land-cover metadata, without making operational forecast-improvement or safety-critical claims.

## What this package is

This package is a **control + execution scaffold** for building MRDE in an agentic IDE without losing the scientific boundaries.

It includes:

- stable project-control Markdown files;
- Antigravity-oriented `AGENTS.md`, `GEMINI.md`, rules, skills, workflows, and knowledge files;
- Stage 0–1 implementation planning artifacts;
- experiment templates;
- append-only log and JSON schema templates;
- package review/check artifacts;
- archived review prompt and original all-in-one packet.

## What this package is not

This package is not:

- a working weather model;
- a forecast-correction product;
- an operational alerting system;
- a claim that MRDE improves forecasts;
- implementation code for HRRR/ASOS ingestion;
- a completed experiment.

## Authority order

`README.md` hosts this authority order for reference. It is **not itself a governance document** and does not override the ordered files below.

If files conflict, use this order:

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
11. Current user instruction, **only if it does not conflict with items 1–10**

## Current allowed work

Allowed now:

- place this package in a repo;
- review and tighten docs;
- create or revise the pre-run experiment plan;
- validate file consistency;
- prepare schemas and templates.

Blocked until a completed, human-approved, append-only-logged pre-run experiment plan exists:

- data ingestion;
- residual inspection;
- station swapping after inspection;
- candidate discovery from residuals;
- validation claims;
- public claims.

## Folder map

```text
.
├─ README.md
├─ AGENTS.md
├─ GEMINI.md
├─ 00_PROJECT_IDENTITY_AND_GLOSSARY.md
├─ 01_MASTER_COMPLETION_CONTRACT.md
├─ 02_STAGE_GATE_PLAN.md
├─ 03_DISCOVERY_WITHIN_DISCOVERY.md
├─ 04_SCOPE_LOCK_AND_V0_DEFINITION.md
├─ 05_DATA_ENGINEERING_AND_PROVENANCE.md
├─ 06_EVALUATION_CLAIMS_AND_ASSUMPTIONS.md
├─ 07_SYSTEM_BOUNDARIES_AND_GOVERNANCE.md
├─ 08_APPEND_ONLY_LOG_SCHEMA.md
├─ 09_IMPLEMENTATION_ROADMAP_AND_V0_SUCCESS.md
├─ 10_PUBLIC_LANGUAGE_RULES.md
├─ APPENDIX_PRIOR_ART.md
├─ APPENDIX_FUTURE_BRANCHES.md
├─ CHANGELOG.md
├─ DECISIONS.md
├─ ONE_PASS_CHECK.md
├─ PACKAGE_MANIFEST.md
├─ .agent/
│  ├─ rules/
│  ├─ skills/
│  ├─ workflows/
│  └─ knowledge/
├─ plans/
├─ experiments/
├─ logs/
├─ schemas/
└─ archive/
   ├─ MRDE_CONTROL_PACKET_CANONICAL_v1.1_ALL_IN_ONE.md
   └─ CLAUDE_REVIEW_PROMPT.md
```
