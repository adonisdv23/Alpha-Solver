# Spec Summary

The spec creates a concrete contract for a future local LLM provider integration
packet while keeping this lane non-executing.

## Required preservation

The future packet must preserve:

- `provider_mode="local_llm"`;
- `MODEL_PROVIDER=local` as smoke-only unless a later approved lane explicitly
  changes it;
- portable-contract path metadata;
- SHA-256 fingerprint metadata;
- SHA-256 as the fingerprint algorithm;
- system/contract and user prompt separation;
- expected-fingerprint mismatch as a fail-closed pre-call condition;
- no-provider-by-default behavior.

## Future target

The spec selects exactly one future shape: an Ollama-style local HTTP backend.
The target remains behind localhost constraints, mandatory timeout handling,
explicit opt-in, default skips, and offline fixtures.

## Current lane result

The current lane is specification evidence only. It produces no runtime,
provider, model, API, dashboard, operator, benchmark, billing, comparison, or
Batch C evidence.
