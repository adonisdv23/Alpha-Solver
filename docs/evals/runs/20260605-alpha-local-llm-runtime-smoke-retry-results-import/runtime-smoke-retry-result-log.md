# Runtime Smoke Retry Result Log

## Source evidence

`docs/evals/runs/20260605-alpha-local-llm-runtime-smoke-execution-retry/source-evidence/ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-RETRY-002.md`

## Result log

- `attempt_id`: `002`
- `retry_reason`: `prior smoke artifact had incomplete exact executable command provenance; attempt 001 failed before runtime due missing repo-root PYTHONPATH`
- Attempt 001 context: prior failed runner/import-path attempt caused by missing repo-root `PYTHONPATH`; this is not treated as a local LLM runtime failure.
- Attempt 002 correction: repo root was included in `PYTHONPATH`; the exact executable shell command and exact Python script were preserved.
- The preserved Python script imports and calls `run_configured_local_llm_runtime(USER_PROMPT, env=os.environ)`.
- The preserved Python script serializes the returned result to JSON with `json.dumps(record, sort_keys=True, indent=2)`.
- Precheck command: `PYTHONPATH="<repo-root>" python3 scripts/check_env.py`
- Precheck exit code: `0`
- `smoke_ran`: `yes`
- `smoke_exit_code`: `0`
- `provider_mode`: `local_llm`
- `ALPHA_LOCAL_LLM_ENABLED`: `true`
- Endpoint summary: localhost / loopback HTTP endpoint.
- `endpoint_pattern_used`: `http://127.0.0.1:11434/api/chat`
- Model: `gemma3:4b`
- Timeout: `120` seconds
- Result status: `non_evidence`
- Result reason: `local_llm_provider_adapter_wiring_only`
- Result `output_text`: `OK`
- Result `behavior_evidence`: `false`
- Metadata includes `backend_class: ollama-local-http-runtime`, `endpoint_host_label: loopback`, `endpoint_is_loopback: true`, `local_backend: ollama_chat`, `local_model: gemma3:4b`, `no_hosted_fallback: true`, `no_provider_keys_required: true`, `no_real_provider_call: true`, `provider_mode: local_llm`, `real_provider_call_enabled: false`, and `timeout_seconds: 120.0`.
- Prompt source fingerprint metadata is present: `prompt_source_fingerprint`, `prompt_source_fingerprint_algorithm: sha256`, `prompt_source_path: alpha_solver_portable.py`, and `prompt_source_sha256`.
- Raw precheck stdout/stderr and raw runtime smoke stdout/stderr are preserved in the source evidence.
- Local artifact hygiene caveats are preserved: an untracked prior smoke artifact at repo root and untracked manual-artifact folders from prior local attempts were present in the source artifact repo status sections.

## Bounded result statement

The imported retry smoke supports only that the merged optional local LLM runtime path executed one local loopback retry smoke with complete executable command provenance and returned the recorded `non_evidence` result with `output_text: OK` and `behavior_evidence: false`.

## Excluded evidence

Terminal wrapper noise is not imported as smoke evidence. The import does not reconstruct missing fields and does not use material outside the repo-source artifact.
