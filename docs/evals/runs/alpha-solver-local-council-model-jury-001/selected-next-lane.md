# Selected Next Lane

Recommended next lane: `ALPHA-SOLVER-LOCAL-COUNCIL-FAKE-HARNESS-002`.

## Objective

Implement a minimal fake-model-only council harness that consumes deterministic role fixtures, emits the disagreement matrix, enforces finalizer non-claims, and returns a blocked or inconclusive verdict when required role fields are missing.

## Boundaries

The next lane should not run local model inference, call Ollama, call hosted providers, use tokens, expose or call `/v1/solve`, touch dashboards, run broad evals, update Google Sheets, or claim validation.

## Acceptance evidence

- Focused tests for missing role, echo output, unsupported finalizer claim, and strong disagreement escalation.
- Static docs check for non-claims and local-only boundaries.
- Evidence packet with fake harness output only.
