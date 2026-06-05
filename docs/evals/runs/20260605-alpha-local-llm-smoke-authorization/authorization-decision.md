# Authorization Decision

## Decision record

- Direct smoke execution in this PR: **not authorized**.
- Live provider execution in this PR: **not authorized**.
- Hosted provider execution in this PR: **not authorized**.
- Local model execution in this PR: **not authorized**.
- Packet preparation for a future lane: **draft reference only**.
- Smoke progression: **blocked pending endpoint-locality hardening**.

## Selected corrective lane

`ALPHA-LOCAL-LLM-ENDPOINT-LOCALITY-HARDENING-001`

## Blocking condition

A later smoke lane must not run until the backend fails closed on non-loopback / non-local endpoint URLs before invoking any transport. Localhost or loopback endpoint validation must be implemented before smoke can be authorized.

The future hardening lane must add tests proving hosted URLs such as `https://example.com/api/chat` fail closed without transport invocation.
