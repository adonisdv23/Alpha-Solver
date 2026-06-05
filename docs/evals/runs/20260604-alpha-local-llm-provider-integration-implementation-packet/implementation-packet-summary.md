# Implementation Packet Summary

Lane ID: `ALPHA-LOCAL-LLM-PROVIDER-INTEGRATION-IMPLEMENTATION-PACKET-001`

## Selected future provider shape

The selected future provider shape is an Ollama-style local HTTP backend. This
packet does not also select an OpenAI-compatible local endpoint or direct
subprocess wrapper.

## Packet-only status

This packet is documentation only and non-executing. It does not add a backend
class, parser, source-code path, test code, runtime switch, provider key,
network call, local model call, hosted-provider call, `/v1/solve` path, or
dashboard preview integration.

## Contract anchors to preserve

A later implementation lane must preserve these anchors:

- `provider_mode="local_llm"` remains the adapter mode.
- `MODEL_PROVIDER=local` remains smoke-only unless a later approved
  implementation lane explicitly changes that meaning.
- The portable-contract path remains present in metadata.
- The portable-contract SHA-256 fingerprint remains present in metadata.
- The fingerprint algorithm remains `sha256`.
- Expected-fingerprint mismatch fails closed before backend access.
- System/contract content remains separated from user prompt content.
- Offline fixture output and any separately authorized smoke output remain
  explicitly labeled and must not become runtime, readiness, quality, or
  comparison evidence.

## Proposed future implementation purpose

The future implementation lane may add an Ollama-style local HTTP backend behind
the existing injected-backend seam. The backend would accept
`LocalLLMAdapterRequest`, map it to an Ollama-style request payload, parse an
offline-fixture-shaped response into normalized adapter output, and fail closed
for unsafe or malformed outcomes.

## Non-execution confirmation

No provider is called by this packet. No endpoint is configured. No model is
started. No evidence outside this packet directory is modified.
