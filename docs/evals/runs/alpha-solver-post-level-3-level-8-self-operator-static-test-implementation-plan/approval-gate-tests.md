# Approval Gate Tests

## Purpose

Planned static tests must prove that Self Operator side effects cannot proceed without explicit human approval metadata.

## Approval requirements

A future implementation should statically expose these concepts before it is trusted:

- A side-effect classification for any operation that writes files, runs commands, opens routes, invokes tools, or mutates state.
- An approval record containing approver identity or local reviewer marker, timestamp, scope, approved action, and artifact destination.
- A fail-closed branch when approval is missing, malformed, stale, or out of scope.
- Artifact persistence for approval decisions and denial decisions.

## Planned test cases

| Case | Fixture shape | Expected finding |
|---|---|---|
| Approved local no-op | Side-effect classifier present and approval checked before no-op execution. | No finding. |
| Missing approval check | Side-effect operation with no approval guard. | `SELF_OPERATOR_APPROVAL_GATE_REQUIRED`. |
| Approval after action | Approval is recorded only after action execution. | `SELF_OPERATOR_APPROVAL_ORDER_INVALID`. |
| Broad approval | Approval scope is wildcard or not tied to the action. | `SELF_OPERATOR_APPROVAL_SCOPE_INVALID`. |
| Denial ignored | Denial stop state exists but code continues. | `SELF_OPERATOR_APPROVAL_DENIAL_IGNORED`. |

## Expected outputs

Failures should include the side-effect operation name, the missing or invalid approval field, and the line where execution could proceed without a valid approval gate.
