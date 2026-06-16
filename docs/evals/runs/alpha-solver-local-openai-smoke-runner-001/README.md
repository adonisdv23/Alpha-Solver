# ALPHA-SOLVER-LOCAL-OPENAI-SMOKE-RUNNER-001

## Objective

Create a practical operator smoke-runner lane that lets the Operator explicitly run one local/Ollama smoke check or one OpenAI smoke check from the repo with strict evidence boundaries.

## Files added or changed

- `tools/operator_smoke_runner.py`
- `tests/test_operator_smoke_runner.py`
- `.specs/ALPHA-SOLVER-LOCAL-OPENAI-SMOKE-RUNNER-001.md`
- `.specs/INDEX.md`
- `docs/evals/runs/alpha-solver-local-openai-smoke-runner-001/`
- `docs/CURRENT_STATE.md`
- `docs/LANE_REGISTRY.md`
- `docs/EVIDENCE_INDEX.md`

## How local mode works

Local mode is selected with `--mode local`. It requires `ALPHA_LOCAL_LLM_ENABLED=1`, a loopback `ALPHA_LOCAL_LLM_ENDPOINT`, a concrete `ALPHA_LOCAL_LLM_MODEL`, and `ALPHA_LOCAL_LLM_TIMEOUT_SECONDS`. The runner rejects non-loopback endpoints, rejects hosted provider key environment variables, uses the existing local/Ollama adapter path, applies a bounded timeout, and prints sanitized JSON only.

## How OpenAI mode works

OpenAI mode is selected with `--mode openai`. It requires `MODEL_PROVIDER=openai`, a non-empty `OPENAI_API_KEY`, and explicit `ALPHA_LIVE_OPENAI=1` opt-in. The runner uses a bounded prompt, a bounded token count, the existing OpenAI provider client, and sanitized JSON output.

## Evidence boundary

Runner output is smoke evidence only. It is not quality evidence, benchmark evidence, readiness evidence, production evidence, public evidence, security/privacy completion evidence, provider validation, local-model validation, or Alpha-superiority evidence.

## Non-actions

This lane does not run OpenAI in Codex, run local models in Codex, pull local models, install local models, expose `/v1/solve`, build UI, mutate Google Sheets, generate scores, inspect prior raw outputs, unblind, perform source-map work, add broad dependencies, or implement release behavior.

## Non-claims

This lane does not claim provider quality, local model quality, benchmark success, readiness, production readiness, public readiness, buyer validation, traction, security/privacy completion, partnership/Pi.dev integration, or Alpha superiority.

## Selected next state after merge

`OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_SMOKE_RUNNER_001`

This state is review-only. It does not authorize UI implementation unless the Operator later provides reviewed smoke results.
