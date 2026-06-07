# Rubric and Scoring

## Future scoring boundary

A future frozen packet may define rubric dimensions and score fields, but scoring may occur only in a later approved execution/review lane. This design packet does not score any run.

## Candidate rubric dimensions

A future rubric may score or classify:

- provenance completeness;
- exact invocation capture;
- parseable normalized JSON availability;
- terminal status validity;
- safety flag presence and reviewability;
- evidence boundary preservation;
- redaction compliance;
- local-only/no-fallback invariant preservation;
- malformed artifact handling;
- operator/environment note completeness.

## Scoring exclusions

The rubric must not score or claim:

- production readiness;
- MVP readiness;
- benchmark performance;
- local model quality;
- provider-orchestration quality;
- Alpha superiority;
- billing correctness;
- dashboard readiness;
- `/v1/solve` readiness;
- broad runtime readiness;
- evidence-model promotion.

## Score status boundary

Any future score must remain packet-local and evidence-bounded. A passing future packet would not, by itself, authorize production, hosted providers, dashboards, `/v1/solve`, billing work, broad runtime deployment, benchmark claims, or evidence promotion.
