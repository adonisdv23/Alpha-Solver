# Evidence Requirements

## Current evidence limit

The current accepted evidence is limited to Level 2 local operator usability evidence and Level 3 artifact-complete, non-promotional local orchestration evidence.

## Requirements for future levels

Future packets must preserve the following requirements:

- They must state whether they are design-only or execution lanes.
- They must identify the source evidence reviewed before any new claim boundary is defined.
- They must state explicit non-actions.
- They must prevent Level 2 and Level 3 evidence from being promoted into broader readiness evidence.
- They must define pass, fail, stop, and fallback conditions before execution work begins.
- They must record checks run and whether any check was not run due to environment limits.
- They must avoid claiming production readiness, MVP readiness, benchmark evidence, local model quality evidence, provider-orchestration evidence, Alpha superiority, billing evidence, dashboard readiness, `/v1/solve` readiness, broad runtime readiness, or evidence-model promotion unless a later authorized lane produces bounded evidence for that exact claim.

## Execution separation

Design packets do not create execution evidence. Benchmark runs, local inference runs, hosted provider calls, `/v1/solve` calls, dashboard exposure, billing work, and provider fallback implementation require separate explicit authorization.
