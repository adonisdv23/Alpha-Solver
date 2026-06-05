# Failure Classification

Future runtime smoke must use one primary failure classification and may add secondary notes when needed.

## Categories

1. `implementation missing` — the reviewed runtime implementation does not exist, is not merged, or the expected smoke entrypoint is unavailable.
2. `environment missing` — required local environment pieces are absent, such as the local runtime process, configuration, or toolchain.
3. `endpoint locality failure` — the endpoint is not localhost or loopback only.
4. `connection failure` — the localhost or loopback endpoint cannot be reached.
5. `model unavailable` — the exact local model name is not available from the local runtime.
6. `timeout` — the request exceeds the finite configured timeout.
7. `malformed response` — the runtime response cannot be parsed according to the future reviewed smoke contract.
8. `empty output` — the runtime returns no usable output.
9. `prompt echo` — the output primarily echoes the user prompt rather than producing a response.
10. `system echo` — the output exposes or echoes system or hidden instruction content.
11. `hosted fallback detected` — evidence indicates fallback to a hosted provider or non-local endpoint.
12. `provider key required` — local mode requires, requests, or fails due to hosted provider credentials.

## Required Evidence Handling

- Preserve raw artifacts for the failure.
- Create a sanitized import after execution only when authorized.
- Preserve `behavior_evidence=false` unless a later lane explicitly changes the evidence model.
- Avoid readiness, validation, superiority, benchmark, production, MVP, billing, runtime, or provider-orchestration claims.
