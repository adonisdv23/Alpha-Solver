# Approval, artifact, and stop-state gates

Static tests must fail with:

- `SELF_OPERATOR_APPROVAL_GATE_REQUIRED` if operator approval records are absent or bypassed.
- `SELF_OPERATOR_ARTIFACT_SCHEMA_INCOMPLETE` if raw artifacts, reviewer notes, command records, or redaction markers are missing.
- `SELF_OPERATOR_STOP_STATE_REQUIRED` if blocked conditions do not map to stop states.
