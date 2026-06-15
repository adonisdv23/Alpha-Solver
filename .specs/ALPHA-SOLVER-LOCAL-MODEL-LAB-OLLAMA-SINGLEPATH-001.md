# ALPHA-SOLVER-LOCAL-MODEL-LAB-OLLAMA-SINGLEPATH-001 · Local Ollama Singlepath Lab Lane

## Purpose

Create a single-model, single-path local Ollama lab lane for a tiny controlled task subset. This lane is not multi-model routing, council work, benchmark work, provider fallback work, production exposure, or evidence-model promotion.

## Scope

This lane authorizes only documentation and local-only smoke scaffolding for an operator-run lab lane using exactly one local Ollama model name:

- `gemma3:4b`

The only approved endpoint is:

- `http://127.0.0.1:11434/api/chat`

The tiny controlled task subset must use synthetic prompts only. No private data, hosted provider calls, tokens, public API exposure, dashboard exposure, model pulls, model installs, model registry sweeps, scoring, routing readiness claims, benchmark claims, or Alpha superiority claims are authorized.

## Local-only prerequisites

Before any operator-run local smoke, the operator must confirm:

1. Ollama is already installed locally.
2. The exact local model `gemma3:4b` is already present locally.
3. The local loopback endpoint `http://127.0.0.1:11434/api/chat` is available.
4. No hosted provider credentials or tokens are set or required for this lane.
5. The prompt fixture is synthetic and contains no private or production data.
6. The run uses the operator-only local CLI path, not `/v1/solve`, dashboard, or any public API.
7. Smoke output is recorded only as local non-behavior/smoke evidence unless a separate approved scoring lane changes that status.

## Operator-run template

The operator-run template is maintained in:

- `docs/evals/runs/alpha-solver-local-model-lab-ollama-singlepath-001/operator-run-template.md`

The template must preserve the exact model name, exact loopback endpoint, explicit local opt-in, finite timeout, synthetic prompt source, and no-provider/no-token boundaries.

## Evidence packet

The evidence packet is maintained in:

- `docs/evals/runs/alpha-solver-local-model-lab-ollama-singlepath-001/evidence-packet.md`

The packet must record prerequisites, fixture identity, command, environment boundary, smoke status, and non-claims. It must not score model quality or compare Alpha against any baseline.

## Validation boundary

Repository validation for this lane is limited to fake-transport or local-only static/docs checks unless the operator explicitly authorizes a real local Ollama run. `git diff --check` is required.

## Non-claims

This lane does not claim local model quality, routing readiness, benchmark success, council behavior, model-selection quality, Alpha superiority, production readiness, MVP validation, `/v1/solve` readiness, dashboard readiness, hosted-provider behavior, or evidence-model promotion.

## Follow-on state

No follow-on lane is started by this packet.

`NO_FURTHER_LOCAL_MODEL_LAB_OLLAMA_SINGLEPATH_LANES_SELECTED`
