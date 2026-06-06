# Current Local Path Trace

## Scope

This trace describes the current local LLM runtime path only. It does not execute a local model and does not claim runtime readiness beyond the already closed local runtime smoke track.

## Path steps

| Step | Current local path behavior | Primary source evidence |
| --- | --- | --- |
| 1. Env/config validation | `LocalLLMRuntimeConfig.from_env` requires `ALPHA_LOCAL_LLM_ENABLED` truthy, rejects configured hosted provider keys, validates endpoint, requires an exact non-empty model name, and requires a finite positive timeout. | `alpha/local_llm/provider_adapter.py` |
| 2. Local endpoint validation | `validate_ollama_local_endpoint` accepts only `http` URLs with no userinfo and a localhost/loopback hostname; non-local, malformed, unsupported, or ambiguous endpoints fail closed before transport use. | `alpha/local_llm/provider_adapter.py` |
| 3. Portable contract loading | `build_local_llm_adapter_request` loads the portable contract via `load_portable_contract`, sets the loaded contract text as the system message, preserves the user prompt as a separate user message, and records non-evidence metadata. | `alpha/local_llm/provider_adapter.py`; `alpha_solver_portable.py` |
| 4. Ollama payload construction | `OllamaLocalHTTPBackend.generate` calls `build_ollama_chat_payload`, which maps the adapter messages into an Ollama-style `/api/chat` payload with `model`, `messages`, and `stream`. | `alpha/local_llm/provider_adapter.py` |
| 5. Local transport | `run_configured_local_llm_runtime` builds an `OllamaLocalHTTPBackend` and uses either an injected transport or the loopback-only `urllib_ollama_json_transport`; the transport performs an HTTP POST only after local endpoint and timeout validation and has no hosted-provider fallback. | `alpha/local_llm/provider_adapter.py` |
| 6. Response parsing | `parse_ollama_chat_response` requires a mapping with an assistant or omitted-role message and non-empty string content. | `alpha/local_llm/provider_adapter.py` |
| 7. Fail-closed result wrapper | `run_local_llm_provider_adapter` normalizes adapter/backend exceptions, empty output, prompt echo, and system echo to `failed_closed`; successful adapter output remains `status: non_evidence` with `behavior_evidence=false`. | `alpha/local_llm/provider_adapter.py` |

## Active current path summary

`run_configured_local_llm_runtime(user_prompt, env=..., transport=...)` → `LocalLLMRuntimeConfig.from_env` → `LocalLLMRuntimeConfig.build_backend` → `run_local_llm_provider_adapter` → `build_local_llm_adapter_request` → `OllamaLocalHTTPBackend.generate` → `build_ollama_chat_payload` → local-only transport → `parse_ollama_chat_response` → `LocalLLMAdapterResult`.

## Explicit bypasses in the current local path

The current local path does not call:

- `alpha_solver_entry._tree_of_thought`.
- `alpha-solver-v91-python.py` `_tree_of_thought`.
- `PortableAlphaSolver.solve` or `SolverEnvelope` assembly.
- `service.app.solve` `/v1/solve` lifecycle.
- `service.app` expert two-pass prompts or confidence-mode gates.
- `alpha.reasoning.react_lite.run_react_lite`.
- `alpha.core.runner.run_reasoning`, plan runner, or governance execution.
- `alpha.reasoning.cot.run_cot` or `alpha.reasoning.cot_self_validate.validate_answer`.
- `alpha.webapp.routes.expert_preview` dashboard routes.
- OpenAI/provider client, model-set resolver, provider accounting, or hosted-provider fallback.
