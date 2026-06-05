# Recommended Next Lane

Exactly one recommended next lane is selected:

`ALPHA-LOCAL-LLM-PROVIDER-INTEGRATION-IMPLEMENTATION-PACKET-001`

## Scope

The next lane should prepare an implementation packet/spec only. It should not
implement a provider, run a provider, call Ollama, contact a local model, contact
a hosted provider, add provider keys, use `/v1/solve`, add dashboard preview
integration, edit operator evidence, perform Batch C work, or make readiness,
quality, comparison, benchmark, billing, orchestration, or production claims.

## Packet contents

The packet should restate the Ollama-style local HTTP backend selection, propose
exact files for a future implementation, define offline tests and fixture parser
checks, restate the authorization gate, and include rollback steps. Any smoke
command must remain default-skipped and separately authorized before execution.
