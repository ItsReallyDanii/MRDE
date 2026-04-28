# Package Manifest

## Created content

- Root control docs: `README.md`, `00_*.md` through `10_*.md`
- Shared agent rules: `AGENTS.md`
- Antigravity-specific rules: `GEMINI.md`
- Agent rules: `.agent/rules/MRDE_ALWAYS_ON_RULES.md`
- Agent skills: `.agent/skills/*/SKILL.md`
- Agent workflows: `.agent/workflows/*.md`
- Agent knowledge seed: `.agent/knowledge/MRDE_CONTEXT.md`
- Plans: `plans/*`
- Experiment templates: `experiments/EXP001/*`
- Logs: `logs/*`
- Schemas: `schemas/*`
- Review/check artifacts: `ONE_PASS_CHECK.md` (single-use review artifact, not live governance), `PACKAGE_MANIFEST.md`
- Archive:
  - `archive/MRDE_CONTROL_PACKET_CANONICAL_v1.1_ALL_IN_ONE.md`
  - `archive/CLAUDE_REVIEW_PROMPT.md`

## Revision notes

Post-Claude minor-revision cleanup completed at `2026-04-28T04:51:26Z`.

Second-pass audit cleanup completed at `2026-04-28T05:18:00Z`:

- removed the `residual_preinspection_attestation: false` template trap and replaced it with a fill-only-after-confirmation placeholder;
- added temporal split prohibition for time-correlated meteorological validation;
- hardened `schemas/pre_run_plan.schema.json` to require temporal split, sensitivity check, and proxy-risk fields;
- added ASOS airport siting bias, grid-to-point elevation mismatch, and diurnal/seasonal stratification guidance;
- added current stage status table to `02_STAGE_GATE_PLAN.md`;
- appended a canonical Stage 0 `PASSED` correction entry to `logs/append_only_log.jsonl`;
- clarified `mrde-prerun-plan-writer` trigger description;
- updated `MRDE_CONTEXT.md` to reflect Stage 0 complete / Stage 1 in progress;
- labeled `ONE_PASS_CHECK.md` as a single-use review artifact.
- updated `README.md` status wording for the second-pass cleanup.

Original post-Claude cleanup completed at `2026-04-28T04:51:26Z`:

- moved `CLAUDE_REVIEW_PROMPT.md` out of root into `archive/`;
- aligned `AGENTS.md` authority order with `README.md`;
- clarified `README.md` as authority-order host, not governance authority;
- specialized all skill procedures;
- specialized all workflow procedures;
- removed undocumented `NO_CLAIM` enum from `schemas/claim_review.schema.json`;
- seeded `logs/append_only_log.jsonl` with a Stage 0 changelog entry.

## Known limitations

- This package has not been validated inside the live Antigravity IDE.
- Official Antigravity behavior may require path or filename adjustments.
- No data pipeline code is included because the pre-run experiment plan is not yet approved.
- No scientific result claims are included because no MRDE experiment has been run.
