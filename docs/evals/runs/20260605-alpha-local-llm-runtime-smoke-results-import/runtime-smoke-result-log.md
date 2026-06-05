# Runtime Smoke Result Log

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-RESULTS-IMPORT-001`

## Source evidence

- Source artifact path: `docs/evals/runs/20260605-alpha-local-llm-runtime-smoke-execution/source-evidence/ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-001.md`
- Imported artifact path: `source-evidence/sanitized-runtime-smoke-execution-artifact.md`
- Import source restriction: repo-source artifact only.

## Execution metadata imported exactly

- lane_id: `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-001`
- start_time_utc: `2026-06-05T20:48:47Z`
- end_time_utc: `2026-06-05T20:49:55Z`
- repo_path: `<repo-root>`
- git_head: `87a52c8f5d6d9707840fac292d43c99c450d9616`
- provider_mode: `local_llm`
- alpha_local_llm_enabled: `true`
- endpoint_public_summary: `localhost-or-loopback-http endpoint`
- endpoint_pattern_used: `http://127.0.0.1:11434/api/chat`
- model: `gemma3:4b`
- timeout_seconds: `120`
- provider_keys_unset_before_execution: `OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, GEMINI_API_KEY, DEEPSEEK_API_KEY`

## Git status caveat imported exactly

```text
## main...origin/main
?? ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-001.md
```

Interpretation boundary for this caveat: the repo-source artifact says it appears to be an unrelated untracked prior smoke artifact at repo root and is not treated as part of this runtime smoke result. This import preserves the caveat and does not treat it as invalidating the bounded runtime smoke result.

## Precheck result imported exactly

- command: `python3 scripts/check_env.py`
- exit_code: `0`

### Precheck stdout imported exactly

```text
Environment looks good. This validates configuration only; no remote provider API calls were made.
```

### Precheck stderr imported exactly

```text

```

## Runtime smoke execution result imported exactly

- smoke_ran: `yes`
- smoke_exit_code: `0`

## Local runtime configuration imported exactly

- provider_mode: `local_llm`
- ALPHA_LOCAL_LLM_ENABLED=true
- endpoint summary: localhost / loopback HTTP endpoint
- endpoint_pattern_used: `http://127.0.0.1:11434/api/chat`
- model: `gemma3:4b`
- timeout_seconds: `120`

## Exact smoke command summary imported from source artifact

```bash
MODEL_PROVIDER=local_llm \
ALPHA_LOCAL_LLM_ENABLED=true \
ALPHA_LOCAL_LLM_ENDPOINT=http://127.0.0.1:11434/api/chat \
ALPHA_LOCAL_LLM_MODEL=gemma3:4b \
ALPHA_LOCAL_LLM_TIMEOUT_SECONDS=120 \
python3 -c 'from alpha.local_llm.provider_adapter import run_configured_local_llm_runtime'
```

## Runtime smoke stdout imported exactly

```json
{
  "behavior_evidence": false,
  "metadata": {
    "backend_class": "ollama-local-http-runtime",
    "behavior_evidence": false,
    "endpoint_host_label": "loopback",
    "endpoint_is_loopback": true,
    "evidence_label": "non_evidence_local_llm_provider_adapter_wiring",
    "local_backend": "ollama_chat",
    "local_model": "gemma3:4b",
    "model": "gemma3:4b",
    "no_hosted_fallback": true,
    "no_provider_keys_required": true,
    "no_real_provider_call": true,
    "prompt_source_fingerprint": "98841febea17e2ea4d0155df63537bcb76f948e51395bddc1ce870b349d3c7bb",
    "prompt_source_fingerprint_algorithm": "sha256",
    "prompt_source_path": "alpha_solver_portable.py",
    "prompt_source_sha256": "98841febea17e2ea4d0155df63537bcb76f948e51395bddc1ce870b349d3c7bb",
    "provider_mode": "local_llm",
    "real_provider_call_enabled": false,
    "timeout_seconds": 120.0
  },
  "output_text": "OK",
  "reason": "local_llm_provider_adapter_wiring_only",
  "status": "non_evidence"
}
```

## Runtime smoke stderr imported exactly

```text

```

## Smoke output fields imported exactly

- status: `non_evidence`
- reason: `local_llm_provider_adapter_wiring_only`
- output_text: `OK`
- behavior_evidence: `false`

## Runtime metadata fields imported exactly

- backend_class: `ollama-local-http-runtime`
- endpoint_host_label: `loopback`
- endpoint_is_loopback: `true`
- local_backend: `ollama_chat`
- local_model: `gemma3:4b`
- no_hosted_fallback: `true`
- no_provider_keys_required: `true`
- no_real_provider_call: `true`
- provider_mode: `local_llm`
- real_provider_call_enabled: `false`
- timeout_seconds: `120.0`

## Prompt source fingerprint metadata imported exactly

- prompt_source_fingerprint: `98841febea17e2ea4d0155df63537bcb76f948e51395bddc1ce870b349d3c7bb`
- prompt_source_fingerprint_algorithm: `sha256`
- prompt_source_path: `alpha_solver_portable.py`
- prompt_source_sha256: `98841febea17e2ea4d0155df63537bcb76f948e51395bddc1ce870b349d3c7bb`

## Evidence boundary

This imported result is local LLM runtime smoke execution evidence only. It is not local model quality evidence, hosted provider evidence, `/v1/solve` readiness, dashboard preview readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, Alpha superiority evidence, broad runtime readiness evidence, billing evidence, or evidence-model promotion.
