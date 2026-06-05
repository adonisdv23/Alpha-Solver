# Smoke Preconditions

A future execution lane must require all of the following before any local smoke command is run:

- Endpoint-locality hardening has been implemented and reviewed.
- Backend fails closed on non-loopback / non-local endpoint URLs before invoking any transport.
- Tests prove hosted URLs such as `https://example.com/api/chat` fail closed without transport invocation.
- Explicit operator approval naming the execution lane.
- Localhost-only endpoint using a loopback host pattern.
- Exact model name supplied by the operator in the future execution lane.
- Finite timeout supplied by the operator or the future execution spec.
- Default-skipped smoke test path.
- Explicit opt-in flag or command for the default-skipped smoke test.
- No provider access material.
- No hosted provider fallback.
- No readiness or quality claims.
- Raw artifact preservation.
- Sanitized result import if the future smoke is executed.
- Clear rollback or disablement instructions.

If any precondition is absent, the smoke test must remain unexecuted.
