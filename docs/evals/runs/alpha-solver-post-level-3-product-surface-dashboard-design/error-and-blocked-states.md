# Error and Blocked States

## Required blocked states

A future dashboard must block display or action when:

- The source packet is missing.
- The source packet has no evidence boundary or equivalent non-actions file.
- The source packet has contradictory selected-next state.
- The selected next action and blocker fallback lane are missing.
- A claim would imply dashboard readiness, `/v1/solve` readiness, production readiness, MVP readiness, benchmark evidence, provider readiness, billing readiness, local model quality evidence, Alpha superiority, or evidence promotion without an accepted source.
- Level 6 has not authorized use of this design for implementation.

## Required error states

A future dashboard must distinguish:

- `SOURCE_NOT_FOUND`: source artifact cannot be resolved.
- `BOUNDARY_MISSING`: evidence boundary or non-actions are absent.
- `CONTRADICTORY_STATE`: selected-next state conflicts with no-further-lanes state.
- `UNSUPPORTED_CLAIM`: display text would exceed accepted evidence.
- `IMPLEMENTATION_NOT_AUTHORIZED`: a route, UI, or control is requested before release gates are met.
- `RUNTIME_ACTION_BLOCKED`: requested action would call providers, run models, expose `/v1/solve`, expose dashboards, run benchmarks, perform billing work, or promote evidence.

## Operator-facing language

Blocked states must use plain language. Example: "This dashboard cannot display a readiness claim because the source artifact does not establish readiness evidence."

## Non-action boundary

Defining blocked states does not build blocked-state UI. This packet does not create dashboard routes, UI components, API behavior, provider calls, model runs, benchmark runs, billing behavior, `/v1/solve` exposure, or evidence promotion.
