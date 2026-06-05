# Smoke Result Summary

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-TRACK-CLOSEOUT-001`

## Runtime smoke facts preserved

- command precheck: `python3 scripts/check_env.py`
- precheck exit_code: `0`
- smoke_ran: `yes`
- smoke_exit_code: `0`
- provider_mode: `local_llm`
- `ALPHA_LOCAL_LLM_ENABLED=true`
- endpoint summary: localhost / loopback HTTP endpoint
- endpoint_pattern_used: `http://127.0.0.1:11434/api/chat`
- endpoint_host_label: `loopback`
- endpoint_is_loopback: `true`
- model: `gemma3:4b`
- local_model: `gemma3:4b`
- timeout_seconds: `120` / `120.0`
- backend_class: `ollama-local-http-runtime`
- local_backend: `ollama_chat`
- no_hosted_fallback: `true`
- no_provider_keys_required: `true`
- no_real_provider_call: `true`
- real_provider_call_enabled: `false`
- status: `non_evidence`
- reason: `local_llm_provider_adapter_wiring_only`
- output_text: `OK`
- behavior_evidence: `false`

## Bounded summary

The smoke result supports only that the merged optional local LLM runtime path executed one local loopback smoke and returned the recorded non-evidence result.
