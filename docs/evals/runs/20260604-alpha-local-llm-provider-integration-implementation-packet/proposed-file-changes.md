# Proposed Future File-Change Boundary

This document proposes the file boundary for the next lane only. It does not
make those changes in this packet.

## Allowed future implementation files

A later approved implementation lane may consider changes in exactly these areas:

1. `alpha/local_llm/provider_adapter.py`
   - Add an Ollama-style local HTTP backend class or helper functions behind the
     existing `LocalLLMProviderBackend.generate(request)` seam.
   - Add offline response parsing and failure normalization if kept within the
     adapter module.
2. `alpha/local_llm/__init__.py`
   - Export only the new backend or parser symbols required by tests or later
     approved callers.
3. Local LLM adapter tests
   - Add offline unit tests for request mapping, response parsing, failure
     normalization, and preserved metadata.
   - Add fixture parser tests that do not call a live endpoint.
4. Lane-specific docs
   - Add evidence notes for implementation decisions, offline fixture labels,
     blocked smoke behavior, and rollback steps.

## Files that must remain outside the next lane unless a later spec supersedes this packet

- Runtime entrypoints and routing files.
- Hosted-provider adapters.
- Provider-key or credential configuration files.
- `/v1/solve` code paths or evidence.
- Dashboard preview code paths or evidence.
- Operator-test evidence directories.
- Backlog workbooks or registry exports.
- Batch C materials.
- Billing, benchmark, comparison, readiness, or provider-orchestration artifacts.

## Required default behavior

The future backend must be default-off and no-provider-by-default. Without an
explicit approved opt-in, the backend must not initiate HTTP traffic and must not
change existing runtime behavior.
