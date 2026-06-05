# Sanitized Artifact Template

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-PACKET-001`

This template is for a future docs-only import lane after authorized execution. Do not import smoke results in this packet-preparation PR.

```yaml
lane: ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-001
source_packet_lane: ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-PACKET-001
review_gate_authorized_smoke: true
execution_timestamp_utc: <timestamp>
command_summary: <sanitized command summary>
exit_code: <integer>
provider_mode: local_llm
alpha_local_llm_enabled: true
endpoint_public_summary: <localhost|loopback http endpoint; no nonpublic host details beyond loopback>
endpoint_is_loopback: true
endpoint_host_label: <localhost|loopback>
local_backend: ollama_chat
backend_class: ollama-local-http-runtime
local_model: <exact-local-model-name>
timeout_seconds: <finite-positive-number>
no_provider_keys_required: true
provider_keys_absent_confirmed: true
no_hosted_fallback: true
status: <non_evidence|failed_closed>
reason: <implementation reason code>
behavior_evidence: false
output_text_summary: <short sanitized summary or redacted if sensitive>
raw_stdout_artifact: <raw artifact reference>
raw_stderr_artifact: <raw artifact reference>
raw_result_artifact: <raw artifact reference>
failure_classification: <if applicable>
non_claims:
  - not runtime smoke evidence until imported by the future import lane
  - not local model quality evidence
  - not hosted provider evidence
  - not /v1/solve readiness
  - not dashboard preview readiness
  - not MVP validation
  - not production readiness
  - not benchmark evidence
  - not provider orchestration evidence
  - not Alpha superiority evidence
```

## Sanitization requirement

The sanitized artifact must preserve enough information to identify local-only execution and bounded outcome without exposing provider keys, private paths, private URLs, nonpublic endpoints, tokens, full environment dumps, or unrelated machine details.
