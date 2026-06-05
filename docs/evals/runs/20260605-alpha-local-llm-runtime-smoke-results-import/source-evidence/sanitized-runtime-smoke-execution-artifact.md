# ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-001

## Source cleanup note

This repo-source artifact preserves the local LLM runtime smoke execution artifact from the operator-provided terminal output. Terminal wrapper output from `git pull`, branch listings, shell prompts, and command echo material outside the artifact preview was excluded from this source-evidence file.

The operator-provided preview recorded one worktree caveat: `?? ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-001.md`. That caveat is preserved below in the Git status snapshot. It appears to be an unrelated untracked prior smoke artifact at repo root and is not treated as part of this runtime smoke result.

This file is source evidence for future local LLM runtime smoke import, interpretation, final decision, and closeout lanes only. It is local LLM runtime smoke execution evidence only. It is not local model quality evidence, hosted provider evidence, `/v1/solve` readiness, dashboard preview readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, Alpha superiority evidence, or broad runtime readiness evidence.

## Execution metadata

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

## Git status snapshot

```text
## main...origin/main
?? ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-001.md
```

## Precheck result

- command: `python3 scripts/check_env.py`
- exit_code: `0`

### Precheck stdout

```text
Environment looks good. This validates configuration only; no remote provider API calls were made.
```

### Precheck stderr

```text

```

## Runtime smoke execution

- smoke_ran: `yes`
- smoke_exit_code: `0`

## Exact smoke command summary

```bash
MODEL_PROVIDER=local_llm \
ALPHA_LOCAL_LLM_ENABLED=true \
ALPHA_LOCAL_LLM_ENDPOINT=http://127.0.0.1:11434/api/chat \
ALPHA_LOCAL_LLM_MODEL=gemma3:4b \
ALPHA_LOCAL_LLM_TIMEOUT_SECONDS=120 \
python3 -c 'from alpha.local_llm.provider_adapter import run_configured_local_llm_runtime'
```

## Runtime smoke stdout

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

## Runtime smoke stderr

```text

```

## Artifact preservation notes

- Raw stdout and stderr were captured before this Markdown artifact was written.
- Endpoint is recorded only as localhost / loopback.
- Provider keys were unset before execution.
- No hosted provider endpoint or provider key is used by this smoke command.
- If precheck failed, smoke was not executed and the artifact records the stop condition.

## Evidence boundary

This artifact is local LLM runtime smoke execution evidence only.

It is not local model quality evidence, hosted provider evidence, `/v1/solve` readiness, dashboard preview readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, Alpha superiority evidence, or broad runtime readiness evidence.

## Non-claims

- No readiness claim is made.
- No quality claim is made.
- No benchmark claim is made.
- No production claim is made.
- No provider-orchestration claim is made.
- No Alpha-superiority claim is made.
