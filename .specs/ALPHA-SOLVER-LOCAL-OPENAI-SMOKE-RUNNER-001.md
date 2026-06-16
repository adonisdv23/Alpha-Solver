# ALPHA-SOLVER-LOCAL-OPENAI-SMOKE-RUNNER-001

## Objective

Add a practical operator smoke-runner lane that lets an operator explicitly run either one loopback-only local/Ollama smoke check or one gated OpenAI smoke check from the repository.

## Scope

- Add `tools/operator_smoke_runner.py`.
- Add operator documentation under `docs/evals/runs/alpha-solver-local-openai-smoke-runner-001/`.
- Add focused tests for argument parsing, loopback validation, OpenAI gating, no-secret output, and schema shape.
- Update source-of-truth docs to record the lane and selected next state.

## Required boundaries

- The runner must not run both modes by default.
- Local mode must require explicit local endpoint and local model env vars, reject non-loopback endpoints, reject hosted provider keys, use bounded timeout, and output sanitized JSON.
- OpenAI mode must require `MODEL_PROVIDER=openai`, `OPENAI_API_KEY`, and `ALPHA_LIVE_OPENAI=1`, use a bounded prompt and token count, and output sanitized JSON.
- No OpenAI live call or local model call is performed by this lane during repository validation.
- All results are smoke-only and are not quality, benchmark, readiness, production, public, or superiority evidence.

## Selected next state

`OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_SMOKE_RUNNER_001`

This state is review-only and does not authorize UI implementation unless the operator later provides smoke results.
