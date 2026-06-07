# Quick Start

## Minimal local prerequisites

- A local developer machine.
- A local loopback Ollama-style endpoint such as `http://127.0.0.1:11434/api/chat` if an operator intentionally performs a local-only run.
- A local model identifier available to that local runtime.
- No hosted provider keys configured or supplied for this path.
- An explicit finite positive timeout.

## Approved command identity

```text
python -m alpha.local_llm.operator_cli
```

The wrapper is local-only, operator-only, non-production, default-off, explicit opt-in, loopback-only, finite-timeout, no hosted provider keys required, no hosted fallback, and no provider fallback.

## Minimal safe command shape

Template only; run only on the local developer machine where the intended local runtime is installed:

```bash
python -m alpha.local_llm.operator_cli \
  --enable-local-llm \
  --prompt "List three bounded local-only considerations." \
  --endpoint-url "http://127.0.0.1:11434/api/chat" \
  --model "qwen2.5:3b" \
  --timeout-seconds "60"
```

## High-level sequence

1. Read [operator-safe-use-checklist.md](operator-safe-use-checklist.md).
2. Confirm the Level 3 final accepted decision remains `LEVEL_3_VALIDATION_EXECUTION_ACCEPTED_AS_ARTIFACT_COMPLETE_NON_PROMOTIONAL_LOCAL_ORCHESTRATION_EVIDENCE`.
3. Confirm the closeout selected next action remains `NO_FURTHER_LEVEL_3_VALIDATION_LANES_SELECTED`.
4. Confirm any local endpoint is loopback/local and no hosted provider keys are needed or supplied.
5. Run only the approved local-only wrapper if a local operator run is intentionally needed; do not run it as validation, smoke, or benchmark evidence.
6. Inspect result fields: `status`, `mode`, `answer`, `final_answer`, `considerations`, `assumptions`, `confidence`, `metadata`, `metadata.gate_trace`, `behavior_evidence=false`, `no_hosted_fallback=true`, and `no_provider_keys_required=true`.
7. Stop on missing stdout JSON, nonzero exit code, malformed JSON, non-loopback endpoint, hosted key exposure, missing artifact fields, hosted fallback, provider fallback, `/v1/solve` exposure, or dashboard exposure.

## Evidence boundary

Do not treat any output as production readiness, MVP readiness, benchmark evidence, local model quality evidence, provider-orchestration evidence, Alpha superiority, billing evidence, dashboard readiness, `/v1/solve` readiness, broad runtime readiness, or evidence-model promotion.

This quick start does not reopen validation and does not authorize local model inference for validation, Ollama execution for validation, smoke reruns, hosted provider calls, `/v1/solve`, dashboard routes, provider fallback, hosted fallback, benchmarks, billing claims, Google Sheets updates, backlog workbook updates, or evidence promotion.

Post-closeout operator-docs consolidation selected next action: `NO_FURTHER_OPERATOR_DOCS_CONSOLIDATION_LANES_SELECTED`. Blocker fallback lane: `ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-POST-LEVEL-3-OPERATOR-DOCS-CONSOLIDATION-FIX-001`.
