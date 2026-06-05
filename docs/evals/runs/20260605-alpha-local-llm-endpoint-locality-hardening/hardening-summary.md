# Hardening Summary

Lane ID: `ALPHA-LOCAL-LLM-ENDPOINT-LOCALITY-HARDENING-001`

## Summary

This lane adds endpoint-locality validation to the Ollama-style local HTTP backend before any injected transport can be invoked.

The adapter now fails closed with `endpoint_not_local_non_evidence` when an endpoint is missing, malformed, uses a disallowed scheme, or resolves to a non-loopback / non-local hostname.

## Implemented behavior

- Validates endpoint URLs before request payload creation and before transport invocation.
- Allows loopback endpoints such as `http://127.0.0.1:11434/api/chat`, `http://localhost:11434/api/chat`, and `http://[::1]:11434/api/chat`.
- Rejects hosted and non-loopback endpoints before transport invocation.
- Keeps backend default-off when no transport is injected.
- Preserves `provider_mode="local_llm"`.
- Preserves `MODEL_PROVIDER=local` as separate smoke-only semantics.
- Preserves portable-contract path, SHA-256 fingerprint, fingerprint algorithm, and system/user prompt separation.
- Preserves `behavior_evidence=False`.

## Non-actions

No live smoke, local model call, hosted provider call, `/v1/solve` call, runtime routing change, dashboard preview change, Batch C work, or provider key is introduced.
