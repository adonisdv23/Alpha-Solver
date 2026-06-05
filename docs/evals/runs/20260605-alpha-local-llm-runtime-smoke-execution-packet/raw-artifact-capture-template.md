# Raw Artifact Capture Template

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-PACKET-001`

Do not create runtime smoke artifacts in this packet-preparation PR. This template defines what a later authorized execution lane must preserve before sanitization.

## Raw artifact fields

```yaml
lane: ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-001
execution_packet_lane: ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-PACKET-001
review_gate_lane: ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-REVIEW-GATE-001
review_gate_authorized_smoke: <yes/no>
operator: <operator-id-or-redacted-label>
working_directory: <repo-root-or-redacted-path>
start_timestamp_utc: <timestamp>
end_timestamp_utc: <timestamp>
command_path_or_shell: <raw-command-location>
command_exact: |
  <exact command executed>
exit_code: <integer>
raw_stdout_path: <path>
raw_stderr_path: <path>
raw_result_path: <path>
config_summary_path: <path>
sanitized_result_path: <path>
endpoint_summary:
  raw_endpoint_preserved: <yes/no; preserve securely, sanitize before import>
  public_summary: <localhost-or-loopback-only>
  endpoint_host_label: <localhost|loopback>
  scheme: http
  redirect_observed: <yes/no>
local_model: <exact-local-model-name>
timeout_seconds: <finite-positive-number>
provider_mode: local_llm
alpha_local_llm_enabled: true
provider_keys_absent:
  OPENAI_API_KEY: <confirmed-absent/empty>
  ANTHROPIC_API_KEY: <confirmed-absent/empty>
  GOOGLE_API_KEY: <confirmed-absent/empty>
  GEMINI_API_KEY: <confirmed-absent/empty>
  DEEPSEEK_API_KEY: <confirmed-absent/empty>
no_hosted_fallback: <confirmed>
status: <non_evidence|failed_closed|not_run>
reason: <implementation-reason-or-stop-condition>
behavior_evidence: false
failure_classification: <if applicable>
artifact_preservation_confirmed: <yes/no>
```

## Raw stdout and stderr preservation

Preserve the raw `stdout` and `stderr` byte-for-byte in dedicated files. Do not overwrite raw artifacts with sanitized artifacts.

## Raw artifact stop rule

If raw command, stdout, stderr, exit code, config summary, or sanitized result cannot be preserved, stop and classify as `artifact capture cannot be preserved`.
