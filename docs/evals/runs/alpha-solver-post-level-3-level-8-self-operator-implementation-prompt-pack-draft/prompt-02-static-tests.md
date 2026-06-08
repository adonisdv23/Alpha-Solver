# Prompt 02 — Static Tests

```text
HARD STOP: Stop unless Level 8 is accepted, implementation planning is selected, and a spec-backed Self Operator MVP test scope is approved.

Implement only local static tests for the approved Self Operator MVP scope. Do not implement runtime behavior in this lane. Do not call providers, use credentials, automate a browser, deploy, bill, expose /v1/solve, expose dashboards, or promote evidence.

Tasks:
1. Inspect the approved spec and implementation plan.
2. Add or update focused local tests that fail before implementation and do not require network access.
3. Cover hard-stop gates: missing Level 8 acceptance, missing approval, provider-call prohibition, credential prohibition, browser/deployment/billing prohibition, route/dashboard exposure prohibition, and evidence-promotion prohibition.
4. Run the most focused test command and static checks practical for the touched files.
5. Return changed files and exact checks.

Stop if tests would require live services, secrets, browser automation, route exposure, dashboard exposure, or evidence promotion.
```
