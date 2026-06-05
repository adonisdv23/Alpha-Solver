# Recommended Next Lane

Exactly one next lane is recommended:

`ALPHA-LOCAL-LLM-PROVIDER-INTEGRATION-IMPLEMENTATION-001`

## Scope of the recommended lane

The recommended lane may propose implementation code for an Ollama-style local
HTTP backend behind the existing local LLM adapter seam. It must keep real
provider execution blocked unless a later explicit authorization gate permits a
smoke test.

## Required constraints for the next lane

- Keep `provider_mode="local_llm"`.
- Keep `MODEL_PROVIDER=local` smoke-only unless the approved lane explicitly
  changes that meaning.
- Preserve portable-contract path, SHA-256 fingerprint, `sha256` algorithm, and
  system/user separation.
- Use offline fixtures for parser tests.
- Keep the backend default-off and no-provider-by-default.
- Do not touch runtime routing, `/v1/solve`, dashboard preview, hosted-provider
  paths, provider keys, operator evidence, Batch C materials, backlog workbooks,
  benchmark artifacts, billing artifacts, or provider-orchestration artifacts.
