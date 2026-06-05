# Endpoint Locality Review

## Requirement

Local LLM runtime mode may use only localhost or loopback HTTP endpoints. Non-local, hosted, LAN/private-network, malformed, ambiguous, unsupported-scheme, missing-host, userinfo-bearing, and invalid-port endpoints must fail closed.

## Findings

- Endpoint validation strips the input only after requiring a non-empty string.
- Only the `http` scheme is accepted; `https` and other schemes fail closed.
- Userinfo-bearing URLs fail closed when username or password is present.
- Hostnames are normalized and accepted only when they are `localhost` or parse as loopback IP addresses.
- `127.0.0.1` and `::1` are accepted as loopback examples.
- Remote public hosts such as `example.com` fail closed.
- LAN/private-network hosts such as `192.168.1.25` fail closed because they are not loopback.
- Missing-host and ambiguous forms fail closed.
- Invalid or out-of-range ports fail closed when `parsed.port` raises `ValueError`.
- Endpoint validation occurs before transport invocation in the runtime backend and again in the urllib transport.

## Test evidence reviewed

Focused tests cover accepted loopback endpoints, rejected non-local/ambiguous endpoints, and transport-not-called behavior for invalid endpoints. The focused test command passed.

## Decision impact

Endpoint locality review found no blocker for bounded manual smoke. The future smoke lane must still record the exact local endpoint and confirm it is localhost or loopback before execution.
