# Operator Instructions

These instructions apply only if a later lane explicitly authorizes smoke execution.

1. Confirm the future execution lane ID and operator approval are recorded.
2. Confirm the endpoint is localhost-only and uses a loopback host pattern.
3. Supply the exact local model name in the future lane record.
4. Supply a finite timeout.
5. Confirm the smoke test remains default-skipped without the opt-in flag.
6. Confirm no provider access material or access material are present.
7. Confirm no hosted fallback is configured.
8. Run only the approved smoke command for the approved lane.
9. Preserve raw artifacts before summarizing results.
10. Import only sanitized results into repository docs.
11. Do not make readiness, quality, comparison, benchmark, billing, production, or orchestration claims.

If any condition fails, stop before execution and record the blocker in the future lane.
