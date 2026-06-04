# Local LLM Readiness Review

Lane ID: `ALPHA-LOCAL-LLM-PREVIEW-READINESS-001`

Status: docs-only readiness review; no implementation and no model calls.

## Overall assessment

Alpha Solver can likely support a local LLM preview path in principle, but the current repo wiring does not yet provide a trustworthy local LLM behavior surface that consumes the portable Alpha contract. The existing `MODEL_PROVIDER=local` path is a deterministic local/offline fallback for smoke and compatibility, not an LLM provider path. It reaches the v91 Tree-of-Thought implementation through `alpha_solver_entry.py` and strips `context.route` before calling the local solver. It does not read `alpha_solver_portable.py` or transform the portable contract into the prompt sent to a model.

The current local `/dashboard/expert-preview` observation that the panes appeared to echo prompts should remain a surface blocker, not behavior evidence. It likely came from the smoke-oriented local path producing placeholder-like or deterministic local output rather than from a true local LLM consuming the portable prompt contract.

## Feasible in principle?

Yes, but only with explicit new wiring. Feasibility rests on existing seams:

- `ProviderRequest`, `ProviderResult`, and `ProviderError` already describe a minimal provider contract.
- `service.app._get_provider_client()` already uses an injectable provider-client factory.
- `ModelSetRegistry` and `ModelSetResolver` already centralize provider/model selection for the provider-backed path.
- `/dashboard/expert-preview` already calls the shared `solve()` function twice, once plain and once with `context["route"] = "expert"`.

Those seams are currently OpenAI-oriented. They do not by themselves prove Ollama readiness, local endpoint readiness, portable-contract consumption, or answer quality.

## Major blockers

1. **`MODEL_PROVIDER=local` is already a smoke/offline path.** Overloading it for local LLM behavior would blur smoke evidence and local-model evidence.
2. **No current runtime path consumes `alpha_solver_portable.py`.** The portable file is intended as a system prompt / portable behavior contract, but the service path imports `_tree_of_thought` from `alpha_solver_entry.py`.
3. **Provider gating is binary.** `service.app._is_openai_provider_enabled()` only enables provider execution when `MODEL_PROVIDER=openai`; otherwise the code falls back to local deterministic execution.
4. **Model-set validation allows only `openai` and `anthropic`.** A local LLM provider value would require config changes before model-set driven local routing could be represented cleanly.
5. **OpenAI provider code targets the Responses API.** Ollama native `/api/generate` or OpenAI-compatible `/v1/chat/completions` behavior would require a separate adapter/client, request-shape mapping, and safe metadata policy.
6. **Evidence labeling is missing for local model runs.** Future evidence would need backend, model name, model version/tag, base URL class, prompt source hash, environment, route, request count, and no-cloud-provider confirmation.

## Required repo changes for a future lane

A future implementation lane would likely need to:

- introduce a distinct provider value such as `MODEL_PROVIDER=local_llm` or `MODEL_PROVIDER=ollama`, rather than reuse `local`;
- add a local LLM provider client or endpoint adapter behind the existing provider contract;
- extend provider selection beyond `_is_openai_provider_enabled()`;
- update model-set/config validation to represent local LLM backends without enabling cloud provider calls;
- add a wrapper that loads the portable contract from `alpha_solver_portable.py`, preserves a stable prompt-source fingerprint, and passes it as the system prompt or provider request system field;
- add tests proving the local LLM path uses the portable contract and does not call `_tree_of_thought` or v91 for local LLM requests;
- preserve the current `MODEL_PROVIDER=local` smoke behavior separately.

## Recommended approach

Use a new provider value, preferably `MODEL_PROVIDER=local_llm`, with backend-specific config such as `LOCAL_LLM_BACKEND=ollama`, `LOCAL_LLM_BASE_URL`, and `LOCAL_LLM_MODEL`. This is cleaner than `MODEL_PROVIDER=ollama` if the project wants to support both native Ollama and OpenAI-compatible local endpoints under one local-LLM concept. The future implementation should start with a contract-consumption proof before any operator or product/runtime evidence is collected.

## What should not be done yet

- Do not repurpose `MODEL_PROVIDER=local` as a local LLM provider.
- Do not treat `/dashboard/expert-preview` local smoke output as Alpha behavior evidence.
- Do not claim `/v1/solve` product/runtime evidence until a separate lane proves the endpoint consumes the intended portable contract under controlled conditions.
- Do not run operator tests, Batch C, scoring, provider comparisons, or model-output generation from this readiness spike.
- Do not claim Alpha validation, superiority, runtime readiness, production readiness, exact billing, provider orchestration, or OpenAI/Claude behavior from any local LLM feasibility review.
