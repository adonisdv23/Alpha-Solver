# Local LLM Endpoint Locality Hardening

Lane ID: `ALPHA-LOCAL-LLM-ENDPOINT-LOCALITY-HARDENING-001`

Status: implementation and offline test lane for endpoint-locality fail-closed handling.

## Purpose

Harden the Ollama-style local LLM adapter so non-local endpoint URLs fail closed before any injected transport can be invoked.

This closes the smoke-progression blocker recorded by PR #303: a future smoke lane must not be able to pass a hosted or non-loopback endpoint to the injected transport path.

## Scope

This lane updates the local LLM adapter seam and focused offline tests only. It does not run smoke and does not call a real provider, model, endpoint, `/v1/solve`, or dashboard preview path.

## Files changed

- `alpha/local_llm/provider_adapter.py`
- `tests/test_local_llm_provider_adapter.py`
- docs under this directory
- docs under `docs/evals/runs/20260605-alpha-local-llm-endpoint-locality-review-gate/`
- docs under `docs/evals/runs/20260605-alpha-local-llm-smoke-authorization-refresh/`

## Evidence boundary

This lane proves endpoint-locality hardening and offline adapter fail-closed behavior only.

It is not local LLM behavior evidence, Ollama behavior evidence, hosted provider evidence, `/v1/solve` readiness evidence, dashboard preview readiness evidence, runtime readiness evidence, MVP validation, production readiness, Alpha quality evidence, Alpha superiority evidence, broad plain-provider inferiority evidence, Batch C readiness, benchmark success, exact billing evidence, or provider orchestration evidence.

## Recommended next lane

`ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-001`

The recommendation remains conditional on review and merge of this hardening lane. Smoke execution still requires explicit operator approval, localhost/loopback endpoint values, exact model name, finite timeout, and raw artifact preservation.
