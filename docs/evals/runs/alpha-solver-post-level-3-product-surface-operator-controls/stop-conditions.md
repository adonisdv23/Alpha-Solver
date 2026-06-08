# Stop Conditions

## Stop-condition rule

Future product-surface work must define conditions that require pausing, disabling, rolling back, or escalating exposure. Stop conditions must be actionable by the operator and visible in audit records.

## Required stop conditions

Future work should stop or remain default-off when any of the following occurs:

- default-off behavior is not verified;
- explicit enablement is missing, stale, ambiguous, or broader than intended;
- a confirmation gate fails or is skipped without documented approval;
- role boundaries are unclear or combined without audit;
- audit capture is unavailable, incomplete, or unreviewable;
- a manual override lacks owner, scope, expiration, rollback, or audit fields;
- provider calls, model runs, benchmarks, billing actions, or evidence promotion are attempted outside approved scope;
- product-surface behavior implies unsupported production, superiority, benchmark, cost, provider, or readiness claims;
- user exposure exceeds the approved audience, environment, or time window;
- rollback cannot be executed promptly;
- unexpected cost, latency, privacy, reliability, or safety risk appears;
- Level 6 adoption authority is absent or contradicted.

## Stop-condition result

When a stop condition triggers, the safe posture is to disable or keep disabled the affected surface, preserve audit records, document the event, and route follow-up through an authorized lane.

## Adoption authority

Level 6 controls whether and how these stop conditions are adopted.
