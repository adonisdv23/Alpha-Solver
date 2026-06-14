# Residual Risks

## Design risks

- The exact bridge transport is not selected in this packet.
- The operation allowlist is not enumerated to implementation granularity.
- Token lifetime, storage, and rotation requirements need a concrete spec.
- Console output redaction rules need testable fixtures.

## Implementation risks

- A future bridge could accidentally expose a non-loopback interface.
- A future bridge could permit generic command execution instead of allowlisted operations.
- Logs could leak prompts, paths, tokens, or environment-derived secrets.
- Runtime entrypoint behavior could drift if bridge dispatch is not isolated.

## Mitigations for next work

- Require fail-closed tests before any bridge merge.
- Add explicit bind-address checks.
- Keep bridge operations narrow and read-only for the first implementation lane.
- Treat credential and redaction tests as merge blockers.
