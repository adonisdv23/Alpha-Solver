# Failure and stop conditions

## Stop conditions before provider orchestration

Future provider orchestration must not start when:

- provider mode is not explicitly enabled by an approved future implementation lane;
- required timeout budgets are absent or invalid;
- required retry limits are absent or invalid;
- circuit-breaker state is open;
- circuit-breaker state cannot be evaluated safely;
- provider credentials are absent, invalid, or unsafe to use;
- budget guardrails reject the request;
- request shape is malformed or unsafe;
- safety policy blocks the request;
- operator policy has disabled the provider route.

## Stop conditions during attempts

A future implementation must stop attempts when:

- the overall request timeout would be exceeded;
- retry limits are exhausted;
- the circuit breaker opens;
- budget or cost guards are exceeded;
- a non-retryable provider error occurs;
- provider output is unsafe or cannot be normalized safely;
- required operator-visible status cannot be produced safely.

## Final fail-closed behavior

Fail-closed outcomes must be explicit and must not masquerade as successful model answers. Fail-closed status must be operator-visible through allowlisted fields and must not expose raw provider payloads or secrets.

## Evidence boundary

This failure-and-stop policy is docs-only. It does not implement runtime stop conditions, provider calls, provider fallback, retries, circuit breakers, timeout enforcement, billing, benchmarks, or evidence promotion.
