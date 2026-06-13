# Blocked after approval

The real operator approval artifact was present and was ingested by the local wrapper/gate, but approved execution stopped because the local gate did not validate the artifact.

Blocked status:

```text
APPROVAL_CAPTURED_EXECUTION_BLOCKED_BY_LOCAL_SAFETY_GATE
```

Gate details:

```text
allowed_for_local_dry_run=false
reason_code=approval_invalid
required finding=SELF_OPERATOR_APPROVAL_HARD_STOP_TEXT_REQUIRED
```

The packet preserves the artifact as supplied rather than editing the operator's text. No local post-gate no-op or deterministic artifact action was treated as approved after this gate result.
