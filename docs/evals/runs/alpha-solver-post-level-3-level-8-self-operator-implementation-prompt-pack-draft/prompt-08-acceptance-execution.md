# Prompt 08 — Acceptance Execution

```text
HARD STOP: Stop unless Level 8 is accepted, implementation planning is selected, implementation lanes have completed, and a spec defines local acceptance criteria.

Run only local acceptance checks for Self Operator MVP. Do not call providers, use credentials, automate browsers, deploy, bill, expose /v1/solve, expose dashboards, or promote evidence.

Tasks:
1. Confirm changed files match the approved implementation scope.
2. Run focused unit/static checks and the approved local acceptance command set.
3. Confirm no provider calls, credentials, browser automation, deployment, billing, route exposure, dashboard exposure, or evidence promotion occurred.
4. Record pass/fail results, residual caveats, and blocked claims.
5. Return acceptance evidence as local check output only.

Stop if acceptance requires live services, secrets, browser automation, deployment, billing, /v1/solve, dashboards, or evidence promotion.
```
