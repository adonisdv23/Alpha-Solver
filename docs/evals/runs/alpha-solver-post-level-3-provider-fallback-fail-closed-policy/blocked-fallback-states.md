# Blocked Fallback States

Fallback is forbidden in these states unless a later Level 7-controlled packet supersedes this list with narrower accepted rules:

- local-only mode is required;
- no-network mode is required;
- no-hosted-fallback defaults apply;
- explicit opt-in is absent, stale, ambiguous, revoked, or out of scope;
- provider identity, endpoint locality, or hosted/local status is unknown;
- billing policy, spend cap, account ownership, or payment authorization is unresolved;
- secrets, credentials, tokens, or sensitive payloads would be exposed;
- audit logging, decision logging, retention policy, or redaction policy is unavailable;
- safety policy blocks the request or requires human review;
- evidence boundary forbids provider calls, model runs, benchmarks, product-readiness claims, provider-readiness claims, billing work, or evidence promotion;
- runtime, provider, API, dashboard, CLI, checker, test, Makefile, CI, or source-artifact changes are out of scope;
- fallback would expose `/v1/solve` or alter API/dashboard behavior;
- fallback would hide, rewrite, or downgrade a failure that should remain visible to reviewers.

When any blocked fallback state is present, the safe outcome is blocked or fail-closed, not retry, hosted fallback, model execution, provider call, benchmark execution, billing work, or evidence promotion.
