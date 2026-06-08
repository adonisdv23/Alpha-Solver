# Implementation Readiness Gates

Before any Self Operator code changes may begin, a later accepted lane must explicitly satisfy all gates below.

## Required gates before code changes

1. An accepted implementation plan must name the exact future implementation lane.
2. The implementation plan must cite the approved files or modules that may change.
3. The implementation plan must define local-only behavior and stop conditions.
4. The implementation plan must preserve operator-supervised approval controls.
5. The implementation plan must preserve no provider calls, no browser control, no deployment, no billing, and no autonomous merge defaults.
6. The implementation plan must define acceptance tests before claiming MVP readiness.
7. The implementation plan must define evidence boundaries and blocked claims.
8. The implementation plan must define rollback or stop-state handling for failed local checks.
9. Reviewers must confirm that implementation scope is narrower than or equal to the allowed MVP scope.
10. Any runtime file changes must be blocked until the accepted implementation lane names them.

## Gate failure handling

If any gate cannot be satisfied, the project must use the blocker fallback lane instead of beginning implementation planning or code changes.
