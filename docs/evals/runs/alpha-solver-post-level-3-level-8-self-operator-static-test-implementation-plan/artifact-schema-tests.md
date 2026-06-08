# Artifact Schema Tests

## Purpose

Planned static tests must verify that any future Self Operator action records enough local artifacts to support review without promoting untrusted behavior.

## Required artifact fields

| Field | Requirement | Expected static assertion |
|---|---|---|
| `run_id` | Stable local run identifier. | Schema defines required string field. |
| `input_ref` | Reference to original operator input. | Schema requires immutable reference. |
| `approval_ref` | Reference to explicit approval record. | Schema requires non-empty approval linkage before side effects. |
| `action_plan_ref` | Reference to planned action text. | Schema preserves plan separately from execution result. |
| `stdout_ref` | Reference to captured stdout, if any. | Schema supports empty, partial, and failed outputs. |
| `stderr_ref` | Reference to captured stderr, if any. | Schema supports empty, partial, and failed errors. |
| `stop_state` | Terminal stop state when execution halts. | Schema restricts to approved stop-state enum. |
| `redaction_log_ref` | Reference to redaction notes. | Schema requires explicit marker for removed sensitive values. |
| `review_notes_ref` | Reviewer-authored notes kept separate from raw artifacts. | Schema prevents summary text from replacing raw outputs. |

## Planned test cases

- Accept a complete schema fixture with all required fields.
- Reject a schema missing `approval_ref`.
- Reject a schema missing raw output references.
- Reject a schema that stores reviewer notes inside raw output fields.
- Reject a schema with no stop-state field.
- Reject a schema with no redaction log reference.

## Expected outputs

- Complete fixture: no findings.
- Missing required field: `SELF_OPERATOR_ARTIFACT_SCHEMA_INCOMPLETE` with the missing field name.
- Raw/reviewer boundary violation: `SELF_OPERATOR_ARTIFACT_BOUNDARY_VIOLATION`.
