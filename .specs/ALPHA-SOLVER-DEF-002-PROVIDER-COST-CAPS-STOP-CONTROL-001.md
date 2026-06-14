# ALPHA-SOLVER-DEF-002-PROVIDER-COST-CAPS-STOP-CONTROL-001

Provider-backed operator-enabled execution paths must fail closed unless explicit operator caps bound cost, input tokens, output tokens, and request count before provider execution.

## Requirements

- Hosted provider execution must remain opt-in and must not run when required caps are absent, malformed, or non-positive.
- Provider requests must not execute when an operator emergency stop flag is active.
- Provider result telemetry must be checked against configured cost and token caps before success accounting is emitted.
- Tests for this lane must use fake provider adapters only and must not call hosted providers or consume credentials.

## Evidence

See `docs/evals/runs/alpha-solver-def-002-provider-cost-caps-stop-control-001/`.
