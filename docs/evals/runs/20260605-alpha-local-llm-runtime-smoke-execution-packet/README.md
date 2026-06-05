# Alpha Local LLM Runtime Smoke Execution Packet

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-PACKET-001`

This directory is a docs-only final manual runtime smoke execution packet for the optional local LLM runtime path. Runtime smoke is not executed in this PR. This packet is not runtime smoke evidence and must not be imported or cited as a completed local runtime result.

Runtime smoke remains blocked until `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-REVIEW-GATE-001` explicitly authorizes smoke execution.

## Source material

- Canonical implementation contract: `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md`
- Merged implementation surface: `alpha/local_llm/provider_adapter.py`
- Environment examples and precheck behavior: `.env.example` and `scripts/check_env.py`
- Provider config validation: `service/config/validators.py`
- Prior implementation packet: `docs/evals/runs/20260605-alpha-local-llm-runtime-integration-implementation/`
- Prior operator runbook: `docs/evals/runs/20260605-alpha-local-llm-runtime-operator-config-runbook/`
- Prior smoke scaffold: `docs/evals/runs/20260605-alpha-local-llm-runtime-smoke-packet-scaffold/`

## Required packet files

1. `README.md`
2. `smoke-execution-packet-summary.md`
3. `prerequisite-gates.md`
4. `operator-runbook.md`
5. `local-runtime-smoke-command.md`
6. `raw-artifact-capture-template.md`
7. `sanitized-artifact-template.md`
8. `expected-result-fields.md`
9. `failure-classification.md`
10. `redaction-rules.md`
11. `post-execution-import-instructions.md`
12. `evidence-boundary.md`
13. `smoke-packet-preservation-checklist.md`
14. `selected-next-lane.md`

## Implementation-aware configuration fields

The packet uses the merged implementation fields below. Actual values must be confirmed by the operator at execution time.

- `MODEL_PROVIDER=local_llm`
- `ALPHA_LOCAL_LLM_ENABLED=true`
- `ALPHA_LOCAL_LLM_ENDPOINT=<localhost-or-loopback-http-endpoint>`
- `ALPHA_LOCAL_LLM_MODEL=<exact-local-model-name>`
- `ALPHA_LOCAL_LLM_TIMEOUT_SECONDS=<finite-positive-number>`

Historical operator-local examples only:

- Endpoint pattern: `http://127.0.0.1:11434/api/chat`
- Model: `gemma3:4b`
- Timeout: `120`

These examples are not automatic execution values.

## Evidence boundary

This PR prepares a manual runtime smoke execution packet only. It is not runtime smoke execution, runtime smoke evidence, local model quality evidence, hosted provider evidence, `/v1/solve` readiness, dashboard preview readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, or Alpha superiority evidence.
