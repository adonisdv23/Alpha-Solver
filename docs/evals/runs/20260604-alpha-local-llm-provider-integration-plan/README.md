# Alpha Local LLM Provider Integration Plan

Lane ID: `ALPHA-LOCAL-LLM-PROVIDER-INTEGRATION-PLAN-001`

Status: plan/review only.

## Purpose

This lane records a non-executing plan for a future lane that may connect the
existing local LLM adapter seam to a real local-provider backend. It does not
change source code, tests, routing, runtime behavior, provider configuration, or
operator evidence.

## Source files reviewed

- `alpha/local_llm/provider_adapter.py`
- `alpha/local_llm/__init__.py`
- `alpha/local_llm/portable_contract.py`
- `tests/test_local_llm_provider_adapter.py`
- `tests/test_local_llm_contract_consumption_proof.py`
- `docs/evals/runs/20260604-alpha-local-llm-provider-adapter/`
- `docs/evals/runs/20260604-alpha-local-llm-adapter-review-gate/`

## Plan scope

A future implementation lane may propose an adapter backend that receives the
existing `LocalLLMAdapterRequest`, preserves prompt-source metadata, calls only a
separately authorized local backend, normalizes failures, and returns a
non-upgraded result unless an approved evidence lane later defines stronger use.

The future lane must preserve the distinction between `provider_mode="local_llm"`
and `MODEL_PROVIDER=local`. `MODEL_PROVIDER=local` remains smoke-only unless a
later approved implementation lane explicitly changes that semantic.

## Required companion documents

- `integration-plan.md`
- `provider-options.md`
- `authorization-requirements.md`
- `failure-handling-plan.md`
- `test-plan.md`
- `evidence-boundary.md`
- `implementation-non-goals.md`
- `recommended-next-lane.md`
- `plan-preservation-checklist.md`

## Evidence boundary

This directory is planning evidence only. It is not model-output evidence,
provider-execution evidence, API readiness evidence, dashboard readiness
evidence, runtime evidence, validation evidence, comparative evidence, Batch C
evidence, billing evidence, benchmark evidence, or orchestration evidence.
