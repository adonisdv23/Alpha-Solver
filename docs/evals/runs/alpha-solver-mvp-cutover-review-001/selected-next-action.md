# Selected next action

Recommended next action: operator performs manual review of the local MVP candidate using `manual-review-plan.md`.

The operator should start with route preview only, verify that preview metadata is visible and execution flags are false, verify prompt-too-long fail-closed behavior, verify sanitized JSON copy scope, and stop if sensitive content appears.

The operator should not execute the routed-vs-plain pilot, run scoring, unblind, inspect raw Alpha/baseline outputs, expose `/v1/solve`, expose dashboard/public API behavior, deploy, add dependencies, mutate Google Sheets, or claim production/public/benchmark/provider/local-model/tool/security/privacy/autonomous readiness or Alpha superiority.
