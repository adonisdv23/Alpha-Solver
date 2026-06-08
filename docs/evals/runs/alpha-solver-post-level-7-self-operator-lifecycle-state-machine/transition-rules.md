# Transition Rules

## Allowed transitions

| From | To | Condition |
| --- | --- | --- |
| `created` | `preflight` | A lifecycle record exists and local-only preflight is allowed. |
| `created` | `blocked` | Required initial scope, permission, or evidence is missing or unclear. |
| `preflight` | `awaiting_operator_confirmation` | All local preflight checks pass and an operator decision is required before execution. |
| `preflight` | `blocked` | Permission, evidence, scope, credentials boundary, fallback boundary, or claim safety is missing or ambiguous. |
| `preflight` | `failed` | A non-recoverable safety violation or corrupted lifecycle record is detected. |
| `awaiting_operator_confirmation` | `running_local_only` | Explicit operator approval is recorded for the precise local-only action. |
| `awaiting_operator_confirmation` | `stopped` | The operator declines, cancels, or stops the run. |
| `awaiting_operator_confirmation` | `blocked` | Approval is absent, stale, ambiguous, or narrower than the requested action. |
| `running_local_only` | `completed` | Approved local-only activity completes inside scope. |
| `running_local_only` | `blocked` | New permission, evidence, scope, credentials, fallback, or claim question appears. |
| `running_local_only` | `stopped` | Operator or system stop is requested. |
| `running_local_only` | `failed` | Non-recoverable execution error or safety violation occurs. |
| `blocked` | `preflight` | A future approved fix lane supplies missing documentation or local preflight input. |
| `blocked` | `stopped` | Operator chooses not to continue. |
| `stopped` | `archived` | Audit record is complete and no resumption is authorized. |
| `completed` | `archived` | Completion evidence is recorded and preserved. |
| `failed` | `archived` | Failure audit record is complete and preserved. |

## Disallowed transitions

- `created` directly to `running_local_only`.
- `preflight` directly to externally visible action.
- `awaiting_operator_confirmation` to `running_local_only` without explicit operator approval.
- `blocked`, `stopped`, `completed`, `failed`, or `archived` directly back to `running_local_only`.
- `archived` to any active state.

## Fail-closed transition rule

If a future implementation cannot determine the safe next transition, it must transition to `blocked` when recoverable or `failed` when non-recoverable. It must not infer permission from silence, missing files, incomplete evidence, defaults, or prior unrelated approvals.
