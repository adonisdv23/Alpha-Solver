# Fail-Closed Review

## Covered fail-closed cases

| Case | Reviewed outcome |
| --- | --- |
| Timeout | `timeout_non_evidence` normalized to a failed-closed result. |
| Connection failure | `connection_failure_non_evidence` normalized to a failed-closed result. |
| Backend error | `backend_error_non_evidence` or existing injected-backend adapter error normalization. |
| Prompt echo | `prompt_echo_non_evidence` failed-closed result. |
| System echo | `prompt_echo_non_evidence` failed-closed result. |
| Missing contract | Portable-contract loader error before backend invocation. |
| Empty contract | Portable-contract loader error before backend invocation. |
| Fingerprint mismatch | Portable-contract loader error before backend invocation. |
| Disabled backend | `provider_backend_disabled_non_evidence` failed-closed result. |
| Malformed response | `malformed_response_non_evidence` parser error. |
| Non-object response | `malformed_response_non_evidence` parser error. |
| Empty output | `empty_model_output_non_evidence` or proof-seam `empty_output_non_evidence`. |
| Non-assistant role | `malformed_response_non_evidence` parser error. |

## Unresolved fail-closed case

Endpoint-locality enforcement is not yet covered. A later smoke lane must not run until the backend fails closed on non-loopback / non-local endpoint URLs before invoking any transport.

The future hardening lane must add tests proving hosted URLs such as `https://example.com/api/chat` fail closed without transport invocation.

## Boundary

All reviewed failures are offline-only. They do not prove model execution, local service availability, runtime integration, or answer quality.
