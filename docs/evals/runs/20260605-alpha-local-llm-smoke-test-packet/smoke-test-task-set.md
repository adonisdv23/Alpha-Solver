# Smoke-Test Task Set

This task set is a future placeholder for a default-skipped local smoke test. It is not an executed result and is blocked pending endpoint-locality hardening.

## Minimum future task

1. Confirm endpoint-locality hardening has been merged and reviewed.
2. Confirm the backend fails closed on non-loopback / non-local endpoint URLs before invoking any transport.
3. Build a local adapter request from the portable contract and one short operator-approved user prompt.
4. Send the request only to the operator-approved localhost endpoint.
5. Use the exact operator-supplied model name.
6. Apply a finite timeout.
7. Preserve raw request/response artifacts in the future execution lane.
8. Import only sanitized summaries after execution, if execution occurs.

## Prohibited task expansion

The future smoke task must not expand into runtime routing, public solve route, dashboard preview, hosted service fallback, benchmark, billing, Batch C, or provider-orchestration work.
