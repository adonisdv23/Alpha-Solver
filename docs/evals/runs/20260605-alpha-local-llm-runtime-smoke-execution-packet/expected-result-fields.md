# Expected Result Fields

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-PACKET-001`

The future smoke should capture implementation-specific result fields emitted by `run_configured_local_llm_runtime()`.

## Top-level result fields

- `status`: expected `non_evidence` for a bounded non-failed result or `failed_closed` for a bounded failure.
- `reason`: expected implementation reason code.
- `behavior_evidence`: must remain `false`.
- `output_text`: raw model output or empty string on failed-closed outcomes.
- `metadata`: implementation metadata map.

## Expected metadata fields

The merged implementation currently supplies or preserves the following metadata fields for the local runtime path:

- `provider_mode`: `local_llm`
- `backend_class`: `ollama-local-http-runtime`
- `local_backend`: `ollama_chat`
- `local_model`: exact configured local model name
- `model`: exact configured local model name
- `endpoint_is_loopback`: `true`
- `endpoint_host_label`: `localhost` or `loopback`
- `timeout_seconds`: finite positive timeout
- `no_provider_keys_required`: `true`
- `no_hosted_fallback`: `true`
- `behavior_evidence`: `false`
- `failure_label`: `failed_closed_result` when a failure is normalized

## Expected reason codes

Known implementation reason codes include:

- `local_llm_provider_adapter_wiring_only`
- `local_llm_disabled_non_evidence`
- `provider_keys_forbidden_non_evidence`
- `endpoint_not_local_non_evidence`
- `invalid_model_non_evidence`
- `missing_model_non_evidence`
- `invalid_timeout_non_evidence`
- `provider_mode_mismatch_non_evidence`
- `provider_backend_disabled_non_evidence`
- `timeout_non_evidence`
- `connection_failure_non_evidence`
- `backend_error_non_evidence`
- `endpoint_redirect_non_evidence`
- `malformed_response_non_evidence`
- `empty_model_output_non_evidence`
- `prompt_echo_non_evidence`
- `system_echo_non_evidence`

## Blocked-if-absent rule

If any required implementation config field is absent or cannot be mapped at execution time, stop before smoke and classify as `implementation missing` or `implementation config field absent`, rather than inventing a field name.
