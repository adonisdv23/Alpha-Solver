# Deferred Work

The following work is deferred until this Level 7 packet is accepted and a later lane explicitly authorizes it:

- provider registry implementation;
- provider capability schema implementation;
- provider router implementation;
- provider selection implementation;
- provider fallback implementation;
- hosted fallback implementation;
- credential and environment configuration changes;
- timeout, retry, and circuit-breaker code changes;
- budget and quota enforcement changes;
- provider provenance and observability implementation;
- provider-backed safety gate implementation;
- `/v1/solve` exposure or modification;
- dashboard route exposure or modification;
- live provider testing;
- local model inference;
- hosted model inference;
- Ollama runs;
- benchmarks and quality scoring;
- billing integration;
- external ledger updates;
- MVP readiness review.

## Why Level 8 remains deferred

Level 8 MVP readiness review remains deferred because MVP readiness cannot be reviewed safely until Level 7 provider orchestration boundaries are accepted. Without accepted provider registry, routing, fail-closed, credential, timeout, retry, cost, quota, provenance, observability, safety, and stop-condition requirements, an MVP review would risk treating unresolved provider orchestration hazards as readiness evidence.
