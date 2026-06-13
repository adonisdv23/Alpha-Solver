# Issue register summary

Full register (fields + evidence paths): [`docs/ISSUE_REGISTER.md`](../../../ISSUE_REGISTER.md).

| id | sev | title | status | smoke | public |
|----|-----|-------|--------|-------|--------|
| ISS-001 | P2 | Spec contamination (systemic, 22 specs) | CONFIRMED | No | No |
| ISS-002 | P3 | Stale roadmap | CONFIRMED | No | No |
| ISS-003 | P2 | CORS default `*` + credentials | CONFIRMED | No | Yes |
| ISS-004 | P2 | Plaintext file secrets | CONFIRMED | No | Yes |
| ISS-005 | P3 | Provider telemetry prompt content | PARTIALLY_CONFIRMED (default-safe) | No | Review |
| ISS-006 | P2 | Commit-signing test hermeticity | CONFIRMED | No | No |
| ISS-007 | P3 | Hardcoded pricing | PARTIALLY_CONFIRMED | No | No |
| ISS-008 | P2 | Duplicate provider/adapter surfaces | CONFIRMED | No | No |
| ISS-009 | P2 | Sanitizer Unicode normalization gap | CONFIRMED | No | Yes |
| ISS-010 | P3 | Orphan / duplicate MVP docs | PARTIALLY_CONFIRMED | No | No |
| ISS-011 | Info | Stale branches/refs | CONFIRMED | No | No |
| ISS-012 | P2 | alpha/service stack overlap | CONFIRMED | No | No |
| ISS-013 | P3 | Backlog/lane status drift | CONFIRMED | No | No |
| ISS-014 | Info | Checker coverage gaps after #508 | PARTIALLY_CONFIRMED | No | No |
| ISS-015 | P1 | OpenAI project/billing blocker | CONFIRMED | **Yes** | n/a |

Only ISS-015 (P1) blocks the current objective. Security items (P2) matter
before public exposure but not for a narrow synthetic smoke. No issue asserts a
forbidden claim; unverified items are not overstated.
