# Prompt 03 — Artifact Schema Code

```text
HARD STOP: Stop unless Level 8 is accepted, implementation planning is selected, and a spec authorizes local Self Operator artifact schema code.

Implement only local artifact schema code for Self Operator MVP artifacts. Do not implement provider execution, browser automation, deployment, billing, /v1/solve exposure, dashboard exposure, or evidence promotion.

Tasks:
1. Re-read the approved artifact schema spec and prior artifact persistence packet.
2. Add or update local schema/dataclass/validation code only in the approved file set.
3. Preserve raw-evidence versus reviewer-authored interpretation boundaries.
4. Ensure credential fields are prohibited or redacted by schema rules.
5. Add focused local tests for valid artifacts, missing approvals, stop states, and forbidden fields.
6. Run focused tests and static checks.

Stop if the implementation would store secrets, call a provider, run a model, mutate source evidence, or claim evidence promotion.
```
