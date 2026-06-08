# Stop-state artifacts

A stop-state artifact is required whenever a blocked condition appears. Required fields:

- `stop_state_code`
- `blocked_surface`
- `reason`
- `first_detected_at_utc`
- `changed_files_at_stop`
- `commands_completed_before_stop`
- `operator_review_required: true`

Stop-state artifacts must be local-only and must not promote evidence.
