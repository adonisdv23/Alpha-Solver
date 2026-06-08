# Candidate Run ID and Trace Fields

## Scope

These fields are candidate trace vocabulary for future audit. They are not tracing infrastructure, telemetry, observability code, request IDs in production, API headers, database columns, or runtime behavior.

## Candidate run identifiers

| Field | Candidate meaning | Notes |
| --- | --- | --- |
| `run_id` | Top-level identifier for an operator run. | Candidate string unique within a local packet or audit ledger. |
| `trace_id` | Identifier that can group task, job, checks, and artifacts. | Candidate string; no tracing backend is implied. |
| `task_id` | Candidate task identifier associated with the run. | Mirrors `task-schema.md`. |
| `job_id` | Candidate job attempt identifier associated with the run. | Mirrors `job-schema.md`. |
| `run_sequence_number` | Operator-visible sequence number for ordered local runs. | Candidate integer. |
| `parent_run_id` | Prior run that this run follows or retries. | Candidate string; optional. |

## Candidate trace context fields

| Field | Candidate meaning | Notes |
| --- | --- | --- |
| `trace_started_at_local` | Local timestamp when trace capture starts. | Candidate timestamp. |
| `trace_completed_at_local` | Local timestamp when trace capture ends. | Candidate timestamp. |
| `trace_scope` | What the trace covers. | Candidate values: `docs_only`, `local_checks`, `manual_operator_run`, `runtime_experiment`. |
| `trace_redaction_profile` | Redaction rule label used for shared artifacts. | Candidate text. |
| `trace_evidence_boundary_label` | Evidence boundary label applied to trace output. | Example: `DOCS_ONLY_SCHEMA_DESIGN`. |
| `trace_notes` | Brief operator notes about trace limitations. | Candidate text. |
