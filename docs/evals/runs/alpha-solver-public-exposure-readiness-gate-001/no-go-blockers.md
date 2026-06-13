# No-go blockers

Public exposure must not proceed while any of these blockers remain open.

1. DEF-002 is open and not closed by operator-approved evidence.
2. RR-02 plaintext provider-secret storage is not remediated or explicitly blocked by a no-persistence design.
3. RR-03 known/default dashboard/API credential semantics are not hardened.
4. RR-01 CORS defaults are not hardened and tested for public exposure.
5. RR-09 `/v1/solve` auth/tenancy decision is not closed with tests.
6. Public provider-cost caps, tenant quotas, kill switch, and alerting are not proven.
7. Dashboard route inventory and role boundary are not proven.
8. Provider data-sharing disclosure and operator/end-user acceptance are not captured.
9. Data classification registry/precedence is not reconciled.
10. Dependency lock/hash and vendored dependency provenance gaps remain open.
11. Rollback and incident-response minimums for public abuse, leaked keys, over-billing, and data exposure are absent.
12. Operator public-exposure approval has not been captured.

## Forbidden claims while blockers remain

Do not claim public readiness, production readiness, runtime readiness, provider readiness, dashboard readiness, `/v1/solve` readiness, security/privacy completion, DEF-002 closure, broad-user readiness, benchmark validation, or value evidence.
