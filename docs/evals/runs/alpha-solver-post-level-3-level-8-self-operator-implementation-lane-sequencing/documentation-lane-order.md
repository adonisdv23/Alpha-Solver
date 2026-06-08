# Documentation lane order

## Documentation sequence

Future documentation updates should trail the implementation risk they describe:

1. Implementation plan packet before code changes.
2. Inline docs or developer notes with static test scaffold only if needed to explain test scope.
3. Schema documentation with artifact schema scaffold.
4. Preflight documentation with preflight runner scaffold.
5. Confirmation wording documentation with operator confirmation capture.
6. Stop-state documentation with stop-state handling.
7. Harness usage notes with local harness wrapper.
8. Acceptance execution packet after execution evidence exists.
9. Operator runbook closeout after all acceptance and boundary evidence has been reviewed.

## Rationale

Operator-facing documentation should not imply runnable capability before the corresponding future lane is implemented, tested, and accepted. Runbook closeout belongs last because it summarizes validated behavior rather than authorizing it.

## Required boundary language

Each future documentation lane should state whether it is docs-only, test-only, scaffold-only, local-only, or acceptance-only, and should explicitly list non-actions.
