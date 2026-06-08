# Provider Orchestration Boundary

## In scope for this design packet

This packet defines requirements for future provider orchestration, including:

- provider registry shape and capability metadata;
- provider routing and selection constraints;
- fallback and fail-closed behavior;
- credential, token, secret, and environment boundaries;
- timeout, retry, circuit-breaker, and budget controls;
- provenance, observability, usage, cost, and quota controls;
- provider-backed safety and claim gates;
- implementation-readiness gates and stop conditions.

## Out of scope for this design packet

This packet does not implement provider orchestration. It does not change runtime code, provider adapter behavior, provider routing, provider fallback, hosted fallback, operator CLI behavior, checker scripts, tests, Makefile targets, CI workflows, API routes, dashboard routes, credentials, local model inference, hosted model inference, Ollama behavior, benchmarks, billing, external ledgers, or evidence status.

## Required boundary for future lanes

A future implementation lane must identify the exact provider path being changed, the exact entrypoint being affected, and the exact evidence boundary being preserved. Broad changes to routing, MCP, SAFE-OUT, budget guard, determinism, observability, replay, or SolverEnvelope behavior remain blocked unless explicitly authorized by a later accepted spec or lane.
