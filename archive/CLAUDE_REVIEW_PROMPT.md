# Claude/Sonnet Review Prompt — MRDE Antigravity Control Package

You are reviewing an MRDE repository scaffold intended for use in Google Antigravity.

Context:
- MRDE = Microclimate Residual Discovery Engine.
- Goal: build an AI-assisted public-data research system that discovers and validates terrain/context-conditioned weather forecast-observation mismatch patterns.
- v0 scope: 2-meter temperature residuals only, likely HRRR forecasts vs ASOS/METAR observations, joined with terrain/land-cover metadata.
- Critical boundary: MRDE v0 is not a weather model, not a correction product, not a safety-critical system, and must not claim forecast improvement.
- Existing governance packet was treated as Part 1 only. This package adds a full project completion contract, stage gates, Antigravity rules/skills/workflows, templates, logs, and schemas.

Your job:
Perform a skeptical one-pass review of the package.

Please check:

1. Folder placement
   - Are `AGENTS.md`, `GEMINI.md`, `.agent/rules`, `.agent/skills`, `.agent/workflows`, and `.agent/knowledge` placed sensibly for Antigravity?
   - Are any names/paths likely wrong for current Antigravity usage?

2. Governance correctness
   - Does `01_MASTER_COMPLETION_CONTRACT.md` correctly define the overall project finish line without overfitting unknown results?
   - Does it clearly distinguish Part 1 governance completion from full MRDE completion?
   - Does it prevent endless v0.1/v0.2 drift?

3. Scientific safety
   - Does the package prevent station cherry-picking, post-hoc thresholds, overclaiming, and correction claims?
   - Does it preserve AMBIGUOUS and FAILED outcomes as valid project outputs?
   - Does it avoid “beats NOAA / better than weather models” framing?

4. Agent-safety / Antigravity fit
   - Are the skills too broad or appropriately scoped?
   - Are the workflows stage-gated enough?
   - Are always-on rules strict enough to stop agent overreach?
   - Should any files be merged, split, renamed, moved, or deleted?

5. Missing pieces
   - What files are missing before Stage 0 is complete?
   - What files are missing before Stage 1 can begin?
   - What should explicitly NOT be created yet?

6. Required revisions
   - Give a PASS / PASS WITH MINOR REVISIONS / FAIL verdict.
   - List only concrete changes, grouped by file path.
   - Do not rewrite the whole package unless necessary.
   - Be blunt about any contradiction, scope leak, or overfit/underfit issue.

Important constraints:
- Do not suggest coding the data pipeline yet.
- Do not suggest choosing stations from residual behavior.
- Do not suggest correction claims in v0.
- Treat the correct operating principle as: LLM proposes, evaluator scores, human promotes.
