---
name: mrde-claim-tier-auditor
description: Use when reviewing language or results for SPECULATIVE, AMBIGUOUS, SUPPORTED_PATTERN, FAILED, or forbidden correction claims.
---

# MRDE Claim Tier Auditor

## Purpose

Use this skill to check whether a proposed claim, README paragraph, report section, validation summary, or public-facing statement matches MRDE claim-tier rules.

## Required context files

Read in this order:

1. `06_EVALUATION_CLAIMS_AND_ASSUMPTIONS.md`
2. `10_PUBLIC_LANGUAGE_RULES.md`
3. `01_MASTER_COMPLETION_CONTRACT.md`
4. Relevant `experiments/EXP001/VALIDATION_REPORT.md`
5. Relevant `experiments/EXP001/CLAIM_REVIEW.md`
6. `schemas/claim_review.schema.json`

## Allowed claim tiers

Allowed v0 tiers:

- `SPECULATIVE`
- `AMBIGUOUS`
- `SUPPORTED_PATTERN`
- `FAILED`

Forbidden in v0:

- `SUPPORTED_CORRECTION`
- forecast-improvement claims
- operational/safety-critical claims

## Forbidden-language scan

Scan proposed language for phrases or meanings equivalent to:

- beats NOAA
- better than official forecasts
- predicts weather better
- fixes weather forecasting
- hidden weather law
- AI discovered weather truth
- operational alert
- safety-critical prediction
- forecast correction product
- superior weather model

If any forbidden phrase or equivalent meaning appears, output BLOCKED with the specific phrase or sentence flagged.

## Procedure

1. Identify the proposed claim text and requested tier.
2. Confirm the requested tier exists in the allowed v0 tier enum.
3. Check whether the evidence source is exploratory, validation, human review, or public language.
4. If requested tier is `SUPPORTED_PATTERN`, verify the checklist in `06_EVALUATION_CLAIMS_AND_ASSUMPTIONS.md` is satisfied by actual validation outputs and human review.
5. If evidence is exploratory or post-hoc, restrict tier to `SPECULATIVE` or lower.
6. If validation is incomplete, unresolved, or proxy-risk remains material, restrict tier to `AMBIGUOUS` or `FAILED` as applicable.
7. Run forbidden-language scan against `10_PUBLIC_LANGUAGE_RULES.md`.
8. Return a safe replacement wording if the original is blocked.

## Output format

Return:

- `verdict`: ALLOWED / BLOCKED / NEEDS_HUMAN_APPROVAL
- `requested_tier`: string
- `allowed_tier`: string
- `forbidden_phrases_found`: list
- `evidence_gap`: list
- `safe_rewrite`: optional
- `human_review_required`: yes/no

## Hard stops

Stop if the claim:

- says or implies forecast improvement in v0;
- uses operational/safety-critical language;
- calls a post-hoc pattern confirmatory;
- claims causal explanation without mechanistic evidence;
- requests `SUPPORTED_PATTERN` without all required validation and human review.
