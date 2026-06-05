# Fail-Closed Coverage

Lane ID: `ALPHA-LOCAL-LLM-ENDPOINT-LOCALITY-HARDENING-001`

## New endpoint-locality coverage

| Case | Expected result |
| --- | --- |
| Hosted HTTPS endpoint | `endpoint_not_local_non_evidence`; transport not invoked |
| Hosted HTTP endpoint | `endpoint_not_local_non_evidence`; transport not invoked |
| OpenAI-style hosted endpoint | `endpoint_not_local_non_evidence`; transport not invoked |
| Private LAN IP endpoint | `endpoint_not_local_non_evidence`; transport not invoked |
| Non-HTTP scheme | `endpoint_not_local_non_evidence`; transport not invoked |
| Missing host / malformed URL | `endpoint_not_local_non_evidence`; transport not invoked |
| Loopback host with invalid / out-of-range port | `endpoint_not_local_non_evidence`; transport not invoked |
| Empty endpoint | `endpoint_not_local_non_evidence`; transport not invoked |
| 127.0.0.1 loopback endpoint | allowed to reach injected fake transport |
| localhost loopback endpoint | allowed to reach injected fake transport |
| IPv6 loopback endpoint | allowed to reach injected fake transport |

## Preserved fail-closed coverage

This lane preserves existing fail-closed handling for malformed response, non-object response, empty output, prompt echo, system echo, timeout, connection failure, backend error, disabled backend, missing contract, empty contract, and fingerprint mismatch.

## Boundary

The coverage is offline only. No real provider, model, network, runtime route, dashboard path, or smoke execution is used.
