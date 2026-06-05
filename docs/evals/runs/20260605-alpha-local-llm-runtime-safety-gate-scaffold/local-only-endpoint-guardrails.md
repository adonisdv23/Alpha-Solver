# Local-Only Endpoint Guardrails

This is a scaffold only. Local LLM runtime integration is not implemented here.

## Required endpoint locality

Any future local LLM runtime implementation must accept only localhost or loopback endpoints for local LLM mode. The acceptable endpoint boundary must be limited to local machine targets such as `localhost`, `127.0.0.1`, and `::1`, subject to a future implementation spec defining exact parsing rules.

## Fail-closed endpoint handling

A future implementation must fail closed for:

- non-local endpoint;
- malformed endpoint;
- endpoint values that cannot be parsed deterministically;
- endpoint values that could be interpreted as hosted, remote, or network provider targets.

## Provider-key separation

Local LLM mode must require no hosted-provider keys, no local-provider keys, and no provider credential fallback path. If a provider key is required for a path, that path must not be treated as local LLM mode.

## No readiness claim

These guardrails are requirements for future work only. They are not runtime evidence and do not prove endpoint-locality enforcement in code.
