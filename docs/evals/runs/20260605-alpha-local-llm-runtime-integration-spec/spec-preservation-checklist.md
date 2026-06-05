# Spec Preservation Checklist

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-SPEC-001`

## Scope checks

- [x] Docs-only package created under `docs/evals/runs/20260605-alpha-local-llm-runtime-integration-spec/`.
- [x] No source code changes are authorized by this package.
- [x] No test code changes are authorized by this package.
- [x] No runtime implementation is included.
- [x] No provider implementation is included.
- [x] No `/v1/solve` or dashboard change is included.

## Strategy checks

- [x] Exactly one backend strategy is selected: `hybrid`.
- [x] `hosted-only` is not selected.
- [x] `local-only` is not selected.
- [x] Hybrid requires explicit provider selection.
- [x] Hybrid prohibits silent fallback.

## Safety checks

- [x] Local LLM runtime mode is default-off.
- [x] Explicit operator opt-in is required.
- [x] Localhost / loopback endpoint only is required.
- [x] No provider keys are required for local LLM mode.
- [x] Finite timeout is required.
- [x] Fail-closed handling is required for non-local endpoint, malformed endpoint, connection failure, timeout, malformed response, empty output, prompt echo, and system echo.
- [x] Hosted-provider fallback is prohibited unless separately authorized and explicitly labeled.
- [x] Observability must distinguish local LLM output from hosted provider output.
- [x] `behavior_evidence=false` remains preserved unless a later lane explicitly changes the evidence model.
- [x] Runtime smoke is required before any future runtime-readiness claim.
- [x] `/v1/solve` remains blocked from local LLM mode for this implementation phase.
- [x] Dashboard preview remains blocked from local LLM mode for this implementation phase.

## Evidence-boundary checks

- [x] This package is not implementation evidence.
- [x] This package is not runtime evidence.
- [x] This package is not model quality evidence.
- [x] This package is not hosted provider evidence.
- [x] This package is not `/v1/solve` readiness.
- [x] This package is not dashboard preview readiness.
- [x] This package is not MVP validation, production readiness, benchmark evidence, provider orchestration evidence, or Alpha superiority evidence.

## Next-lane check

- [x] Exactly one next lane is selected: `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-IMPLEMENTATION-001`.
