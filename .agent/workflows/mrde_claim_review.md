---
description: Review validation outputs and prepare a human-readable claim-tier review without upgrading claims autonomously.
---

# MRDE Claim Review Workflow

Use only after validation outputs exist. This workflow does not promote claims by itself; it prepares the evidence packet for human review.

1. Read `06_EVALUATION_CLAIMS_AND_ASSUMPTIONS.md`, `10_PUBLIC_LANGUAGE_RULES.md`, `experiments/EXP001/VALIDATION_REPORT.md`, and `experiments/EXP001/CLAIM_REVIEW.md` if present.
2. Identify each candidate hypothesis and requested/recommended claim tier.
3. Run through the SUPPORTED_PATTERN checklist in `06_EVALUATION_CLAIMS_AND_ASSUMPTIONS.md` item by item. Mark each as `PASS`, `FAIL`, or `UNKNOWN`.
4. Check baseline comparison matrix, strongest baseline result, p-value adjustment, heldout split, sensitivity checks, and proxy-risk status.
5. Run through the public release gate checklist and forbidden-language rules in `10_PUBLIC_LANGUAGE_RULES.md`.
6. If any SUPPORTED_PATTERN requirement is failed or unknown, downgrade the maximum allowed tier to `AMBIGUOUS` or `FAILED` as applicable.
7. If language implies forecast improvement, operational use, causal proof, or “beats NOAA” framing, output BLOCKED and provide safe wording.
8. Prepare a human-review packet:
   - hypothesis ID
   - evidence summary
   - maximum allowed tier
   - failed/unknown requirements
   - safe public wording
   - required human approval entry
9. Do not modify thresholds, baselines, station list, metrics, or validation rules.
