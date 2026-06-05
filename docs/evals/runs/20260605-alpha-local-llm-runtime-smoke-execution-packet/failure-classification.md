# Failure Classification

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-PACKET-001`

Use one primary failure classification and optional secondary notes. Preserve raw artifacts for every attempted execution or pre-execution stop.

## Stop conditions and classifications

| Stop condition | Classification |
| --- | --- |
| Review gate missing or not approving smoke | `review gate missing or not approving smoke` |
| Implementation missing | `implementation missing` |
| Required implementation config field absent | `implementation config field absent` |
| Local service unavailable | `local service unavailable` |
| Model unavailable | `model unavailable` |
| Endpoint not local | `endpoint not local` |
| Endpoint redirects | `endpoint redirects` |
| Invalid scheme | `invalid scheme` |
| Userinfo-bearing endpoint | `userinfo-bearing endpoint` |
| Invalid port | `invalid port` |
| Timeout | `timeout` |
| Malformed response | `malformed response` |
| Empty output | `empty output` |
| Prompt echo | `prompt echo` |
| System echo | `system echo` |
| Hosted fallback detected | `hosted fallback detected` |
| Provider key unexpectedly required | `provider key unexpectedly required` |
| Artifact capture cannot be preserved | `artifact capture cannot be preserved` |

## Mapping to implementation reason codes

- `endpoint_not_local_non_evidence` may map to endpoint not local, invalid scheme, userinfo-bearing endpoint, or invalid port depending on the raw validation context.
- `endpoint_redirect_non_evidence` maps to endpoint redirects.
- `timeout_non_evidence` maps to timeout.
- `connection_failure_non_evidence` maps to local service unavailable unless service health artifacts prove a narrower cause.
- `malformed_response_non_evidence` maps to malformed response.
- `empty_model_output_non_evidence` maps to empty output.
- `prompt_echo_non_evidence` maps to prompt echo.
- `system_echo_non_evidence` maps to system echo.
- `provider_keys_forbidden_non_evidence` maps to provider key unexpectedly required or forbidden-key-present depending on context.

## Required language

Classifications must not be converted into readiness, validation, superiority, benchmark, production, MVP, billing, provider-orchestration, hosted-provider, local-model-quality, `/v1/solve`, or dashboard-preview claims.
