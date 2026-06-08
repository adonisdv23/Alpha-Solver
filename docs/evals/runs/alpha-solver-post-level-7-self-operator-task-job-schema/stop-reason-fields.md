# Candidate Stop Reason Fields

## Scope

These fields define candidate stop reason vocabulary for operator-only local execution records. They do not implement failure handling, retries, schedulers, queues, runtime exits, API errors, or dashboard states.

## Candidate stop reason fields

| Field | Candidate meaning | Notes |
| --- | --- | --- |
| `stop_reason` | Primary reason the job stopped. | Candidate enum-like value. |
| `stop_reason_detail` | Human-readable details about the stop. | Candidate text. |
| `stopped_at_local` | Local timestamp when the stop occurred. | Candidate timestamp. |
| `stopped_by` | Actor or process label that stopped the job. | Candidate values: `operator`, `guardrail`, `check_failure`, `scope_boundary`, `environment`. |
| `recoverability` | Whether the stop can be retried or requires a fix lane. | Candidate values: `retryable`, `requires_fix_lane`, `not_retryable`, `not_applicable`. |
| `fallback_lane` | Fallback lane to use when blocked. | For this packet: `ALPHA-SOLVER-POST-LEVEL-7-SELF-OPERATOR-TASK-JOB-SCHEMA-FIX-001`. |

## Candidate stop reason values

| Value | Candidate meaning |
| --- | --- |
| `completed_successfully` | Job completed within the allowed scope. |
| `blocked_missing_source_evidence` | Required source evidence was unavailable. |
| `blocked_scope_conflict` | Requested action conflicts with allowed scope. |
| `blocked_checks_failed` | Required checks failed and need follow-up. |
| `blocked_environment_limitation` | Local environment prevented completion. |
| `blocked_operator_confirmation_missing` | Required operator confirmation was missing. |
| `stopped_for_safety_boundary` | Work stopped to preserve a safety or evidence boundary. |
| `abandoned_superseded` | Job was superseded by another lane or instruction. |
