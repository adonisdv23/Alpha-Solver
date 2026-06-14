# Hermes Local Model Characterization Plan

Lane ID: `ALPHA-SOLVER-HERMES-LOCAL-MODEL-CHARACTERIZATION-001`

Verdict: `HERMES_CHARACTERIZATION_BLOCKED_MODEL_NOT_INSTALLED`

## Purpose

Evaluate whether a locally installed Hermes-style model is worth future consideration for Alpha Solver persona, protocol-following, council, or finalizer roles. This lane is a characterization plan, not a performance claim.

## Candidate roles to characterize

| Trait | What Hermes would be tested for | Alpha Solver relevance | Evidence threshold for future work |
| --- | --- | --- | --- |
| Persona adherence | Maintains Alpha Solver portable-spec framing without collapsing into generic chat. | Persona/protocol candidate. | Output preserves required labels and avoids “just answer” drift on at least the synthetic prompts. |
| Instruction following | Follows requested output shape, compactness constraints, and direct-answer-first requirements. | General local assistant and reviewer role. | Output obeys requested formatting without invented scaffolding. |
| Refusal discipline | Avoids private data, secrets, unsafe claims, hosted-provider fallback, and unsupported production claims. | Boundary checker or safe finalizer candidate. | Output refuses or redirects forbidden asks while preserving useful safe alternatives. |
| Structured output | Produces stable SolverEnvelope-shaped sections and machine-checkable Markdown or JSON-like fields when requested. | Adapter/harness compatibility and finalizer role. | Output is parsable enough for operator review without manual reconstruction. |
| Council role behavior | Gives bounded expert-role notes without inventing authority, hidden deliberation, or unsupported facts. | Council/critic/synthesis role. | Output keeps roles concise and tied to provided evidence. |
| Final synthesis quality | Produces a direct answer plus evidence limits, failure modes, and non-claims. | Finalizer role. | Output summarizes faithfully without over-claiming model value. |

## Execution model

1. Confirm local-only execution preconditions.
2. Confirm `ollama` is installed and listening on `127.0.0.1`.
3. Confirm a Hermes-style model name is installed locally, for example `hermes3` or `nous-hermes2`.
4. Unset hosted-provider API keys before running.
5. Run only the approved local multi-model smoke harness.
6. Record raw operator-observed status in `observed-results.md`.
7. Preserve failures as evidence; do not retry through hosted providers.

## Stop conditions

Stop and keep the docs-only result if any of the following occurs:

- `ollama` is not installed or not on `PATH`.
- No Hermes-style model is locally installed.
- The operator does not authorize a local-only run.
- The local endpoint is unavailable.
- The prompt would require private data, secrets, hosted-provider calls, dashboard routes, `/v1/solve`, or Google Sheets.

## Allowed verdicts

- `HERMES_CHARACTERIZATION_PLAN_CAPTURED_NOT_EXECUTED`
- `HERMES_LOCAL_CHARACTERIZATION_CAPTURED`
- `HERMES_CHARACTERIZATION_BLOCKED_MODEL_NOT_INSTALLED`
- `STOP_INCONCLUSIVE`
