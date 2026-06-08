# Prompt 06 — Stop-State Handling

```text
HARD STOP: Stop unless Level 8 is accepted, implementation planning is selected, and a spec authorizes local stop-state handling.

Implement local fail-closed stop-state handling for Self Operator MVP. Do not call providers, use credentials, automate browsers, deploy, bill, expose /v1/solve, expose dashboards, or promote evidence.

Tasks:
1. Implement approved stop-state enums, records, or validators.
2. Cover missing evidence, missing approval, unclear task, provider/fallback ambiguity, credential risk, branch pollution, forbidden route/dashboard exposure, and evidence-promotion attempts.
3. Ensure stopped runs cannot continue without new approval.
4. Preserve local artifact/provenance boundaries for stopped runs.
5. Add focused tests and run them locally.

Stop if any requested stop behavior would continue execution, retry externally, deploy, bill, expose routes, expose dashboards, or promote evidence.
```
