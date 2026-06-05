# ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-RETRY-002

## Source cleanup note

This repo-source artifact preserves the successful second manual local LLM runtime smoke retry attempt from the operator-provided terminal output. Terminal wrapper material outside the artifact preview was excluded.

Attempt 001 is preserved as context in the retry reason: the prior retry attempt failed before runtime execution because the executable script did not include repo-root `PYTHONPATH`, causing `ModuleNotFoundError: No module named 'alpha'`. This attempt added repo root to `PYTHONPATH` and reached the local runtime smoke path.

This file is source evidence for future local LLM runtime smoke retry import, interpretation, final decision, and closeout lanes only. It is local LLM runtime smoke execution retry evidence only. It is not local model quality evidence, hosted provider evidence, `/v1/solve` readiness, dashboard preview readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, Alpha superiority evidence, broad runtime readiness evidence, billing evidence, or evidence-model promotion.

## Execution metadata

- lane_id: `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-RETRY-001`
- attempt_id: `002`
- retry_reason: `prior smoke artifact had incomplete exact executable command provenance; attempt 001 failed before runtime due missing repo-root PYTHONPATH`
- start_time_utc: `2026-06-05T22:23:52Z`
- end_time_utc: `2026-06-05T22:24:40Z`
- repo_path: `<repo-root>`
- git_head: `4513eead8e640ae152b03219696546a343724067`
- provider_mode: `local_llm`
- alpha_local_llm_enabled: `true`
- endpoint_public_summary: `localhost-or-loopback-http endpoint`
- endpoint_pattern_used: `http://127.0.0.1:11434/api/chat`
- model: `gemma3:4b`
- timeout_seconds: `120`
- pythonpath_repo_root_set: `yes`
- provider_keys_unset_before_execution: `OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, GEMINI_API_KEY, DEEPSEEK_API_KEY`

## Repo status before retry artifacts

```text
## main...origin/main
?? ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-001.md
?? docs/evals/runs/20260605-alpha-local-llm-runtime-smoke-execution-retry/
?? docs/evals/runs/20260605-alpha-local-llm-runtime-smoke-execution/manual-artifacts/
```

## Precondition check

- required_retry_lane_doc: `docs/evals/runs/20260605-alpha-local-llm-runtime-final-decision/selected-next-lane.md`
- required_retry_lane_present: `yes`

## Precheck result

- command: `PYTHONPATH="<repo-root>" python3 scripts/check_env.py`
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

## Exact executable shell command

This is the exact command form used from the repo root after exporting the local LLM environment variables listed above.

```bash
PYTHONPATH="<repo-root>" python3 "docs/evals/runs/20260605-alpha-local-llm-runtime-smoke-execution-retry/manual-artifacts-attempt-002/runtime_smoke_retry_executable.py"
```

## Exact Python script executed

```python
import json
import os
import sys

from alpha.local_llm.provider_adapter import run_configured_local_llm_runtime

USER_PROMPT = "Reply with exactly OK."

result = run_configured_local_llm_runtime(USER_PROMPT, env=os.environ)

record = {
    "status": result.status,
    "reason": result.reason,
    "behavior_evidence": result.behavior_evidence,
    "output_text": result.output_text,
    "metadata": dict(result.metadata),
}

print(json.dumps(record, sort_keys=True, indent=2))

if result.status == "failed_closed":
    sys.exit(2)

sys.exit(0)
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

## Repo status after retry artifacts

```text
## main...origin/main
?? ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-001.md
?? docs/evals/runs/20260605-alpha-local-llm-runtime-smoke-execution-retry/
?? docs/evals/runs/20260605-alpha-local-llm-runtime-smoke-execution/manual-artifacts/
```

## Artifact preservation notes

- Exact executable shell command is preserved.
- Exact Python script executed is preserved.
- Repo root was added to PYTHONPATH before precheck and runtime smoke execution.
- The script calls `run_configured_local_llm_runtime` with a user prompt.
- The script serializes the returned result to JSON.
- Raw precheck stdout and stderr were preserved.
- Raw runtime smoke stdout and stderr were preserved.
- Provider keys were unset before execution.
- Endpoint is recorded only as localhost / loopback.
- No hosted provider endpoint or provider key is used by this smoke command.
- If precheck failed, smoke was not executed and the artifact records the stop condition.

## Evidence boundary

This artifact is local LLM runtime smoke execution retry evidence only.

It is not local model quality evidence, hosted provider evidence, `/v1/solve` readiness, dashboard preview readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, Alpha superiority evidence, broad runtime readiness evidence, billing evidence, or evidence-model promotion.

## Non-claims

- No readiness claim is made.
- No quality claim is made.
- No benchmark claim is made.
- No production claim is made.
- No provider-orchestration claim is made.
- No Alpha-superiority claim is made.
