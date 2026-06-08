# Prompt 07 — Local Harness Wrapper

```text
HARD STOP: Stop unless Level 8 is accepted, implementation planning is selected, and a spec authorizes a local Self Operator harness wrapper.

Implement only a local harness wrapper for approved Self Operator MVP behavior. Do not call providers, use credentials, automate browsers, deploy, bill, expose /v1/solve, expose dashboards, or promote evidence.

Tasks:
1. Wrap only approved local components behind explicit preflight, approval, artifact, and stop-state gates.
2. Default to dry-run or no-op where the spec requires uncertainty handling.
3. Write artifacts only to approved local paths.
4. Add tests proving forbidden external modes fail closed.
5. Run focused local tests and static checks.

Stop if the wrapper would run hosted models, use secrets, control browsers, deploy, create billing risk, expose /v1/solve or dashboard surfaces, or promote artifacts as evidence.
```
