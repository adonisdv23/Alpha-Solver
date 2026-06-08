# Prompt 05 — Approval Capture

```text
HARD STOP: Stop unless Level 8 is accepted, implementation planning is selected, and a spec authorizes local approval-capture behavior.

Implement local approval capture for Self Operator MVP. Do not call providers, use credentials, automate browsers, deploy, bill, expose /v1/solve, expose dashboards, or promote evidence.

Tasks:
1. Define and implement a local approval record format consistent with the approved schema.
2. Require explicit operator approval metadata before any future Self Operator action can proceed.
3. Ensure approvals cannot imply provider permission, deployment permission, billing permission, route exposure, dashboard exposure, or evidence promotion unless a separate future authorization exists.
4. Add tests for missing, expired, mismatched, and valid approvals.
5. Run focused local tests.

Stop if approval capture would collect secrets, grant external-service permission, or bypass Level 8/spec gates.
```
