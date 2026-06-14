# Routing Evidence Plan

## Preconditions before execution

1. Local smoke must pass for each candidate model with `behavior_evidence=false` retained.
2. Operator must explicitly authorize local model runs.
3. Inputs must be synthetic or approved non-private data.
4. Endpoint must be loopback-only and hosted-provider keys must be absent.
5. The task bank, labels, pass/fail/unknown criteria, and stop conditions must be frozen before model calls.

## Minimum artifact fields per route decision

- task id and category;
- selected route or role;
- rejected routes or roles;
- reason selected;
- evidence used by the router;
- evidence missing;
- uncertainty level;
- stop condition checked;
- human escalation trigger checked;
- what must not be claimed;
- model id and digest when available;
- endpoint shape, timeout, and host resource class;
- raw output or normalized output artifact;
- failure reason code when blocked;
- statement that no hosted provider or token was used.

## Pass/fail/unknown criteria for future experiments

`PASS` may be recorded only for a narrow routing experiment when all of the following are true: local smoke passed first, all task-bank examples were synthetic/non-private, every route row includes selected and rejected routes with reasons, expected route labels match the frozen answer key within the preregistered tolerance, every uncertainty and stop condition is recorded, and no forbidden claim appears in outputs.

`FAIL` should be recorded when routing executes but materially violates the frozen route key or boundaries, omits rejected-route rationale, claims success without evidence, uses hosted providers, exposes private data, or continues after a stop condition.

`UNKNOWN` or `STOP_INCONCLUSIVE` should be recorded when local model availability, connection, timeout, ambiguous labels, missing artifacts, or insufficient operator authorization prevents interpretation.

## Evidence hierarchy

1. Static documentation capture: this packet only.
2. Fake-transport smoke: harness wiring, not behavior evidence.
3. Real local smoke: model availability and non-echo sanity only, not quality evidence.
4. Synthetic routing execution: narrow routing evidence only if preregistered and logged.
5. Value experiment: separate protocol; routing evidence alone cannot support value or superiority claims.
