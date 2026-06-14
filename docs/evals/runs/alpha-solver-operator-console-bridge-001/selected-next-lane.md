# Selected Next Lane

## Recommended next lane

Create a spec-backed, read-only local bridge spike that exposes one harmless operator status operation over loopback only.

## Entry criteria

- A spec identifies the first operation, transport, authentication mechanism, and stop conditions.
- Tests define loopback-only behavior and fail-closed credential behavior.
- The implementation plan avoids changing solver entrypoint semantics.

## Exit criteria

- One read-only operation succeeds locally with valid short-lived credentials.
- Invalid credentials fail closed.
- Non-allowlisted operations fail closed.
- Bind-address evidence confirms local-only exposure.
- Logs show required redaction behavior.
