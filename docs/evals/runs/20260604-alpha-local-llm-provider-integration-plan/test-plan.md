# Test Plan

## Phase 1: offline tests only

The future implementation must start with tests that do not contact a provider:

- request construction preserves portable-contract path;
- SHA-256 fingerprint and fingerprint algorithm are present;
- user prompt remains separate from system/contract content;
- `provider_mode="local_llm"` is accepted;
- `provider_mode="local"` is rejected so `MODEL_PROVIDER=local` remains
  smoke-only;
- fake backend receives the expected request shape;
- timeout, connection failure, malformed response, empty output, prompt echo,
  missing contract, empty contract, fingerprint mismatch, and backend errors are
  covered through stubs or fixtures;
- no source or test path invokes a real provider by default.

## Phase 2: fixture-based parser tests

If a backend wire format is selected, add static fixture tests for successful
and failed payload parsing. These tests must not open sockets, start services,
use keys, or require local models.

## Phase 3: separately authorized local smoke tests

Only a later authorization gate may permit opt-in local-provider smoke tests.
Those tests must be skipped by default and must require explicit environment
variables or command flags. Their output must be labeled separately from offline
stub evidence.

## Required checks for a future PR

A future PR should run focused unit tests first, then `python -m pytest -q` when
practical. Any opt-in local smoke command must be reported separately and must
not be used to expand claims beyond the approved evidence boundary.
