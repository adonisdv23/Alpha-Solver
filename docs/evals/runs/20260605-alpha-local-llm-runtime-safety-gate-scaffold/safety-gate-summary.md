# Safety-Gate Summary

This is a scaffold only. Local LLM runtime integration is not implemented here.

Any future local LLM runtime integration implementation must satisfy the safety gates below before it can be described as runtime-ready.

## Required gates

1. Local LLM runtime use must remain default-off unless explicitly configured by the operator.
2. Local LLM mode must require a localhost or loopback endpoint only.
3. Local LLM mode must require no provider keys.
4. Hosted provider fallback is prohibited unless separately authorized by a later lane.
5. Runtime calls must use a finite timeout.
6. Runtime handling must fail closed for endpoint, connection, timeout, response, and echo failures.
7. Runtime smoke must run before any runtime-readiness claim.
8. `behavior_evidence=false` must remain preserved until a later lane explicitly changes the evidence model.
9. `/v1/solve` must not be exposed to local LLM mode until explicitly authorized.
10. Dashboard preview must not be exposed to local LLM mode until explicitly authorized.
11. Observability must distinguish local LLM from hosted providers.
12. Raw artifacts must be preserved for runtime smoke.

## Blocked by this scaffold

This scaffold does not permit source changes, test changes, runtime changes, provider changes, `/v1/solve` changes, dashboard changes, local model calls, hosted provider calls, network calls, provider keys, or any readiness, validation, superiority, benchmark, production, MVP, runtime, billing, or provider-orchestration claim.
