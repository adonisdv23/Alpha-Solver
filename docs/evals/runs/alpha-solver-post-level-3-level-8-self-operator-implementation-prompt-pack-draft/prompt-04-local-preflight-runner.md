# Prompt 04 — Local Preflight Runner

```text
HARD STOP: Stop unless Level 8 is accepted, implementation planning is selected, and a spec authorizes a local-only preflight runner.

Implement a local preflight runner for Self Operator MVP readiness gates. Do not call providers, use credentials, automate a browser, deploy, bill, expose /v1/solve, expose dashboards, or promote evidence.

Tasks:
1. Inspect the approved spec, CLI conventions, and existing local orchestration guardrails.
2. Implement only deterministic local checks for approval presence, branch/worktree state, artifact directory safety, forbidden external modes, and stop-state prerequisites.
3. Make the runner fail closed with clear operator-visible messages.
4. Add focused tests for pass, fail, and ambiguous states.
5. Run focused local checks.

Stop if preflight requires network access, secrets, provider configuration, browser sessions, deployments, billing accounts, API-route exposure, dashboard exposure, or evidence promotion.
```
