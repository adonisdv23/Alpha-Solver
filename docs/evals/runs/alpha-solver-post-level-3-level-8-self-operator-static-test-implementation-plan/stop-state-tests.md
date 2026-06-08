# Stop-State Tests

## Purpose

Planned static tests must verify that Self Operator stop states are explicit, terminal, persisted, and non-promotional.

## Required stop states

Future implementation should define a constrained stop-state set before execution is trusted. Initial planned states:

- `STOPPED_PENDING_APPROVAL`
- `STOPPED_APPROVAL_DENIED`
- `STOPPED_BLOCKED_BEHAVIOR_DETECTED`
- `STOPPED_ARTIFACT_PERSISTENCE_FAILED`
- `STOPPED_STATIC_GUARDRAIL_FAILED`
- `STOPPED_OPERATOR_ERROR`

## Planned test cases

| Case | Expected result |
|---|---|
| Every blocked behavior maps to a stop state. | No finding when all mappings exist. |
| Missing stop state for provider-call block. | `SELF_OPERATOR_STOP_STATE_REQUIRED`. |
| Code continues after stop-state assignment. | `SELF_OPERATOR_STOP_STATE_NOT_TERMINAL`. |
| Stop state is not persisted to artifact schema. | `SELF_OPERATOR_STOP_STATE_NOT_PERSISTED`. |
| Stop state text claims evidence promotion or runtime trust. | `SELF_OPERATOR_STOP_STATE_PROMOTION_BLOCKED`. |

## Expected output format

Stop-state findings should include `finding_id`, `blocked_behavior`, `expected_stop_state`, `path`, `line`, and `message`.
