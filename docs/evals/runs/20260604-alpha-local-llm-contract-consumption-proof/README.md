# Alpha Local LLM Contract Consumption Proof

Lane ID: `ALPHA-LOCAL-LLM-CONTRACT-CONSUMPTION-PROOF-001`

Status: fake-client contract-consumption proof only.

## Purpose

Prove that Alpha Solver can load the intended portable behavior contract from
`alpha_solver_portable.py`, construct a local-LLM-style request with that
contract as the prompt source, preserve safe prompt-source fingerprint metadata,
and avoid v91 / `_tree_of_thought` fallback in the proof path.

## Scope

This lane adds a minimal, isolated proof seam. It does not wire local LLM
behavior into `/v1/solve`, `/dashboard/expert-preview`, the provider registry,
or `MODEL_PROVIDER=local`. The existing `MODEL_PROVIDER=local` behavior remains
smoke/offline deterministic behavior and is not overloaded for local LLM use.

## Files changed

- `alpha/local_llm/__init__.py`
- `alpha/local_llm/portable_contract.py`
- `tests/test_local_llm_contract_consumption_proof.py`
- `docs/evals/runs/20260604-alpha-local-llm-contract-consumption-proof/README.md`
- `docs/evals/runs/20260604-alpha-local-llm-contract-consumption-proof/contract-consumption-proof.md`
- `docs/evals/runs/20260604-alpha-local-llm-contract-consumption-proof/proof-preservation-checklist.md`
- `docs/evals/runs/20260604-alpha-local-llm-contract-consumption-proof/recommended-next-lane.md`

## What was proven

- `alpha_solver_portable.py` can be loaded as direct prompt-source text.
- The prompt source is fingerprinted with SHA-256 and labeled with the safe
  source path `alpha_solver_portable.py`.
- A local-LLM-style fake request can keep the portable contract in the `system`
  field and the user prompt in a separate `user_prompt` field.
- Request metadata identifies the prompt source path, prompt source fingerprint,
  fake backend class, `local_llm` proof mode, no real provider call, and no
  behavior evidence.
- The proof path does not import `alpha_solver_entry.py`, does not import
  `alpha-solver-v91-python.py`, and does not call `_tree_of_thought`.
- `provider_mode=local` is rejected for this proof helper so that
  `MODEL_PROVIDER=local` remains smoke-only.
- Missing contract files and SHA-256 mismatches fail closed.
- Empty output, prompt echo, and fake-client failure are labeled as failed-closed
  non-evidence conditions.

## What was not proven

- No Ollama adapter was implemented.
- No local model was called.
- No OpenAI, Anthropic, or other provider was called.
- `/v1/solve` behavior was not used as evidence.
- `/dashboard/expert-preview` behavior was not used as evidence.
- No operator-test results were imported.
- No Batch C, scoring, validation, superiority, production-readiness, runtime
  readiness, provider-orchestration, or exact-billing claim is made.

## Checks run

- `git status --short`
- `git diff --check`
- `git diff --name-only main...HEAD` where available, with a fallback to
  `git diff --name-only --cached --diff-filter=ACMRT` before commit because this workspace has no `main` ref.
- `python -m pytest tests/test_local_llm_contract_consumption_proof.py -q`
- `python -m pytest tests/test_alpha_minimal_behavior_contract.py -q`
- `MODEL_PROVIDER=local python scripts/check_env.py`

## Next recommended lane

Recommended next lane: `ALPHA-LOCAL-LLM-PROVIDER-ADAPTER-001`.
