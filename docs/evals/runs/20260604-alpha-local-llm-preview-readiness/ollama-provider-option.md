# Ollama Provider Option

Lane ID: `ALPHA-LOCAL-LLM-PREVIEW-READINESS-001`

Status: feasibility analysis only; Ollama was not run and no local model was called.

## Ollama as a local backend

Ollama is a reasonable first local backend candidate for a future preview lane because it is commonly used for local model serving, can run without cloud API keys, and may expose either native or OpenAI-compatible request surfaces depending on deployment. That does not mean Ollama is validated for Alpha behavior, performance, reliability, or quality. It only means it is plausible as a first backend to evaluate behind a deliberately narrow local LLM preview path.

## Native API vs OpenAI-compatible endpoint

| Option | Pros | Cons | Readiness implication |
| --- | --- | --- | --- |
| Ollama native API | Direct mapping to Ollama concepts; likely clearer backend identity; can preserve Ollama-specific metadata. | Requires a dedicated request/response parser, failure taxonomy mapping, and separate tests. | Best when the project wants explicit Ollama behavior and does not want to rely on compatibility layers. |
| OpenAI-compatible local endpoint | May reuse a chat-completions style mental model and make future local endpoints more interchangeable. | Current OpenAI client uses the Responses API shape, not generic chat completions; compatibility may be incomplete or backend-specific. | Attractive only if a new generic local OpenAI-compatible client is added rather than reusing the current OpenAI Responses client unchanged. |

A future lane should not point the existing `OpenAIProviderClient` at a local base URL without a review. Its code and parsing are built around the OpenAI Responses API, credential expectations, OpenAI provider labels, and OpenAI-specific error messages.

## Likely configuration fields

A future local LLM lane would likely need explicit config such as:

- `MODEL_PROVIDER=local_llm` or `MODEL_PROVIDER=ollama`;
- `LOCAL_LLM_BACKEND=ollama`;
- `LOCAL_LLM_BASE_URL=http://127.0.0.1:11434` or another approved local endpoint;
- `LOCAL_LLM_MODEL=<model-tag>`;
- `LOCAL_LLM_TIMEOUT_MS=<timeout>`;
- `LOCAL_LLM_MAX_TOKENS=<limit>` or backend-specific output limit;
- `LOCAL_LLM_TEMPERATURE=<value>` if stochastic behavior is allowed;
- `LOCAL_LLM_LOCAL_ONLY=true` to fail closed on non-localhost/non-private endpoints;
- `ALPHA_PORTABLE_CONTRACT_PATH=alpha_solver_portable.py` if the path is configurable;
- a safe metadata flag/fingerprint such as `prompt_source=alpha_solver_portable.py` and `prompt_sha256=<hash>`.

## Likely failure modes

- Ollama service not running.
- Model tag not pulled or not available locally.
- Endpoint returns a streaming shape that the adapter does not parse.
- Timeout on slower hardware or large prompts.
- Context window too small for the full portable contract plus user prompt.
- Empty response, prompt echo, or instruction noncompliance.
- Non-local base URL accidentally configured.
- Provider metadata too raw or unsafe to expose.
- Contract read failure or prompt hash mismatch.
- Silent fallback to deterministic v91 path if provider selection is not explicit.

## Model and hardware assumptions

Future docs should record hardware assumptions without broad performance claims. At minimum, each local LLM run should label the machine class, operating environment, backend, model tag/version, approximate memory/accelerator availability when known, timeout, context/window assumptions, and whether the endpoint was localhost/private-network only. The project should not claim general speed, quality, reliability, or portability from a single local machine.

## Why Ollama evidence would not equal OpenAI/Claude evidence

Ollama evidence would be specific to the local backend, model, model tag/version, prompt source, config, and environment used. It would not prove OpenAI behavior, Claude behavior, provider orchestration, cloud-provider fallback behavior, billing behavior, exact cost accounting, broad runtime readiness, production readiness, or Alpha validation. It could support only bounded statements such as local LLM preview wiring worked for a named local backend/model/configuration under the recorded environment.
