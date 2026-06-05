# File-Change Boundary

## This lane

Allowed files for this lane are limited to:

- `.specs/alpha-local-llm-provider-integration-spec.md`
- files under `docs/evals/runs/20260604-alpha-local-llm-provider-integration-spec/`

No source code, tests, runtime files, provider configuration, operator evidence,
or backlog workbooks are changed by this lane.

## Future implementation packet boundary

A later approved implementation packet may propose changes to:

- `alpha/local_llm/provider_adapter.py` for an Ollama-style local HTTP backend
  or response parser behind the existing injected-backend seam;
- `alpha/local_llm/__init__.py` only if exports are required;
- local LLM adapter tests for offline unit tests and fixture parser tests;
- a new docs evidence directory for packet-only evidence and any later
  separately authorized smoke labels.

## Blocked files and areas

The future packet must not include runtime entrypoints, `/v1/solve`, dashboard
preview code, hosted-provider adapters, provider routing, provider keys,
operator-test evidence edits, PR #288 through PR #295 evidence rewrites, Batch C
materials, or broad refactors unless a later approved spec changes that scope.
