# Merge Blockers

## Blocker for smoke progression

Endpoint-locality fail-closed enforcement is missing for the injected transport path. A later injected transport could receive any `endpoint_url`, including a non-local hosted URL such as `https://example.com/api/chat`, before the backend rejects the endpoint.

A later smoke lane must not run until the backend fails closed on non-loopback / non-local endpoint URLs before invoking any transport.

The future hardening lane must add tests proving hosted URLs such as `https://example.com/api/chat` fail closed without transport invocation.

Localhost or loopback endpoint validation must be implemented before smoke can be authorized.

## Conditions that would block this docs-only PR if introduced

- Any implementation code change.
- Any test code change.
- Any live local or hosted provider call.
- Any provider access material, private endpoint, or nonpublic URL.
- Any runtime routing, public solve route, dashboard preview, operator evidence, Batch C, benchmark, billing, or provider-orchestration work.
- Any claim upgrade beyond offline/non-evidence labels.

## Current status

The lane remains documentation-only and does not mutate prior evidence. Smoke progression is blocked pending `ALPHA-LOCAL-LLM-ENDPOINT-LOCALITY-HARDENING-001`.
