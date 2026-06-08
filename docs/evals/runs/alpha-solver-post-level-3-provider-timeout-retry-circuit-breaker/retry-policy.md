# Retry policy

## Policy intent

Future provider orchestration must use bounded retries only for retryable provider failures. Retries must be opt-in through the future implementation authority and must never create unbounded loops.

## Required future retry limits

Before implementation, a future lane must define:

- maximum attempts per provider request, including the first attempt;
- maximum retry count after the first failed attempt;
- retryable status or error categories;
- non-retryable status or error categories;
- backoff schedule and jitter rules, if any;
- retry budget interaction with request timeout and cost ceilings;
- stable operator-visible retry status fields;
- deterministic stop behavior when retry limits are exhausted.

## Required retry exclusions

A future implementation must not retry:

- authentication or authorization failures;
- malformed requests;
- policy or safety denials;
- budget-exceeded decisions;
- non-idempotent calls unless a future spec proves the request is safe to retry;
- provider responses that are already accepted as final;
- failures where retry would exceed the request timeout or cost budget.

## Cost and visibility requirements

Every attempted provider call must be accountable to operator-visible status and cost guardrails. Retry count must be visible as metadata or telemetry without exposing secrets, prompts, raw payloads, or raw exception strings.

## Evidence boundary

This retry policy is docs-only. It does not implement retries, backoff, jitter, provider calls, provider fallback, runtime changes, model inference, benchmarks, billing, or evidence promotion.
