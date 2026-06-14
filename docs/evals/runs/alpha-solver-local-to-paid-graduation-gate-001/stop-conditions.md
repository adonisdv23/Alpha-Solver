# Stop conditions

Stop immediately and do not make or continue paid-provider calls if any condition below is true.

1. Operator authorization is missing, ambiguous, stale, or not tied to the exact provider/model/fixture/run.
2. The fixture contains secrets, credentials, private keys, billing details, sensitive personal data, proprietary customer data, or live user payloads.
3. Project/account boundary, model, cost cap, token cap, request cap, or max run count is missing.
4. Any cap is reached, cannot be measured, or conflicts across artifacts.
5. The provider returns an authentication, quota, billing, policy, safety, timeout, or malformed-response error.
6. The response echoes the prompt/system text instead of producing a bounded substantive smoke output.
7. The run would require exposing API, dashboard, `/v1/solve`, public routes, credentials, or deployment surfaces.
8. The run would require Google Sheets updates or external planning-ledger mutation.
9. The operator attempts to interpret smoke output as value, benchmark validation, Alpha superiority, public readiness, production readiness, or hosted-provider validation.
10. DEF-002/security/privacy blockers become relevant to the exact action and have not been explicitly resolved or risk-accepted for that action.
11. The action expands from a tiny smoke into a value experiment, benchmark, multi-user demo, or production-like workload.
12. Any evidence file cannot be preserved with redaction and boundary labels.

A stopped run should record `STOP_INCONCLUSIVE` unless the reason is the known missing operator authorization blocker, in which case the verdict should remain `LOCAL_TO_PAID_GATE_BLOCKED_OPERATOR_AUTHORIZATION_REQUIRED`.
