# Implementation sequence

## Named gate

Gate name: **Level 10 Static Safety Merge + GS Gate**.

Runtime-adjacent scaffolds must not start until the Level 10 static-test scaffold PR is merged and GS done.

## Ordered lanes

1. Finish and merge Level 10 static-test scaffold.
2. Artifact schema code scaffold.
3. Local preflight runner code scaffold.
4. Command classification guardrails.
5. Approval record code scaffold.
6. Stop-state code scaffold.
7. Local harness dry-run wrapper.
8. Acceptance packet prep.
9. Manual local acceptance run.
10. Acceptance results import.
11. Acceptance interpretation.
12. MVP runbook and closeout.

Any lane may be split if review scope becomes too broad, changed-file proof becomes hard to review, or deterministic test coverage would be clearer in a smaller PR.
