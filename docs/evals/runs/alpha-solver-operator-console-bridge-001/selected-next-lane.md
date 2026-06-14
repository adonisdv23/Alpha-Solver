# Selected Next Lane

## Verdict

`OPERATOR_CONSOLE_BRIDGE_BLOCKED_SECURITY_DECISION_REQUIRED`

## Selected next lane

`ALPHA-SOLVER-OPERATOR-UI-SIDECAR-API-SHAPE-SECURITY-GATE-001`

The operator console bridge must not move directly into implementation. The selected next lane is the sidecar API-shape/security gate because PR #546 establishes sidecar feasibility context and PR #549 establishes that API-shape compatibility must be gated before a console or UI bridge can safely map requests.

## Future implementation candidate

`ALPHA-SOLVER-OPERATOR-CONSOLE-BRIDGE-LOCAL-ONLY-IMPLEMENTATION-001`

This lane is only a future implementation candidate after the selected sidecar API-shape/security gate passes. It is not selected now.

## Gate exit requirements before implementation selection

- Decide whether the console path uses an OpenAI-compatible shim or native sidecar request mapping.
- Define and test `/v1/solve` request mapping for Alpha Solver's required `query` field.
- Define and test response-envelope mapping for console rendering.
- Prove the sidecar cannot bypass Alpha Solver router, policy, SAFE-OUT, evidence, auth, tenancy, CORS/CSRF, cost, telemetry, retention, or replay boundaries.
- Confirm direct sidecar-to-model, direct sidecar-to-provider, and direct sidecar-to-Ollama routing remain forbidden.
