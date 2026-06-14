# Selected Next Lane

Selected next lane: `ALPHA-SOLVER-HERMES-LOCAL-OPERATOR-CHARACTERIZATION-RUN-002`

## Entry criteria

Proceed only if an operator separately authorizes a local-only run and confirms that a Hermes-style model is already installed locally.

## Fallback

If no local Hermes-style model is installed, keep this packet closed with verdict `HERMES_CHARACTERIZATION_BLOCKED_MODEL_NOT_INSTALLED` and do not substitute a hosted provider or unrelated model.

## Non-selection

No runtime routing, council assignment, finalizer assignment, `/v1/solve` exposure, dashboard exposure, hosted-provider run, Google Sheets update, or performance comparison lane is selected by this packet.
