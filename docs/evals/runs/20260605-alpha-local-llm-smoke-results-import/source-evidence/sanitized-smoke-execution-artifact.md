# ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-001

## Execution metadata

* lane_id: `ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-001`
* prerequisite: PR #305 merged and GS updated
* start_time_utc: `2026-06-05T16:41:02.641341+00:00`
* end_time_utc: `2026-06-05T16:41:41.668264+00:00`
* machine: `macOS-26.2-arm64-arm-64bit`
* python: `3.9.6`
* ollama_version: `ollama version is 0.30.5`
* endpoint_pattern: `http://127.0.0.1:11434/api/chat`
* model: `gemma3:4b`
* timeout_seconds: `120.0`

## Smoke result

```json
{
  "backend_calls": 1,
  "backend_payloads": 1,
  "behavior_evidence": false,
  "exception": null,
  "executed": true,
  "metadata": {
    "backend_class": "stub-local-llm-provider-adapter",
    "behavior_evidence": false,
    "evidence_label": "non_evidence_local_llm_provider_adapter_wiring",
    "model": "gemma3:4b",
    "no_real_provider_call": true,
    "prompt_source_fingerprint": "98841febea17e2ea4d0155df63537bcb76f948e51395bddc1ce870b349d3c7bb",
    "prompt_source_fingerprint_algorithm": "sha256",
    "prompt_source_path": "alpha_solver_portable.py",
    "prompt_source_sha256": "98841febea17e2ea4d0155df63537bcb76f948e51395bddc1ce870b349d3c7bb",
    "provider_mode": "local_llm",
    "real_provider_call_enabled": false
  },
  "output_text": "OK",
  "reason": "local_llm_provider_adapter_wiring_only",
  "status": "non_evidence"
}
```

## Sanitized request artifact

```json
{
  "endpoint_url": "http://127.0.0.1:11434/api/chat",
  "message_roles": [
    "system",
    "user"
  ],
  "model": "gemma3:4b",
  "stream": false,
  "system_message_length": 43125,
  "system_message_omitted": true,
  "user_prompt": "Reply with exactly OK."
}
```

## Raw response artifact

```json
{
  "created_at": "2026-06-05T16:41:41.009865Z",
  "done": true,
  "done_reason": "length",
  "eval_count": 1,
  "eval_duration": 1000,
  "load_duration": 14026933375,
  "message": {
    "content": "OK",
    "role": "assistant"
  },
  "model": "gemma3:4b",
  "prompt_eval_count": 4095,
  "prompt_eval_duration": 22815223000,
  "total_duration": 38342564625
}
```

## Raw artifact preservation notes

* stdout captured in this Markdown file.
* stderr should be preserved separately if Terminal shows any errors.
* request payload is sanitized: full system message is omitted, but system length and role order are preserved.
* endpoint is localhost / loopback only.
* no provider key or hosted provider endpoint is used.

## Evidence boundary

This artifact is local smoke evidence only.

It is not local LLM quality evidence, broad Ollama behavior evidence, hosted provider evidence, /v1/solve readiness evidence, dashboard preview readiness evidence, runtime readiness evidence, MVP validation, production readiness, Alpha quality evidence, Alpha superiority evidence, broad plain-provider inferiority evidence, Batch C readiness, benchmark success, exact billing evidence, or provider orchestration evidence.

## Non-claims

* No readiness claim is made.
* No quality claim is made.
* No benchmark claim is made.
* No production claim is made.
* No provider-orchestration claim is made.
* No Alpha-superiority claim is made.
