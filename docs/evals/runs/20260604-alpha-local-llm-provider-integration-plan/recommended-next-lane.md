# Recommended Next Lane

Exactly one recommended next lane is selected:

`ALPHA-LOCAL-LLM-PROVIDER-INTEGRATION-SPEC-001`

## Scope for the next lane

The next lane should be spec-first. It should convert this plan into a concrete
implementation contract, select one provider option to design around, define the
file-change boundary, and preserve all authorization gates.

## Required constraints for the next lane

The next lane must:

- remain non-executing unless a later explicit authorization gate approves a
  real provider call;
- preserve `provider_mode="local_llm"`;
- preserve `MODEL_PROVIDER=local` as smoke-only unless explicitly changed by an
  approved implementation lane;
- preserve portable-contract path, SHA-256 fingerprint, fingerprint algorithm,
  and user/system separation;
- start with offline tests and fixtures;
- keep runtime, dashboard preview, hosted providers, `/v1/solve`, and Batch C
  out of scope unless explicitly approved.
