# Self Operator Local Run Harness Design Packet

Lane: `ALPHA-SOLVER-POST-LEVEL-7-SELF-OPERATOR-LOCAL-RUN-HARNESS-DESIGN-PACKET-001`

## Purpose

This packet defines a docs-only design for a future local-only Self Operator MVP run harness. It describes how that future harness should run local preflights, execute bounded tasks, capture artifacts, handle stop states, and avoid external actions.

## Required boundary

This packet is a design artifact only. It does not create a runner, execute tasks, run models, call providers, modify runtime behavior, expose dashboards, deploy services, control browsers, use credentials, create billing activity, or promote evidence.

The future harness design requires:

- no provider calls.
- no hosted model calls.
- no local model execution unless a later explicit local-only implementation lane authorizes it.
- no external API calls.
- no fallback.
- no credential use.
- no billing.
- no dashboard exposure.
- no `/v1/solve` exposure.
- No deployment.
- No browser control.
- No evidence promotion.
- Local-only filesystem artifact capture.
- The harness may only perform bounded local preflights, local artifact capture, and local docs/checker commands that are explicitly allowed by a future implementation lane.
- Explicit stop-state handling before, during, and after task execution.

## Packet files

- `source-evidence-reviewed.md` records the local source evidence reviewed for this docs-only design.
- `harness-overview.md` summarizes the proposed future harness shape.
- `preflight-requirements.md` defines preflight checks the future harness should perform.
- `local-only-execution-boundary.md` defines the execution sandbox and no-external-actions boundary.
- `artifact-capture-requirements.md` defines required local artifact capture.
- `stop-state-handling.md` defines stop states and expected harness responses.
- `forbidden-external-actions.md` enumerates actions the future harness must not perform.
- `non-actions.md` records work intentionally not done by this packet.
- `selected-next-action.md` records the required selected next action.
- `blocker-fallback-lane.md` records the required fallback lane.
- `checks-run.md` records validation checks for this docs-only packet.

## Decision state

Selected next action: `NO_FURTHER_SELF_OPERATOR_LOCAL_RUN_HARNESS_DESIGN_LANES_SELECTED`

Blocker fallback lane: `ALPHA-SOLVER-POST-LEVEL-7-SELF-OPERATOR-LOCAL-RUN-HARNESS-DESIGN-FIX-001`
