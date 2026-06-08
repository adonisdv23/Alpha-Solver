# Operator-visible status

## Policy intent

Operators must be able to determine whether provider orchestration is disabled, timed out, retry-exhausted, circuit-open, budget-blocked, or fail-closed without seeing secrets or raw provider payloads.

## Required future status fields

A future implementation must define stable, allowlisted status fields for:

- provider identifier;
- model identifier;
- route or mode;
- timeout budget selected;
- attempt count;
- retry count;
- retry-exhausted status;
- circuit-breaker state;
- circuit-breaker reason;
- budget status;
- fail-closed reason;
- final operator-visible outcome.

## Redaction and allowlist rules

Operator-visible status must not include API keys, authorization headers, bearer tokens, raw prompts, raw system prompts, raw request bodies, raw provider response bodies, tracebacks, raw exception strings, raw metadata dumps, environment dumps, billing account identifiers, or secret-bearing config values.

The future implementation must build status records from an explicit allowlist rather than capturing broad objects and redacting after the fact.

## Evidence boundary

This status policy is docs-only. It does not add telemetry, logs, dashboards, API fields, CLI output, runtime calls, provider calls, retries, circuit breakers, billing, or evidence promotion.
