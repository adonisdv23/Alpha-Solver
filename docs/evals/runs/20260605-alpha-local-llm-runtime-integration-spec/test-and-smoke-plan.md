# Test and Smoke Plan

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-SPEC-001`

This file defines required future tests and smoke checks. No tests are added by this lane.

## Required offline tests for future implementation

A future implementation must add or update focused tests proving:

1. local LLM mode is default-off;
2. explicit operator opt-in is required;
3. local LLM mode requires no provider keys;
4. localhost and loopback endpoints are accepted;
5. non-local endpoints fail closed;
6. malformed endpoints fail closed;
7. invalid timeout values fail closed;
8. connection failure fails closed;
9. timeout fails closed;
10. malformed response fails closed;
11. empty output fails closed;
12. prompt echo fails closed;
13. system echo fails closed;
14. hosted-provider fallback does not occur from local LLM mode;
15. observability labels local LLM output separately from hosted provider output;
16. `behavior_evidence=false` is preserved.

## Required runtime smoke before future runtime-readiness claim

Before any future runtime-readiness claim, a separate implementation or smoke lane must run a local LLM runtime smoke with:

- explicit local LLM provider selection;
- localhost or loopback endpoint;
- finite timeout;
- no provider keys;
- raw and sanitized artifacts;
- status and reason preservation;
- proof that hosted-provider fallback did not occur.

## Blocked smoke claims

A smoke result may show only the bounded facts it records. It must not be treated as local model quality evidence, hosted provider evidence, `/v1/solve` readiness, dashboard readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, or Alpha superiority evidence.
