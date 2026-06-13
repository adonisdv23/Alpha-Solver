# Free-token usage plan

This is a future-use plan only. No API call is authorized or performed here.

## Safe later usage controls

- Use a dedicated OpenAI project for Alpha Solver smoke/eval work.
- Use a minimal model suitable for tiny synthetic smoke prompts.
- Use a minimal token budget per request.
- Cap daily usage before any real request.
- Record request IDs if available.
- Record exact prompts and sanitized outputs.
- Record request timestamp and model/project boundary.
- Stop if billing starts unexpectedly.
- Stop if response includes sensitive data.
- Stop if provider behavior differs from the expected smoke boundary.

## Evidence capture

A future authorized smoke lane should capture sanitized request/response evidence in a dedicated packet and should not mix provider evidence with local-only Self Operator evidence.

## Remaining non-claims

This planning/scaffold packet does not claim OpenAI validation, provider validation, hosted validation, runtime readiness, public MVP readiness, production readiness, security/privacy completion, benchmark validation, benchmark superiority, broad-user readiness, autonomous readiness, `/v1/solve` readiness, or dashboard readiness.
