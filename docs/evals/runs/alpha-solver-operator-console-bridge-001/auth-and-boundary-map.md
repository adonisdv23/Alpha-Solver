# Authentication and Boundary Map

## Verdict

`OPERATOR_CONSOLE_BRIDGE_BLOCKED_SECURITY_DECISION_REQUIRED`

## Actors

- **Local operator**: a human using the console on a trusted workstation.
- **Operator console**: a future UI or CLI surface that requests local bridge actions after the gate passes.
- **Local bridge**: a future localhost-only adapter that may translate console requests into approved Alpha Solver commands after request mapping is resolved.
- **Alpha Solver runtime**: existing solver entrypoints and supporting scripts.

## Dependency state

PR #546 sidecar feasibility packet exists. PR #549 API-shape compatibility gate exists. Current `/v1/solve` is not assumed OpenAI-compatible and requires Alpha Solver's request shape, including `query`.

## Boundary status table

| Boundary | Status now | Required gate decision |
| --- | --- | --- |
| Clean-room replacement for PR #547 | Resolved in this packet | Preserve no-copy, no-cherry-pick, no-repair boundary. |
| Documentation-only packet scope | Resolved in this packet | Keep changes limited to packet documentation. |
| API-shape/request mapping | Blocked pending gate | Decide and test mapping into `/v1/solve` with required `query`. |
| Response envelope mapping | Blocked pending gate | Define response-envelope mapping for console rendering. |
| Sidecar-to-model bypass prevention | Blocked pending gate | Prove direct sidecar-to-model and sidecar-to-Ollama routing stay forbidden. |
| Sidecar-to-provider bypass prevention | Blocked pending gate | Prove hosted provider calls cannot bypass Alpha Solver controls. |
| CORS/CSRF | Blocked pending gate | Define UI-origin controls and fail-closed tests. |
| Telemetry/audit identity | Blocked pending gate | Define operator/session identity propagation and audit rules. |
| Retention/replay | Blocked pending gate | Define UI session retention and replay boundaries. |
| Token handling | Blocked pending gate | Define short-lived local credentials without repo persistence. |
| Auth and tenancy | Blocked pending gate | Preserve existing auth and tenancy boundaries for any UI-originated request. |
| Cost and policy controls | Blocked pending gate | Preserve policy, SAFE-OUT, cost, and evidence boundaries. |

## Boundary principles

1. The bridge should bind to loopback only by default after the selected gate passes.
2. The bridge should fail closed when authentication or origin checks are not satisfied.
3. The bridge should not accept remote network traffic unless a later spec explicitly authorizes it.
4. The bridge should not embed long-lived secrets in repo files, logs, docs, or examples.
5. The console should request only allowlisted operations with bounded inputs.

## Authentication shape candidate

A future implementation should prefer short-lived local session credentials or an explicit operator start token. The token should be generated at bridge startup, displayed only to the local operator, and never persisted by default.

## Authorization shape candidate

Authorization should be command-scoped. Each callable bridge operation should declare:

- operation name;
- accepted parameters;
- validation rules;
- side-effect class;
- expected output envelope;
- redaction requirements;
- stop conditions.

## Evidence boundary

This file is a design map only. It does not prove that current code enforces these controls.
