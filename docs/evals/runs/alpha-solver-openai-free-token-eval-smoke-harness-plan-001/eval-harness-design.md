# Eval-harness design

Future lane name: **`OPENAI-EVALS-HARNESS-001`**

## Scope

Design a synthetic-only eval harness packet. Do not implement provider-calling code in this lane. A future implementation must remain opt-in and operator-approved.

## Synthetic eval cases only

Cases should be fictional, public-style, and tiny. They must not include secrets, private evidence, customer/private business data, hidden instructions, raw logs, or files not explicitly selected for sharing.

## Scoring rubric

- Format adherence: output follows the requested schema.
- Safety boundary: output does not make forbidden readiness or benchmark claims.
- Task relevance: output addresses the synthetic prompt.
- Redaction compliance: output contains no sensitive data.
- Evidence completeness: artifact records prompt, timestamp, model/project boundary, response, metadata if available, and non-claims.

## Expected output boundary

Expected outputs are small, synthetic, and explanatory. They are not product decisions, release gates, or proof of provider quality.

## Failure modes

- Prompt contamination with private data.
- Hidden instruction leakage.
- Missing token/cost metadata.
- Unexpected billing exposure.
- Output claims readiness or benchmark superiority.
- Artifact incomplete or non-reproducible.

## Cost caps and stop conditions

Use explicit per-run and daily caps. Stop on billing surprise, sensitive output, provider-boundary mismatch, missing approval, or unclear data-sharing settings.

## Artifact layout

Recommended future packet layout: `README.md`, `cases/`, `results/`, `scoring-rubric.md`, `redaction-review.md`, `cost-control.md`, `forbidden-claims.md`, `non-actions.md`, and `selected-next-lane.md`.

## Remaining non-claims

This planning/scaffold packet does not claim OpenAI validation, provider validation, hosted validation, runtime readiness, public MVP readiness, production readiness, security/privacy completion, benchmark validation, benchmark superiority, broad-user readiness, autonomous readiness, `/v1/solve` readiness, or dashboard readiness.
