# Alpha Local LLM Provider Adapter

Lane ID: `ALPHA-LOCAL-LLM-PROVIDER-ADAPTER-001`

Status: provider-adapter wiring proof only.

## Purpose

Add a narrow local LLM provider-adapter seam that builds on the fake-client
contract-consumption proof. The seam constructs an adapter-shaped request from
`alpha_solver_portable.py`, keeps the portable contract as system/contract
content, keeps the user prompt separate, and records prompt-source metadata.

## Scope

This lane is intentionally inert by default. It adds an injected-backend adapter
interface under `alpha/local_llm/` and offline tests that use only a stub backend.
It does not wire local LLM behavior into `/v1/solve`, dashboard preview, the
runtime provider registry, or `MODEL_PROVIDER=local`.

## Files changed

- `alpha/local_llm/__init__.py`
- `alpha/local_llm/provider_adapter.py`
- `tests/test_local_llm_provider_adapter.py`
- `docs/evals/runs/20260604-alpha-local-llm-provider-adapter/README.md`
- `docs/evals/runs/20260604-alpha-local-llm-provider-adapter/adapter-design.md`
- `docs/evals/runs/20260604-alpha-local-llm-provider-adapter/evidence-boundary.md`
- `docs/evals/runs/20260604-alpha-local-llm-provider-adapter/adapter-preservation-checklist.md`
- `docs/evals/runs/20260604-alpha-local-llm-provider-adapter/recommended-next-lane.md`

## What this lane may prove

- A local-LLM-shaped adapter request can be built from `alpha_solver_portable.py`.
- The request preserves the portable contract path and SHA-256 fingerprint.
- The system/contract content and user prompt remain separate message entries.
- The adapter path uses a distinct `local_llm` label.
- The adapter path does not use v91 `_tree_of_thought` fallback.
- The adapter fails closed for empty output, prompt echo, and injected-backend
  errors.
- Stub tests run offline without model servers or provider keys.

## What this lane does not prove

- No local LLM behavior is proven.
- No Ollama behavior is proven.
- No hosted provider behavior is proven.
- No `/v1/solve` readiness is proven.
- No dashboard preview readiness is proven.
- No runtime readiness, MVP validation, production readiness, Alpha quality,
  Alpha superiority, broad plain-provider inferiority, Batch C readiness,
  benchmark success, exact billing accuracy, or provider orchestration is
  claimed.
