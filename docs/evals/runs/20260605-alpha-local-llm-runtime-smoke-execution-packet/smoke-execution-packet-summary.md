# Smoke Execution Packet Summary

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-PACKET-001`

## Purpose

Prepare the exact future manual local runtime smoke execution packet for the optional local LLM runtime path, using the merged implementation and operator runbook as source material.

## Non-execution statement

Runtime smoke is not executed in this PR. No local model is called. No hosted provider is called. No network calls are made. No smoke result is imported.

This packet is not runtime smoke evidence. It only records instructions, command templates, artifact templates, redaction requirements, expected result fields, failure classes, stop conditions, and the selected next lane.

## Blocking gate

Execution is blocked until `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-REVIEW-GATE-001` explicitly authorizes smoke. If the review gate is missing, incomplete, ambiguous, or does not approve smoke, the future operator must stop before running any smoke command.

## Implementation-aware surface

The merged local runtime path is represented by:

- `LocalLLMRuntimeConfig.from_env()` for explicit environment-based local runtime configuration.
- `OllamaLocalHTTPBackend` for the default-off Ollama-style local HTTP backend.
- `urllib_ollama_json_transport()` for local `http` JSON transport with redirects disabled.
- `run_configured_local_llm_runtime()` for future authorized local runtime invocation.

The packet must preserve the implementation's narrow evidence model: successful output is `status="non_evidence"`, `reason="local_llm_provider_adapter_wiring_only"`, and `behavior_evidence=false`; failures are bounded `failed_closed` outcomes.

## Required local setup fields

Actual values must be confirmed by the operator at execution time:

```dotenv
MODEL_PROVIDER=local_llm
ALPHA_LOCAL_LLM_ENABLED=true
ALPHA_LOCAL_LLM_ENDPOINT=<localhost-or-loopback-http-endpoint>
ALPHA_LOCAL_LLM_MODEL=<exact-local-model-name>
ALPHA_LOCAL_LLM_TIMEOUT_SECONDS=<finite-positive-number>
```

Historical examples only: endpoint pattern `http://127.0.0.1:11434/api/chat`, model `gemma3:4b`, timeout `120`.

## Packet outputs

The future execution packet requires preserving:

- raw command;
- raw stdout;
- raw stderr;
- exit code;
- execution timestamps;
- config summary;
- raw result object or failure object;
- sanitized result;
- stop-condition or failure classification when applicable.
