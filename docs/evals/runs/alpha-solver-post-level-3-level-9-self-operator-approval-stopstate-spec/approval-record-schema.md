# Approval record schema

Required fields:

- `schema_version`
- `lane_id`
- `operator_confirmation_text`
- `approved_scope`
- `approved_files`
- `forbidden_files_acknowledged`
- `hard_stops_acknowledged`
- `approved_at_utc`
- `operator_review_required_after_run`

The record must be local-only and must not contain secrets, credentials, provider outputs, browser data, deployment output, billing data, or evidence-promotion labels.
