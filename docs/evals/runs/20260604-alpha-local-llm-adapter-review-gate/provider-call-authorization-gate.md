# Provider Call Authorization Gate

This document records what must be true before any future lane may attempt real
local-provider execution. This review gate itself does not grant that
authorization.

## Current authorization status

Real provider calls are not authorized.

The current adapter seam remains inert and reviewable only through injected
stub/fake backends. No local model, Ollama, hosted-provider, provider-key,
network, `/v1/solve`, dashboard preview, or runtime routing call is authorized
by this lane.

## Minimum prerequisites for a future authorization request

A future authorization request must include all of the following before it can
be considered:

- A new or updated spec in `.specs/` that explicitly scopes provider execution.
- A separate lane ID from this review gate.
- Explicit operator approval for the provider class and execution environment.
- A clear distinction between adapter-wiring checks and real execution checks.
- A plan for preserving prompt-source path and SHA-256 metadata.
- A plan for keeping user prompt content separate from system/contract content.
- A plan for retaining `provider_mode="local_llm"` separation from
  `MODEL_PROVIDER=local` unless a specific approved runtime change says
  otherwise.
- A fail-closed plan for empty output, prompt echo, backend error, missing
  contract, empty contract, fingerprint mismatch, connection failure, timeout,
  and malformed response.
- A non-evidence labeling plan for any dry-run, stub, fake, or fixture output.
- A rollback plan that leaves runtime paths unchanged if authorization is not
  granted.

## Explicit non-authorization

This gate does not authorize:

- real local-provider calls;
- Ollama calls;
- hosted-provider calls;
- provider-key use;
- `/v1/solve` calls;
- dashboard preview use;
- runtime provider routing changes;
- `MODEL_PROVIDER=local` semantic changes;
- v91 fallback substitution;
- operator-test interpretation;
- Batch C work.
