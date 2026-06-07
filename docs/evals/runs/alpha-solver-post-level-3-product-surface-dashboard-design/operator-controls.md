# Operator Controls

## Control posture

All future dashboard operator controls must be default-off. A dashboard page may display read-only evidence by default only after Level 6 authorizes the design and a later implementation lane creates the route or UI.

## Required default-off controls

Potential future controls must remain disabled until separately authorized:

- Refresh evidence snapshot.
- Run guardrail checks.
- Export audit summary.
- Acknowledge a claim boundary.
- Mark a packet as reviewed.
- Start a follow-on lane.

## Required confirmation pattern

If a future implementation adds any control, the control must require:

1. Explicit operator selection.
2. Display of the source artifact being acted on.
3. Display of the claim and evidence boundary.
4. Display of the non-actions that remain true.
5. A confirmation that the control does not expose dashboards beyond the authorized surface and does not expose `/v1/solve`.

## Forbidden control behavior in this design

This design does not create controls that call providers, run models, run benchmarks, perform billing work, mutate runtime configuration, expose dashboard routes, expose `/v1/solve`, or promote evidence.
