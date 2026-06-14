# Bridge Design

## Verdict

`OPERATOR_CONSOLE_BRIDGE_BLOCKED_SECURITY_DECISION_REQUIRED`

## Goal

Define a narrow local bridge pattern that lets an operator console invoke approved Alpha Solver actions only after the sidecar API-shape/security gate resolves request mapping and security boundaries.

## Proposed bridge responsibilities

- expose a localhost-only control surface only after the required gate passes;
- validate operator requests before dispatch;
- translate approved requests into existing commands or functions;
- preserve deterministic inputs where required by existing specs;
- capture structured results for the console;
- redact secrets and sensitive paths from logs;
- return clear fail-closed errors when a request is outside the allowlist.

## API-shape and request-mapping dependency

- Current `/v1/solve` is not assumed OpenAI-compatible.
- Current `/v1/solve` requires Alpha Solver request shape, including `query`.
- Any console or UI bridge must not assume OpenAI-compatible chat/completions shape.
- A future bridge must define and test request mapping and response-envelope mapping before implementation.
- Direct sidecar-to-model, direct sidecar-to-provider, and direct sidecar-to-Ollama routing remain forbidden.
- The bridge must preserve Alpha Solver router, policy, SAFE-OUT, evidence, auth, tenancy, CORS/CSRF, cost, telemetry, retention, and replay boundaries.
- PR #546 sidecar feasibility context and PR #549 API-shape compatibility gate are required dependency state for this bridge lane.

## Non-goals

- no public web service;
- no hosted provider fallback;
- no new solver behavior;
- no background daemon requirement;
- no credential persistence;
- no changes to portable or modular entrypoint semantics;
- no bridge implementation before `ALPHA-SOLVER-OPERATOR-UI-SIDECAR-API-SHAPE-SECURITY-GATE-001` passes.

## Request lifecycle candidate after gate approval

1. Operator starts the bridge locally.
2. Bridge emits a short-lived local session token.
3. Console connects to loopback and presents the token.
4. Bridge validates origin, token, operation, and parameters.
5. Bridge applies the gate-approved request mapping.
6. Bridge dispatches only allowlisted local work through Alpha Solver boundaries.
7. Bridge returns a gate-approved response-envelope mapping with redaction applied.
8. Bridge exits or expires credentials according to operator-configured lifetime.

## Allowlist-first model

The bridge should start with no implicit command execution. Each operation must be added deliberately with tests and documentation after the selected gate lane resolves API-shape and security blockers.
