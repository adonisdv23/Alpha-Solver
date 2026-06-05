# LOCAL-LLM-RUNTIME-INTEGRATION-001 · Local LLM Runtime Integration Implementation Contract

## Purpose

This spec is the canonical implementation contract for a future local LLM runtime integration lane. The supporting lane record lives under `docs/evals/runs/20260605-alpha-local-llm-runtime-integration-spec/`.

This spec preserves local LLM as an optional backend path. It does not make local model setup required for existing operation, and it does not authorize implementation in this spec-registration lane.

## Selected backend strategy

Selected backend strategy: `hybrid`.

Hybrid means hosted and local provider modes may exist as separately selected modes. It does not mean automatic fallback, hidden provider orchestration, provider racing, opportunistic routing, or substituting hosted output for local LLM failure.

The future implementation must require explicit provider selection. Silent hosted-provider fallback from local LLM mode is prohibited.

## Local LLM enablement contract

A future implementation must satisfy all of the following:

1. Local LLM mode is optional and default-off.
2. Explicit operator opt-in is required before local LLM mode can be used.
3. Local LLM mode must accept only localhost or loopback endpoints.
4. Local LLM mode must require no provider keys.
5. Local LLM calls must use a finite timeout.
6. Hosted output must not be labeled as local LLM output.
7. Local LLM output must preserve `behavior_evidence=false` unless a later spec explicitly changes the evidence model.

## Endpoint contract

Local LLM mode may use only local machine endpoints. The future implementation must accept only endpoints that parse deterministically as localhost or loopback, such as:

- `localhost`
- `127.0.0.1`
- `::1`

The implementation must reject remote, hosted, LAN, private-network, malformed, ambiguous, unsupported-scheme, missing-host, and userinfo-bearing endpoint values for local LLM mode.

## Fail-closed contract

A future implementation must fail closed for all of the following local LLM mode cases:

- non-local endpoint;
- malformed endpoint;
- connection failure;
- timeout;
- malformed response;
- empty output;
- prompt echo;
- system echo.

Fail-closed means the local LLM path stops with a bounded local failure outcome, no hosted-provider call is made unless a later spec separately authorizes explicit fallback, failed or echoed output is not presented as successful behavior, and `behavior_evidence=false` is preserved.

## Fallback contract

No silent hosted-provider fallback is allowed from local LLM mode.

If a later spec authorizes fallback, that later spec must define operator opt-in, fallback trigger conditions, hosted-provider credential requirements, provenance labels, and tests proving fallback is explicit rather than silent. Until then, local failures must remain visible as local failures.

## Observability and provenance contract

A future implementation must distinguish local LLM output from hosted provider output in observability and provenance. Local records must include enough metadata to identify:

- local provider mode;
- local backend or adapter identifier;
- configured local model identifier;
- localhost or loopback endpoint confirmation without exposing unnecessary raw endpoint detail;
- timeout value used;
- status and deterministic reason label;
- `behavior_evidence=false`.

Hosted output must not be labeled as local LLM output.

## Blocked surfaces for this implementation phase

The following surfaces remain blocked from local LLM mode unless a later spec explicitly authorizes them:

- `/v1/solve`;
- dashboard preview.

This spec does not authorize changes to provider orchestration, billing or hosted-provider credential paths, broad routing, MCP, SAFE-OUT, budget guard, determinism, replay, or SolverEnvelope behavior.

## Future implementation boundary

Future implementation must remain narrow and avoid broad refactors. The expected implementation boundary is limited to:

- `alpha/local_llm/provider_adapter.py` for local endpoint, timeout, transport, parser, fail-closed, and provenance refinements;
- the narrow runtime configuration module or entrypoint code needed for explicit provider selection, if inspection proves it is required;
- the narrow runtime call site needed to invoke the local LLM backend, if inspection proves it is required;
- focused tests for this contract.

## Required future tests

A future implementation must include focused tests proving:

1. local LLM mode is default-off;
2. explicit operator opt-in is required;
3. local LLM mode requires no provider keys;
4. localhost and loopback endpoints are accepted;
5. non-local endpoints fail closed;
6. malformed endpoints fail closed;
7. invalid timeout values fail closed;
8. connection failure fails closed;
9. timeout fails closed;
10. malformed response fails closed;
11. empty output fails closed;
12. prompt echo fails closed;
13. system echo fails closed;
14. hosted-provider fallback does not occur from local LLM mode;
15. observability labels local LLM output separately from hosted provider output;
16. `behavior_evidence=false` is preserved.

## Runtime smoke requirement

Future runtime smoke is required before any runtime-readiness claim. That smoke must preserve artifacts sufficient to confirm explicit local provider selection, localhost or loopback endpoint use, finite timeout, no provider keys, no hosted-provider fallback, status/reason labels, and `behavior_evidence=false` preservation.

## Evidence boundary

This spec is an implementation contract only. It is not implementation, runtime evidence, local model quality evidence, hosted provider evidence, `/v1/solve` readiness, dashboard preview readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, or Alpha superiority evidence.
