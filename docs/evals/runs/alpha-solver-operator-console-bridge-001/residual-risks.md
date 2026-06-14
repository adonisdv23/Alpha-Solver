# Residual Risks

## Verdict

`OPERATOR_CONSOLE_BRIDGE_BLOCKED_SECURITY_DECISION_REQUIRED`

## Dependency risks

- API-shape compatibility unresolved.
- `/v1/solve` request mapping unresolved.
- OpenAI-compatible shim decision unresolved.
- Native sidecar request mapping unresolved.
- Response-envelope rendering unresolved.
- PR #546 sidecar feasibility context and PR #549 API-shape compatibility gate must remain preserved by later work.

## Security and boundary risks

- Direct provider/model bypass prevention unresolved.
- UI-originated CORS/CSRF unresolved.
- UI-originated telemetry identity unresolved.
- Retention/replay for UI sessions unresolved.
- RAG/private-file ingestion remains forbidden unless separately approved.
- A future bridge could accidentally expose a non-loopback interface.
- A future bridge could permit generic command execution instead of allowlisted operations.
- Logs could leak prompts, paths, tokens, or environment-derived secrets.
- Runtime entrypoint behavior could drift if bridge dispatch is not isolated.

## Mitigations for next work

- Select `ALPHA-SOLVER-OPERATOR-UI-SIDECAR-API-SHAPE-SECURITY-GATE-001` before any implementation lane.
- Require fail-closed tests before any bridge merge.
- Add explicit bind-address checks.
- Keep bridge operations narrow and read-only for the first later implementation candidate.
- Treat credential, CORS/CSRF, telemetry, retention, replay, and redaction tests as merge blockers.
