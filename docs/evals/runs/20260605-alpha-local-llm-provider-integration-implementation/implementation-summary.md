# Implementation Summary

## Scope

Implemented behind the existing injected-backend seam only:

- Ollama-style `/api/chat` request mapping from the adapter request.
- Static Ollama-style response parsing for assistant text extraction.
- A default-off backend class requiring an explicitly injected JSON transport.
- Offline tests that use pure dictionaries and fake transports.

## Preserved behavior

- `provider_mode` remains `local_llm`.
- `MODEL_PROVIDER=local` remains a separate smoke-only label.
- The portable contract path and SHA-256 fingerprint metadata remain preserved.
- System contract text and user prompt text remain separate messages.
- `behavior_evidence` remains `False`.
- Default construction does not have a provider transport.

## Evidence label

This is `non_evidence_wiring` plus `offline_fixture_evidence` only.
