# Local Ollama singlepath run artifact - 2026-06-15

## Verdict

`LOCAL_OLLAMA_SINGLEPATH_BLOCKED_TIMEOUT`

## TLDR

The exact `gemma3:4b` model preflight passed, but the local smoke did not produce a local model answer because the local CLI failed closed with a timeout/backend error.

## Evidence boundary

This artifact records local-only operator evidence for the operator-authorized local Ollama singlepath attempt. It is not Value Read evidence, not benchmark evidence, not runtime readiness evidence, not provider evidence, not local model quality evidence, and not Alpha superiority evidence.

This artifact supports only the bounded facts listed below. It does not claim local model quality, Value Read success, provider validation, public readiness, production readiness, benchmark success, runtime readiness, or Alpha superiority.

## Raw terminal output

The operator-provided terminal output is preserved verbatim below.

```text
$ python3 --version
Python 3.13.5
$ tmpbin="$(mktemp -d)"
$ ln -s "$(command -v python3)" "$tmpbin/python"
$ PATH="$tmpbin:$PATH" which python
/var/folders/operator/tmp/tmp.ollama-singlepath-python/python
$ PATH="$tmpbin:$PATH" python --version
Python 3.13.5
$ PATH="$tmpbin:$PATH" bash scripts/run_local_ollama_singlepath_operator.sh
=== ALPHA SOLVER LOCAL OLLAMA SINGLEPATH OPERATOR HELPER ===
Evidence boundary: operator-local smoke helper only.
Run this only on the same local machine where Ollama is already installed and serving http://127.0.0.1:11434/api/chat.
This script does not run ollama pull, install models, call hosted providers, use provider tokens, access credentials, expose /v1/solve, expose dashboard/public API behavior, mutate Google Sheets, sweep registries, use fallback models, or substitute model tags.
Exact required first-column ollama model tag: gemma3:4b

=== LOCAL OLLAMA SINGLEPATH OPERATOR RESULT ===
preflight exact model check result: PRESENT_EXACT_MODEL_gemma3:4b
command exit status: 1
raw stdout:
{
  "answer": "",
  "assumptions": [],
  "behavior_evidence": false,
  "confidence": null,
  "considerations": [],
  "evidence_boundary": "non-production local solver orchestration only; not runtime smoke execution, local model quality evidence, hosted provider evidence, /v1/solve readiness, dashboard readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, Alpha superiority evidence, evidence-model promotion, or broad runtime readiness evidence",
  "final_answer": "",
  "metadata": {
    "adapter_exception_cause_class": "timeout",
    "backend_class": "ollama-local-http-runtime",
    "behavior_evidence": false,
    "endpoint_is_loopback": true,
    "failure_label": "failed_closed_result",
    "local_model": "gemma3:4b",
    "no_hosted_fallback": true,
    "no_provider_keys_required": true,
    "provider_mode": "local_llm",
    "real_provider_call_enabled": false,
    "reason": "backend_error_non_evidence",
    "status": "failed_closed",
    "timeout_seconds": 30.0
  },
  "mode": "block",
  "no_hosted_fallback": true,
  "no_provider_keys_required": true,
  "orchestration_mode": "non_production_local_solver_orchestration",
  "pass_count": 1,
  "provider_mode": "local_llm",
  "status": "failed_closed",
  "strategy": "local_expert_two_pass"
}
raw stderr if available:
<empty>
operator verdict: BLOCKED_LOCAL_LAB_ENDPOINT_UNREACHABLE
non-claims:
  - no local model quality claim
  - no Value Read success claim
  - no hosted provider validation claim
  - no production readiness claim
  - no public readiness claim
  - no benchmark success claim
  - no runtime readiness claim
  - no Alpha superiority claim
  - no /v1/solve, dashboard, public API, Google Sheets, provider-token, model-pull, model-install, registry-sweep, fallback-model, or tag-substitution claim
$ echo "script exit: $?"
script exit: 1
```

## Extracted facts

- model boundary: `gemma3:4b`
- endpoint boundary: `http://127.0.0.1:11434/api/chat`
- preflight result: exact model present
- command result: failed closed
- failure class: timeout/backend error
- operator verdict: `BLOCKED_LOCAL_LAB_ENDPOINT_UNREACHABLE`
- final artifact verdict: `LOCAL_OLLAMA_SINGLEPATH_BLOCKED_TIMEOUT`

Additional bounded facts from the packet and operator interpretation:

- The operator ran the local helper on a Mac-local repo checkout.
- The exact model preflight found `gemma3:4b`.
- The script used the loopback endpoint boundary `http://127.0.0.1:11434/api/chat`.
- The helper did not call hosted providers.
- The helper did not use provider tokens.
- The helper did not use `/v1/solve`.
- The helper did not expose dashboard or public API behavior.
- The helper did not mutate Google Sheets.
- The helper did not pull, install, substitute, benchmark, route, sweep registries, or use fallback models.
- The local CLI path failed closed with a timeout/backend error.
- No local model answer was generated.
- No local model quality evidence was created.

## What this proves

Only the following bounded facts are supported:

- exact-model local preflight passed
- local helper script could reach the local CLI path
- local execution failed closed under the committed timeout boundary
- the packet did not silently fall back to hosted providers

## What this does not prove

This artifact does not prove:

- local model quality
- Value Read success
- false-premise behavior
- hidden-constraint behavior
- no-echo behavior
- confidence behavior
- provider validation
- runtime readiness
- public readiness
- production readiness
- benchmark success
- Alpha superiority

## Recommended next action

Return to the selected main lane: `ALPHA-SOLVER-VALUE-READ-EXECUTION-PACKET-AUTHORIZATION-001`.

Extending timeout, changing the model, pulling models, installing models, or rerunning with altered behavior would require a separate explicit operator-authorized lane.
