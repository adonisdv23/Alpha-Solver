# Approval Record Schema

A valid approval record must exist before Self Operator performs any gated action.

## Required fields

Each approval record must include:

- `approval_id`: Stable identifier for the approval record.
- `operator_identity`: Human operator identity or accountable approval source.
- `approval_timestamp_utc`: UTC timestamp when approval was granted.
- `requested_action_category`: One of the gated categories, such as PR creation, merge instructions, external provider calls, file deletion, deployment, billing, credential use, browser automation, or evidence promotion.
- `requested_action_details`: Specific action to perform.
- `target`: Exact repository, branch, PR, file path, environment, provider, account, credential, browser target, billing target, deployment target, or evidence artifact affected.
- `scope_limits`: Boundaries on what may and may not be done.
- `time_window`: Validity window for the approval.
- `confirmation_wording`: Exact wording that the operator confirmed.
- `stop_conditions_acknowledged`: Stop conditions acknowledged by the operator.
- `evidence_boundary`: Statement that approval does not expand evidence claims beyond the approved action.
- `record_location`: Where the approval record is stored.

## Invalid records

An approval record is invalid if it is missing required fields, uses ambiguous language, conflicts with another instruction, references a different action, references a different target, exceeds the time window, or cannot be audited.

When the approval record is invalid, Self Operator must stop.
