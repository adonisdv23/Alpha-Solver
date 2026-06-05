# Smoke Retry Result Summary

## Source evidence

`docs/evals/runs/20260605-alpha-local-llm-runtime-smoke-execution-retry/source-evidence/ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-RETRY-002.md`

## Summary

- Attempt 001 failed before runtime due missing repo-root `PYTHONPATH`; it is preserved as runner/import-path context, not as a local LLM runtime failure.
- Attempt 002 corrected repo-root `PYTHONPATH` and preserved exact executable command and Python script provenance.
- Precheck command `PYTHONPATH="<repo-root>" python3 scripts/check_env.py` exited `0`.
- Runtime smoke ran: `yes`.
- Runtime smoke exit code: `0`.
- Endpoint: localhost / loopback, `http://127.0.0.1:11434/api/chat`.
- Model: `gemma3:4b`.
- Timeout: `120` seconds.
- Result: `status: non_evidence`, `reason: local_llm_provider_adapter_wiring_only`, `output_text: OK`, `behavior_evidence: false`.
- Hosted provider separation: `no_hosted_fallback: true`, `no_provider_keys_required: true`, `no_real_provider_call: true`, `real_provider_call_enabled: false`.

## Bounded closeout statement

The smoke retry result supports closing the local LLM runtime track only; it does not support broader claims or authorize future exposure/promotion lanes.
