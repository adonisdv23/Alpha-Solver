# Candidate Job Schema Fields

## Scope

These are candidate job fields only. They describe one attempted execution of a task in an operator-only local context. They do not create jobs, queues, workers, schedulers, database tables, API routes, dashboard routes, or runtime execution.

## Candidate job identity fields

| Field | Candidate meaning | Notes |
| --- | --- | --- |
| `job_id` | Stable local identifier for one task execution attempt. | Candidate string. |
| `task_id` | Link back to the candidate task identifier. | Candidate reference only; not a foreign key. |
| `job_attempt_number` | Attempt number for the task. | Candidate integer starting at `1`. |
| `job_created_at_local` | Local timestamp when the job record is drafted. | Candidate timestamp. |
| `job_started_at_local` | Local timestamp when operator work starts. | Candidate timestamp. |
| `job_completed_at_local` | Local timestamp when operator work ends. | Candidate timestamp. |
| `job_status` | Current status of the job attempt. | Candidate values: `draft`, `confirmed`, `running`, `stopped`, `completed`, `failed`, `abandoned`. |

## Candidate execution context fields

| Field | Candidate meaning | Notes |
| --- | --- | --- |
| `repo_name` | Repository owner/name or local repository label. | Candidate text. |
| `branch_name` | Git branch used for the job. | Candidate text. |
| `base_commit` | Commit SHA observed before changes. | Candidate text. |
| `result_commit` | Commit SHA after changes, when applicable. | Candidate text. |
| `working_directory` | Local working directory used by the operator. | Candidate text; may be omitted or redacted in shared artifacts. |
| `operator_runtime_profile` | Local environment profile. | Candidate label such as `non_interactive_local`. |

## Candidate job outcome fields

| Field | Candidate meaning | Notes |
| --- | --- | --- |
| `job_summary` | Short summary of completed work. | Candidate markdown or plain text. |
| `changed_files` | Files changed by the job. | Candidate list of repo-relative paths. |
| `checks_run` | Checks executed for the job. | Candidate list; see `checks-run.md` for this packet's check record. |
| `stop_reason` | Why the job stopped, if it did. | See `stop-reason-fields.md`. |
| `operator_confirmations` | Confirmation record for sensitive boundaries. | See `operator-confirmation-fields.md`. |
| `artifact_references` | Output artifacts created or reviewed. | See `artifact-reference-fields.md`. |
| `evidence_boundary_label` | Evidence label applied to job outcome. | Example: `DOCS_ONLY_SCHEMA_DESIGN`. |
