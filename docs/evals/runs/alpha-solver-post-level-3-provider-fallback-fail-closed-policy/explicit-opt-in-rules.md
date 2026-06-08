# Explicit Opt-In Rules

## Operator opt-in requirement

Future fallback requires explicit opt-in before any fallback behavior can be considered. Opt-in must be affirmative, scoped, reviewable, and revocable. Silence, default configuration, stale approval, inherited approval, environment drift, provider failure, or runtime convenience must not count as opt-in.

## Required opt-in scope

A future operator opt-in must identify:

- the operator or reviewer role authorizing fallback;
- the run, request class, or bounded operating window;
- the allowed source provider or local path;
- the allowed fallback provider or provider class;
- whether hosted fallback remains forbidden or is narrowly allowed;
- billing scope and spend limits, if any;
- retention, redaction, and audit requirements;
- stop conditions and revocation conditions;
- the evidence boundary for outputs and failures.

## Opt-in invalidation

Opt-in is invalid when any scoped condition changes materially, when policy state is stale, when audit capture is unavailable, when billing scope is unresolved, when safety state is blocked, when the request is outside the authorized window, or when Level 7 has not controlled use of this packet.
