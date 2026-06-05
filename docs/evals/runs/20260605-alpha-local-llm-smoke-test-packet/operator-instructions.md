# Operator Instructions

These instructions apply only if a later lane explicitly authorizes smoke execution after endpoint-locality hardening is merged and reviewed.

1. Confirm `ALPHA-LOCAL-LLM-ENDPOINT-LOCALITY-HARDENING-001` or its approved successor has been merged and reviewed.
2. Confirm tests prove hosted URLs such as `https://example.com/api/chat` fail closed without transport invocation.
3. Confirm the future execution lane ID and operator approval are recorded.
4. Confirm the endpoint is localhost-only and uses a loopback host pattern.
5. Supply the exact local model name in the future lane record.
6. Supply a finite timeout.
7. Confirm the smoke test remains default-skipped without the opt-in flag.
8. Confirm no provider access material are present.
9. Confirm no hosted fallback is configured.
10. Run only the approved smoke command for the approved lane.
11. Preserve raw artifacts before summarizing results.
12. Import only sanitized results into repository docs.
13. Do not make readiness, quality, comparison, benchmark, billing, production, or orchestration claims.

If any condition fails, stop before execution and record the blocker in the future lane.
