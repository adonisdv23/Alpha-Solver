# Offline Test Plan

## Test posture

All tests proposed by this packet are offline. They must not call Ollama, a
hosted provider, a local model, `/v1/solve`, dashboard preview paths, or any
network endpoint.

## Proposed unit tests

A future implementation lane should add focused tests for:

1. Request mapping
   - `LocalLLMAdapterRequest` maps to an Ollama-style local HTTP payload.
   - System and user message separation is preserved.
   - `provider_mode="local_llm"` is retained.
   - `MODEL_PROVIDER=local` is not used as the adapter mode and remains
     smoke-only.
2. Metadata preservation
   - `prompt_source_path` remains present.
   - `prompt_source_fingerprint` and `prompt_source_sha256` remain equal.
   - `prompt_source_fingerprint_algorithm` remains `sha256`.
3. Default-off behavior
   - No backend is constructed or called without explicit opt-in.
   - The disabled/unconfigured model label cannot initiate a live request.
4. Failure handling
   - Timeout returns `failed_closed`.
   - Connection failure returns `failed_closed`.
   - Malformed response returns `failed_closed`.
   - Empty output returns `failed_closed`.
   - Prompt echo returns `failed_closed`.
   - Missing contract and empty contract fail before backend access.
   - Fingerprint mismatch fails before backend access.
   - Backend error returns `failed_closed` without fallback.
5. Non-evidence labeling
   - Offline fixture output remains `behavior_evidence=False`.
   - No test asserts runtime readiness, quality, comparison, billing, benchmark,
     or provider-orchestration conclusions.

## Fixture parser tests

Fixture parser tests should load static JSON files or in-test dictionaries and
assert parser behavior without sockets. They should include successful assistant
text extraction plus malformed, empty, echoed, non-string, and missing-field
cases.

## Optional future smoke test status

An optional future smoke test remains blocked and default-skipped. It would
require a later explicit authorization record naming the lane, local host, port,
URL path, timeout, opt-in command, evidence label, blocked claims, and rollback
steps. This packet does not authorize the smoke test.
