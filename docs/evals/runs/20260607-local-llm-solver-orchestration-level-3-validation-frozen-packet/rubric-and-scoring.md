# Rubric and Scoring Boundaries

## Rubric dimensions

A future review may score only these dimensions:

1. provenance completeness;
2. exact invocation capture;
3. parseable normalized JSON;
4. terminal status validity;
5. required safety flag presence;
6. evidence-boundary preservation;
7. redaction compliance;
8. local-only/no-fallback invariant preservation;
9. stop-condition compliance;
10. operator/environment note completeness.

## Allowed scoring values

Each dimension may be marked only as:

- `pass`
- `fail`
- `blocked`
- `not_reviewable`

## Scoring boundaries

Do not score:

- local model quality;
- benchmark performance;
- production readiness;
- MVP readiness;
- provider-orchestration evidence;
- Alpha superiority;
- billing readiness or billing evidence;
- dashboard readiness;
- `/v1/solve` readiness;
- broad runtime readiness;
- evidence-model promotion.

## Review outcome boundary

A future review may conclude only whether artifacts are complete and within the frozen evidence boundary. It may not convert the artifacts into behavior evidence while `behavior_evidence=false` remains required.
