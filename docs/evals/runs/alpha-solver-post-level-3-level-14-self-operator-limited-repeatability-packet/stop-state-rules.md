# Stop-state rules

A future repeatability execution lane must stop immediately and record
`stop-state.json` below the output root if any terminal condition occurs.

## Stop states

| Stop state | Trigger |
| --- | --- |
| `operator_confirmation_invalid` | Required operator confirmation labels or text are missing or mismatched. |
| `plan_verification_blocked` | Mandatory pre-execution verification does not pass. |
| `unexpected_network_or_external_surface` | Any command attempts network access or a forbidden external surface. |
| `wrapper_execution_detected` | Wrapper executes proposed command text instead of classifying it. |
| `gate_status_unexpected` | Gate status differs from the expected local dry-run wrapper allowance. |
| `release_gate_failed` | Release-gate checker exits nonzero. |
| `packet_consistency_failed` | Packet consistency checker exits nonzero. |
| `source_artifact_mutation_detected` | Repository or source artifacts mutate during execution. |
| `redaction_issue_detected` | Sensitive material is detected in review artifacts. |
| `forbidden_surface_detected` | Any forbidden surface is reached or cannot be disproved. |
| `artifact_inventory_incomplete` | Required raw artifacts are missing. |

On any stop state, the future lane must preserve partial artifacts, avoid any
success wording, and select the blocked follow-up lane.
