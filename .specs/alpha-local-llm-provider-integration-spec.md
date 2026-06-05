# Alpha Local LLM Provider Integration Spec

Lane ID: `ALPHA-LOCAL-LLM-PROVIDER-INTEGRATION-SPEC-001`

Status: specification only, non-executing.

Recommended follow-on lane: `ALPHA-LOCAL-LLM-PROVIDER-INTEGRATION-IMPLEMENTATION-PACKET-001`.

## Purpose

This spec turns the local LLM provider integration plan into a concrete future
implementation contract while preserving all current authorization gates. It is
not an implementation lane and does not permit a provider call, model call,
network call, runtime route change, dashboard preview path, provider key, or
operator evidence update.

The future implementation packet must remain packet/spec preparation only unless
a later explicit authorization gate allows implementation work.

## Source of truth reviewed

The implementation packet must continue from these source-of-truth artifacts:

- `alpha/local_llm/provider_adapter.py`
- `alpha/local_llm/__init__.py`
- `alpha/local_llm/portable_contract.py`
- `tests/test_local_llm_provider_adapter.py`
- `tests/test_local_llm_contract_consumption_proof.py`
- `docs/evals/runs/20260604-alpha-local-llm-provider-adapter/`
- `docs/evals/runs/20260604-alpha-local-llm-adapter-review-gate/`
- `docs/evals/runs/20260604-alpha-local-llm-provider-integration-plan/`

## Selected provider shape

Exactly one future provider shape is selected: an Ollama-style local HTTP
backend.

This shape is selected because it is the narrowest local endpoint target from
the plan options and can be specified behind localhost-only endpoint rules,
mandatory timeout handling, explicit opt-in, default-skip smoke behavior, and
offline request/response fixtures.

The future implementation packet must not also target an OpenAI-compatible local
endpoint or a direct subprocess wrapper. Those alternatives remain out of scope
for this lane family unless a later spec replaces this selection.

## Future file-change boundary

A future implementation packet may propose changes only after a separate
approval step. The expected implementation boundary is:

- `alpha/local_llm/provider_adapter.py` for a backend class or parser wired to
  the existing injected-backend seam;
- `alpha/local_llm/__init__.py` only if public exports need to expose the new
  backend or parser;
- tests under the local LLM adapter test area for offline unit and fixture
  parser checks;
- docs under a new lane-specific evidence directory for packet evidence and
  later, separately approved smoke labels.

The future implementation boundary must not include runtime entrypoints,
provider routing, hosted-provider adapters, dashboard preview code, `/v1/solve`,
operator-test evidence directories, backlog workbooks, Batch C materials, or
provider-key/configuration files unless a later approved spec explicitly changes
that scope.

## Preserved adapter contract

A future implementation must preserve all existing adapter invariants:

- `provider_mode="local_llm"` remains the adapter mode;
- `MODEL_PROVIDER=local` remains smoke-only unless a later approved
  implementation lane explicitly changes that semantic;
- the portable-contract path is retained in metadata;
- the SHA-256 fingerprint is retained in metadata;
- the fingerprint algorithm remains SHA-256;
- expected-fingerprint mismatch fails closed before any backend call;
- system/contract content remains separated from user prompt content;
- no v91 deterministic fallback may be substituted as provider output;
- fixture or smoke output must not be upgraded into runtime, quality, or
  readiness evidence.

## No-provider-by-default rule

Default behavior must remain inert. A future implementation must not call a
local endpoint unless all of the following are true:

1. the lane has separate explicit authorization for implementation or smoke
   execution;
2. the selected provider shape is still the Ollama-style local HTTP backend;
3. the endpoint is localhost or another explicitly approved local address;
4. a bounded timeout is configured;
5. the call path is opt-in and skipped by default in test runs;
6. the output label distinguishes offline fixture evidence from local smoke
   evidence;
7. rollback steps are documented before execution.

If any condition is absent, the backend must not be called and the result must
fail closed or remain skipped, depending on whether it is implementation code or
a smoke test.

## Authorization gate before any local provider call

Before any local provider call, a later authorization record must name:

- lane ID and spec path;
- provider shape, fixed to the Ollama-style local HTTP backend unless a later
  spec supersedes this one;
- approved host, port, URL path, and transport limits;
- timeout value and no-infinite-retry policy;
- exact opt-in command, environment flag, and skip-by-default behavior;
- evidence label for local smoke output;
- confirmation that hosted providers, provider keys, runtime routing,
  dashboard preview paths, `/v1/solve`, operator evidence edits, Batch C work,
  and readiness/comparison claims are out of scope;
- rollback steps for removing or disabling the backend path.

This spec does not provide that execution authorization.

## Response and failure handling

A future backend must fail closed for all of the following cases:

| Case | Required handling |
| --- | --- |
| Timeout | Abort the request, return `failed_closed`, and record a timeout reason without retry loops. |
| Connection failure | Return `failed_closed`; do not route to hosted providers or alternate backends. |
| Malformed response | Reject unexpected JSON, missing fields, or non-text output and return `failed_closed`. |
| Empty output | Treat empty or whitespace-only text as `failed_closed`. |
| Prompt echo | Return `failed_closed` when normalized output matches the user prompt or system/contract content. |
| Missing contract | Use the portable-contract loader error path and do not call the backend. |
| Empty contract | Use the portable-contract loader error path and do not call the backend. |
| Fingerprint mismatch | Return `failed_closed` before backend invocation. |
| Backend errors | Return `failed_closed` with a backend-error reason and no fallback provider call. |

All failed-closed paths must keep evidence labels non-upgraded and must not make
quality, readiness, comparison, billing, or orchestration claims.

## Test strategy

The required order for future test work is:

1. offline unit tests first, using injected fakes or pure parser inputs;
2. fixture parser tests second, using recorded local-shape payloads that do not
   require a running service;
3. opt-in local smoke tests only after separate authorization;
4. no network or provider dependency in default tests.

Any future smoke test must be skipped by default. It must require an explicit
operator-controlled flag and an approved localhost endpoint. It must never be
part of the default `python -m pytest -q` path.

## Evidence labels

Future evidence must use these labels or their exact lane-approved successors:

- `offline_fixture_evidence`: parser and request/response fixture checks with no
  service contact;
- `local_smoke_evidence`: local endpoint smoke output only if separately
  authorized later;
- `non_evidence_wiring`: seam construction, metadata preservation, and injected
  fake/stub handoff;
- `failed_closed_result`: normalized failure outcomes for timeout, connection,
  parsing, empty output, prompt echo, contract, fingerprint, and backend-error
  cases.

## Evidence boundary

This lane is specification evidence only. It is not evidence for local model
execution, Ollama execution, hosted-provider execution, API route readiness,
dashboard preview readiness, runtime readiness, MVP status, production status,
Alpha quality, comparative Alpha claims, broad plain-provider comparison,
Batch C status, benchmark outcomes, exact billing outcomes, or provider
orchestration.

## Rollback

The rollback plan for a future implementation packet must include:

- removal or disablement of the new backend/parser files or exports;
- restoration of inert default behavior;
- removal of opt-in smoke commands and flags if authorization is withdrawn;
- confirmation that default tests still have no provider or network dependency;
- preservation of portable-contract loading and current adapter tests.

## Non-goals

This lane and the recommended next lane do not:

- implement a provider;
- call Ollama, a local model, or a hosted provider;
- add provider keys or private endpoint configuration;
- change runtime routing, API entrypoints, `/v1/solve`, or dashboard preview;
- edit operator-test evidence;
- perform Batch C work;
- claim readiness, quality, superiority, benchmark, billing, orchestration, or
  production outcomes.
