# Session Evidence Format

This is a paper-only format for future Alpha-native local operator sessions. It is not a runtime schema and does not create storage, UI, API, or automation.

## Required fields

| Field | Required | Description |
| --- | --- | --- |
| `session_id` | yes | Stable local identifier, for example `alpha-local-harness-YYYY-MM-DD-###`. |
| `branch_label` | yes | Human-readable branch or lane label. |
| `task_id` | yes | Packet case id, lane id, or operator task id. |
| `lane_id` | yes | Controlling lane id. |
| `repo_commit` | recommended | Commit SHA inspected or changed, when applicable. |
| `prompt_source` | yes | Repo path and section for the prompt/template source. |
| `operator_action` | yes | Named local operator action from the template map or future approved equivalent. |
| `evidence_boundary` | yes | Short statement of what the session can and cannot support. |
| `raw_output_pointer` | conditional | Local pointer to raw output if generated under authorization; otherwise `none`. |
| `score_pointer` | conditional | Local pointer to blind scores/rubric output if scoring occurred under authorization; otherwise `none`. |
| `non_claims` | yes | Claims that the session must not support. |
| `stop_reason` | yes | `completed_docs_only`, `blocked_missing_authorization`, `blocked_no_raw_output`, `failed_closed`, `needs_human`, `evidence_conflict`, or another explicit reason. |
| `operator_decision` | yes | `stop`, `continue_within_scope`, `queue_followup`, `escalate_to_human`, or `export_sanitized`. |
| `export_status` | yes | `not_exported`, `sanitized_export_ready`, `exported_sanitized`, or `blocked_export`. |
| `redaction_status` | yes | `not_needed`, `pending_review`, `redacted`, or `blocked_contains_sensitive_material`. |
| `external_upload` | yes | Must default to `no`. |
| `provider_or_model_call` | yes | Must record `none` unless a future lane explicitly authorizes otherwise. |

## Example record shape

```yaml
session_id: alpha-local-harness-2026-06-15-001
branch_label: local-operator-harness-design-note
task_id: ALPHA-SOLVER-LOCAL-OPERATOR-HARNESS-DESIGN-NOTE-001
lane_id: ALPHA-SOLVER-LOCAL-OPERATOR-HARNESS-DESIGN-NOTE-001
repo_commit: pending
prompt_source: docs/CURRENT_STATE.md#selected-next-lane
operator_action: record-local-harness-design-note
evidence_boundary: docs-only design note; no runtime, provider, model, dashboard, API, or Pi.dev integration evidence
raw_output_pointer: none
score_pointer: none
non_claims:
  - no value evidence
  - no runtime readiness evidence
  - no Pi.dev integration evidence
  - no Alpha superiority evidence
stop_reason: completed_docs_only
operator_decision: stop
export_status: sanitized_export_ready
redaction_status: not_needed
external_upload: no
provider_or_model_call: none
```

## Export and redaction fields

A future session should not be exported until the operator records:

- whether raw output exists and where it is stored;
- whether the raw output contains secrets, credentials, private prompts, private traces, personal data, or private workspace paths;
- whether redaction has been reviewed;
- whether the export is summary-only or includes sanitized excerpts;
- which non-claims must accompany the export;
- whether the export creates any public-surface, provider, model, value, or readiness confusion.
