# 07 — System Boundaries and Governance

## Core rule

LLM proposes. Evaluator scores. Human promotes.

## v0 agent status

For MRDE v0, the agentic loop is advisory only.

The agent may suggest features, groupings, and analysis ideas, but may not execute autonomous search, change scope, change data, change metrics, change thresholds, or upgrade claims.

## Agent may do

The agent may propose feature combinations, station groupings, simple residual-pattern hypotheses, stratification ideas, result summaries, failed-path notes, and follow-up tests.

## Agent may not do

The agent may not change held-out split, evaluator metric, data sources, claim tiers, public language, station selection after residual inspection, or governance rules.

The agent may not run reinforcement-learning, AutoML-style, or arbitrary model-family search loops in v0.

## Human gates

Human approval is required for:

- claim-tier upgrade;
- new data source;
- new variable;
- new geographic region;
- station-list change after logging;
- held-out split change;
- validation metric change;
- baseline definition change;
- evaluator change;
- public-facing language;
- causal explanation;
- expansion beyond 2-meter temperature;
- transition from advisory-only agent to bounded proposal mode.

All human approvals must be logged.

## Stop rules

Stop the run or downgrade the claim if:

- no baseline exists;
- no pre-run experiment plan exists;
- data alignment is uncertain;
- residuals are not reproducible;
- held-out data was leaked;
- region/station frame changed after inspection;
- pattern works only on one cherry-picked station/event;
- p-values fail correction after multiple testing;
- observation artifact is plausible and unresolved;
- model/version changes are pooled without stratification;
- code/evaluator cannot be deterministically replayed;
- generated explanation uses causal language without evidence;
- compute/time/token budget is exceeded;
- no improvement or stability after predefined iterations;
- a post-hoc pattern is presented as confirmatory.

A single hypothesis may not undergo more than the `max_ambiguous_iterations` (declared in the pre-run experiment plan) while in AMBIGUOUS status. Any attempt to re-test the same hypothesis after this limit requires a new experiment ID and a new human-gated pre-run plan.

## Runtime limits

| Limit | Value |
|---|---|
| max_candidate_variants_per_session | 25 |
| max_failed_iterations_before_review | 10 |
| max_runtime_per_candidate | 10 minutes |
| absolute_runtime_override | 30 minutes with human approval |
| max_hypothesis_families_per_dataset | must be set in pre-run plan |

Any longer run requires a separate human-gated experiment entry.

## Correction-claim restriction

MRDE v0 does not make forecast-improvement or correction claims.

If a candidate rule appears to reduce forecast error, the result may be logged as exploratory or AMBIGUOUS, but no SUPPORTED_CORRECTION claim may be made in v0.

## Conflict resolution

If an agent recommendation conflicts with any governance file, the governance file wins.

If governance files conflict, apply the authority order in `README.md`.

---
