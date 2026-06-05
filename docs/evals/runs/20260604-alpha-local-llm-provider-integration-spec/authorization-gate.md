# Authorization Gate

This lane does not authorize a local provider call.

## Required before any local call

A later authorization record must identify:

- the lane ID and spec path;
- the Ollama-style local HTTP backend as the provider shape;
- approved localhost host, port, path, and transport constraints;
- mandatory timeout value and no-infinite-retry rule;
- exact opt-in command and default-skip flag for smoke checks;
- local smoke evidence label, if smoke execution is later approved;
- confirmation that hosted providers, provider keys, runtime routing,
  dashboard preview, `/v1/solve`, operator evidence edits, Batch C work, and
  readiness/comparison claims are excluded;
- rollback steps.

## Default rule

No provider is called by default. Without explicit authorization, future code
must remain inert or fail closed before provider contact.

## Preserved mode rules

`provider_mode="local_llm"` remains the adapter mode. `MODEL_PROVIDER=local`
remains smoke-only unless a later approved lane explicitly changes that meaning.
