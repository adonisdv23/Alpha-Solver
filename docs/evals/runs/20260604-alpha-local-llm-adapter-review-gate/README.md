# Alpha Local LLM Adapter Review Gate

Lane ID: `ALPHA-LOCAL-LLM-ADAPTER-REVIEW-GATE-001`

Status: docs-only review gate for the PR #290 provider-adapter seam.

## Purpose

This review gate decides whether the local LLM provider-adapter seam added in
PR #290 is safe to use as the starting point for a later local-provider planning
lane. It reviews adapter wiring, preservation checks, fail-closed handling, and
evidence boundaries only.

## Source files reviewed

- `alpha/local_llm/provider_adapter.py`
- `alpha/local_llm/__init__.py`
- `alpha/local_llm/portable_contract.py`
- `tests/test_local_llm_provider_adapter.py`
- `tests/test_local_llm_contract_consumption_proof.py`
- `docs/evals/runs/20260604-alpha-local-llm-provider-adapter/README.md`
- `docs/evals/runs/20260604-alpha-local-llm-provider-adapter/adapter-design.md`
- `docs/evals/runs/20260604-alpha-local-llm-provider-adapter/evidence-boundary.md`
- `docs/evals/runs/20260604-alpha-local-llm-provider-adapter/adapter-preservation-checklist.md`
- `docs/evals/runs/20260604-alpha-local-llm-provider-adapter/recommended-next-lane.md`

## Review-gate findings

- The adapter builds requests from `alpha_solver_portable.py` by using the
  portable contract loader.
- Prompt-source path and SHA-256 metadata are preserved in request metadata.
- The portable contract is represented as system/contract content, while the
  user prompt is retained separately.
- `provider_mode="local_llm"` is a distinct adapter label and is not the same as
  `MODEL_PROVIDER=local`.
- `MODEL_PROVIDER=local` remains smoke-only unless a separate approved lane
  changes runtime behavior.
- The adapter uses injected backend seams and has no default real-provider path.
- The covered tests use offline stub/fake backends.
- Adapter output remains `behavior_evidence=False` and is labeled as wiring-only
  non-evidence.
- The adapter and proof paths fail closed for empty output, prompt echo, backend
  error, missing contract, empty contract, and fingerprint mismatch.
- No v91 `_tree_of_thought` fallback is part of the seam.

## Evidence boundary

This gate may support only adapter-wiring review. It is not evidence for:

- local model quality or execution;
- Ollama execution;
- hosted-provider execution;
- `/v1/solve` readiness;
- dashboard preview readiness;
- runtime readiness;
- MVP validation;
- production readiness;
- Alpha quality;
- Alpha comparative-superiority;
- broad plain-provider inferiority;
- Batch C readiness;
- benchmark success;
- exact billing evidence;
- provider orchestration.

## Gate decision

No review blockers were identified for moving to a plan/review lane, provided
that the next lane remains non-executing and does not call a real local model,
Ollama, hosted providers, `/v1/solve`, or dashboard preview paths.

Preferred recommended next lane:
`ALPHA-LOCAL-LLM-PROVIDER-INTEGRATION-PLAN-001`.

The recommended lane must be planning/review only and must not execute a real
provider.

## Files in this review gate

- `adapter-review-checklist.md`
- `adapter-merge-blockers.md`
- `adapter-safe-next-options.md`
- `provider-call-authorization-gate.md`
- `evidence-boundary-review.md`
- `review-gate-preservation-checklist.md`
