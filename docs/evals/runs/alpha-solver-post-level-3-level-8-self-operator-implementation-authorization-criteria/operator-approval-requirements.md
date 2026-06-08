# Operator Approval Requirements

Self Operator runtime code must not be modified until a human operator explicitly approves the future implementation lane.

## Required approvals

The operator approval record must state:

- the exact future implementation lane being approved;
- the allowed file or module scope;
- the forbidden scope that remains out of bounds;
- that execution is local-only;
- that execution is operator-supervised;
- that provider calls are forbidden;
- that browser automation is forbidden;
- that credentials are forbidden;
- that deployment is forbidden;
- that billing is forbidden;
- that autonomous merges are forbidden;
- that `/v1/solve` and dashboard exposure are forbidden;
- that evidence promotion is forbidden;
- that static tests are required;
- that local harness tests are required;
- that artifact capture is required.

## Approval timing

Approval must happen before runtime code is edited. Retroactive approval is not sufficient.

## Approval failure rule

If approval is missing, ambiguous, stale, broader than this packet allows, or inconsistent with these criteria, runtime code must not be modified and the blocker fallback lane must be used.
