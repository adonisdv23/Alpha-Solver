# Current Local LLM Adapter Map

## Inventory result

The repository already contains a default-off local LLM adapter and operator-only path. The current state supports documentation-level inventory for model cataloging, not live model evaluation.

## Configuration support

| Item | Observed state | Boundary |
| --- | --- | --- |
| `ALPHA_LOCAL_LLM_ENABLED` | Present in runtime config and operator CLI environment builder. | Required opt-in; disabled by default when absent or false-like. |
| `ALPHA_LOCAL_LLM_ENDPOINT` | Present in runtime config and operator CLI environment builder. | Must pass local loopback validation. |
| `ALPHA_LOCAL_LLM_MODEL` | Present in runtime config and operator CLI environment builder. | Exact non-empty model string required; catalog names are examples only. |
| `ALPHA_LOCAL_LLM_TIMEOUT_SECONDS` | Present in runtime config and operator CLI environment builder. | Must be finite and positive. |
| Local loopback endpoint validation | Present via `validate_ollama_local_endpoint`. | Allows HTTP loopback such as localhost or loopback IP; rejects non-local hosts, credentials, and non-HTTP schemes. |
| Default-off local model behavior | Present. | Runtime config requires explicit enablement and fails closed otherwise. |
| Fake or injected transport tests support | Present by design through injected backend and `OllamaJSONTransport`. | Tests and CI should use injected fake transports; the public/operator runtime path may use the default urllib loopback transport when explicitly enabled and valid config is supplied. |

## Current adapter shape

- The provider adapter builds messages with a portable-contract system message and a separate user message.
- The Ollama backend maps requests to an `/api/chat`-style JSON payload.
- The backend records calls and payloads and validates endpoint/model/timeout before transport use.
- Direct backend construction without a transport fails closed, while `run_configured_local_llm_runtime` supplies the default urllib loopback Ollama transport when local LLM is explicitly enabled and valid endpoint/model/timeout config is provided.
- The operator CLI is explicitly local-only and default-off through a required `--enable-local-llm` flag plus endpoint, model, and timeout arguments, so operator-run local mode may make a real loopback Ollama call after opt-in.
- The orchestration runner is non-production, local-only, and bounded to a two-pass local expert flow.

## Current unsupported states

- No claim is made that any cataloged Ollama model is installed.
- No claim is made that local routing works.
- No claim is made that model output quality, benchmark behavior, or provider readiness has been established.
- This docs-only catalog did not exercise the default urllib loopback transport or any injected fake transport.
