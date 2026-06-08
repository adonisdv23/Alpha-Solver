# Approval record schema

Proposed local-only fields:

- `schema_version`
- `selected_lane`
- `approved_scope`
- `operator_confirmation_present`
- `confirmation_copy_version`
- `confirmed_at_utc`
- `hard_stops_acknowledged`
- `stop_state_if_missing`

The record must not contain credentials, secrets, provider output, external API output, browser data, billing data, deployment output, or evidence-promotion labels.
