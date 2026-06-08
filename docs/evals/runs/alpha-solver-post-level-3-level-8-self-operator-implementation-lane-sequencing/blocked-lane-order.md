# Blocked lane order

## Blocked until prerequisites exist

The following future work remains blocked until all earlier prerequisites in the recommended order are accepted:

- Local harness wrapper work is blocked until static tests, artifact schema scaffold, preflight scaffold, confirmation capture, and stop-state handling exist.
- Acceptance execution is blocked until the local harness wrapper is implemented in a bounded, local-only form and focused checks pass.
- Operator runbook closeout is blocked until acceptance evidence is reviewed and accepted.
- Provider-aware behavior is blocked from this lane sequence and would require a separate authorization path.
- Dashboard, `/v1/solve`, deployment, credentials, billing, hosted fallback, browser automation, and external actions are blocked from this sequence.

## Blocked by ambiguity

Any future lane should stop before implementation if it cannot identify:

- the accepted source packet it implements;
- the exact files it is allowed to modify;
- the focused tests it must add or update;
- the local-only evidence boundary;
- the stop condition for unclear or missing operator approval.
