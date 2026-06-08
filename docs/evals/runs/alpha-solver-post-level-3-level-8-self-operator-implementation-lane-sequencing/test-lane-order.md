# Test lane order

## Test-first sequence

Future test work should be ordered as follows:

1. Static tests for forbidden external actions, hosted fallback prohibition, and local-only boundaries.
2. Static tests for artifact schema shape and redaction expectations.
3. Static tests for preflight stop-before-start behavior.
4. Static tests for operator confirmation capture requirements.
5. Static tests for stopped, blocked, failed, completed, and archived state transitions.
6. Focused local smoke tests only after scaffolds exist and static tests pass.
7. Acceptance execution packet only after local harness behavior is bounded and reviewable.

## Rationale

The earliest tests should be static and local because they can catch unsafe scope expansion before any future lane adds runtime behavior. Smoke and acceptance execution should remain later because they depend on schemas, preflights, confirmation capture, and stop-state behavior.

## Guardrail

No test lane should claim product readiness, evidence promotion, benchmark status, or autonomous Self Operator capability unless a later accepted packet explicitly authorizes those claims and provides evidence.
