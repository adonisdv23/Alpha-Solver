# Authorization Requirements

No real provider call is authorized by this lane.

## Required before any real provider call

A later lane must obtain explicit authorization that names:

- lane ID and spec path;
- provider option selected;
- local endpoint or command shape;
- allowed host, port, process, or socket constraints;
- timeout limits;
- whether any local smoke command may run;
- exact test command and skip/default behavior;
- evidence label for live local smoke output;
- rollback steps;
- confirmation that no hosted provider, provider key, dashboard preview,
  `/v1/solve`, or runtime routing work is included.

## Prompt-source authorization requirements

The future lane must preserve and check:

- portable contract path;
- SHA-256 fingerprint;
- fingerprint algorithm;
- user prompt separated from system/contract content;
- expected-fingerprint mismatch as a fail-closed condition.

## Mode authorization requirements

The future lane must preserve `provider_mode="local_llm"` as the adapter mode.
It must not reinterpret `MODEL_PROVIDER=local`. That value remains smoke-only
unless a later approved implementation lane explicitly changes it and updates
all related specs and tests.

## Non-authorization

This lane does not authorize local model calls, Ollama calls, hosted-provider
calls, provider credentials, network calls, operator-test changes, runtime routing,
API entrypoint work, dashboard preview work, or Batch C work.
