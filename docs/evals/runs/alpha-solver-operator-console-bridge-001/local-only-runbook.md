# Local-Only Runbook

## Verdict

`OPERATOR_CONSOLE_BRIDGE_BLOCKED_SECURITY_DECISION_REQUIRED`

This runbook is for a later implementation candidate only after `ALPHA-SOLVER-OPERATOR-UI-SIDECAR-API-SHAPE-SECURITY-GATE-001` passes. It is not evidence that a bridge exists today, and it does not authorize implementation before the API-shape/security gate.

## Preconditions after gate approval

- PR #546 sidecar feasibility context and PR #549 API-shape compatibility gate dependency state are preserved.
- Workstation is trusted by the operator.
- Repository checkout is clean and on the intended branch.
- Bridge implementation has an explicit spec and tests.
- `/v1/solve` request mapping includes Alpha Solver's required `query` field.
- Response-envelope mapping is defined and tested.
- No remote exposure has been enabled.

## Future smoke flow after gate approval

1. Start the bridge with loopback binding only.
2. Confirm the bind address is `127.0.0.1` or equivalent local-only loopback.
3. Capture the short-lived startup token from the local terminal.
4. Connect the operator console from the same host.
5. Submit one allowlisted read-only request through the gate-approved request mapping.
6. Verify non-allowlisted requests fail closed.
7. Verify missing or invalid credentials fail closed.
8. Verify direct sidecar-to-model, sidecar-to-provider, and sidecar-to-Ollama routing fail closed.
9. Stop the bridge and confirm credentials expire.

## Required future artifacts

- command transcript with secrets redacted;
- bridge bind-address evidence;
- API-shape and request mapping evidence;
- response-envelope mapping evidence;
- allowlist pass/fail evidence;
- credential failure evidence;
- CORS/CSRF evidence;
- telemetry/audit identity evidence;
- retention/replay evidence;
- stop-condition evidence.
