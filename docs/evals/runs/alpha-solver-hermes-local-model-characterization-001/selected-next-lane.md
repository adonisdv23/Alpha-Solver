# Selected Next Lane

Selected next lane: `ALPHA-SOLVER-HERMES-OPERATOR-LOCAL-RUN-001`

## Rationale

The current lane captured the Hermes characterization plan and synthetic fixtures but did not execute because a Hermes-style local model was not installed or observable in this environment. The next lane should be an operator-run lane on a machine with Ollama and an explicitly installed Hermes-style model.

## Entry criteria

- Operator confirms local-only authorization.
- `ollama list` shows a Hermes-style model such as `hermes3` or `nous-hermes2`.
- Hosted-provider API keys are unset for the shell session.
- The operator uses the approved local multi-model smoke harness.

## Exit criteria

- One or more prompt fixture outputs are captured in `observed-results.md`.
- Failure modes and non-claims remain explicit.
- Verdict is either `HERMES_LOCAL_CHARACTERIZATION_CAPTURED` or `STOP_INCONCLUSIVE`.
