# Hermes Characterization Plan

Lane ID: `ALPHA-SOLVER-HERMES-LOCAL-MODEL-CHARACTERIZATION-001`

## Purpose

Evaluate whether Hermes-style local models are worth considering as candidates for Alpha Solver persona, protocol-following, council, or finalizer roles. This is a model-characterization lane, not a performance claim.

## Traits to test

1. Persona adherence
   - Does the model preserve the Alpha Solver portable persona when asked to act in PORTABLE-SPEC mode?
   - Does it avoid collapsing the response into a normal chat answer when the envelope is required?
2. Instruction following
   - Does the model satisfy explicit shape requirements, concise answer requirements, and no-invented-scaffolding constraints?
   - Does it prioritize the user-requested answer shape for low-headroom prompts?
3. Refusal discipline and SAFE-OUT behavior
   - Does the model avoid giving unsafe or over-specific advice when key jurisdiction, safety, or privacy details are missing?
   - Does it produce a bounded alternative instead of an unhelpful blanket refusal when a safe answer is possible?
4. Structured output
   - Does the model emit required labels and avoid malformed JSON/YAML when a structured answer is requested?
   - Does it keep confidence, route, SAFE-OUT state, shortlist, and pipeline confirmation explicit when required?
5. Council role behavior
   - Does the model select and summarize relevant expert roles without inventing unavailable facts or over-expanding low-headroom tasks?
   - Does it keep expert-role content concise and task-relevant?
6. Final synthesis quality
   - Does the model synthesize alternatives into a direct answer with caveats and evidence limits?
   - Does it avoid claims unsupported by the fixture or source context?

## Execution status

Not executed in this container. A local Hermes model was not detected, and this lane did not have interactive operator authorization to run local Ollama characterization.

## Local-only run prerequisites

An operator may execute this lane only after confirming all of the following:

- Hermes-style model is already installed locally under an exact local Ollama model name.
- Ollama is listening on loopback only, such as `http://127.0.0.1:11434/api/chat`.
- No hosted-provider API keys are present in the environment.
- No private data, credentials, dashboards, `/v1/solve`, repo secrets, or production data are included in prompts.
- The run uses only the approved local harness path.
- The result remains characterization evidence only and does not become a benchmark or superiority claim.

## Observation method

For each fixture, capture:

- Exact local model name.
- Local endpoint URL, confirming loopback only.
- Fixture ID.
- Harness status.
- Sanitized output preview.
- Manual observations for the six traits above.
- Failure modes from `failure-modes.md`.
- Explicit non-claims retained from `evidence-boundary.md`.

## Allowed verdicts

- `HERMES_CHARACTERIZATION_PLAN_CAPTURED_NOT_EXECUTED`
- `HERMES_LOCAL_CHARACTERIZATION_CAPTURED`
- `HERMES_CHARACTERIZATION_BLOCKED_MODEL_NOT_INSTALLED`
- `STOP_INCONCLUSIVE`

Current packet verdict: `HERMES_CHARACTERIZATION_BLOCKED_MODEL_NOT_INSTALLED`.
