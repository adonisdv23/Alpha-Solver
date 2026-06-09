# Failure and Retry Rules

The operator must stop or retry only under explicit review when any condition occurs:

- Missing artifact.
- Malformed artifact.
- Failed redaction.
- Unexpected command execution.
- Output outside root.
- Source mutation.
- Identity mismatch not blocked.
- Unsafe command not blocked.
- Acceptance task not reproducible.
- Evidence boundary violation.

Retry is allowed only after the cause is documented, the temporary output root is reset or safely separated, and explicit operator confirmation is renewed.
