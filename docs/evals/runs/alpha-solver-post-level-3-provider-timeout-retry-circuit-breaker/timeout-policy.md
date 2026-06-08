# Timeout policy

## Policy intent

Future provider orchestration must use finite timeout budgets for every provider interaction. No provider call may wait indefinitely, and no retry sequence may exceed the request-level time budget selected by the future implementation authority.

## Required future budget layers

A future implementation must define all of the following before provider orchestration can be enabled:

1. **Per-call connect timeout**: maximum time allowed to establish the provider connection.
2. **Per-call read timeout**: maximum time allowed to wait for provider response bytes after connection.
3. **Per-call total timeout**: maximum wall-clock budget for a single provider attempt.
4. **Overall request timeout**: maximum wall-clock budget across all attempts, retry delay, safety checks, and final response shaping.
5. **Operator-visible timeout reason**: stable reason code when timeout causes a fail-closed result.

## Candidate constraints for later implementation

A future implementation should prefer conservative defaults:

- exact budgets must be explicit configuration, not implicit library defaults;
- lower environments may use shorter budgets than production-like controlled runs;
- retry delay must count against the overall request timeout;
- provider timeout errors must not be hidden as successful answers;
- timeout status must be observable without exposing prompts, raw provider payloads, headers, secrets, or stack traces.

## Fail-closed requirement

If any required timeout budget is missing, unbounded, non-numeric, or impossible to enforce, provider orchestration must remain disabled or fail closed. A timeout must not trigger hosted fallback, model substitution, or unbounded retry.

## Evidence boundary

This timeout policy is a design packet only. It does not implement timeout enforcement, runtime configuration, provider calls, provider fallback, retries, circuit-breaker logic, or billing behavior.
