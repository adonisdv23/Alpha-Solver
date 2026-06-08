# Candidate Operator Confirmation Fields

## Scope

These fields document candidate confirmations an operator may record before or after a local job. They do not implement prompts, approvals, permissions, access control, UI confirmations, or runtime gates.

## Candidate confirmation identity fields

| Field | Candidate meaning | Notes |
| --- | --- | --- |
| `confirmation_id` | Stable identifier for one confirmation record. | Candidate string. |
| `job_id` | Candidate job associated with the confirmation. | Candidate reference only. |
| `confirmed_by_operator` | Operator label or pseudonymous handle. | Avoid unnecessary personal data. |
| `confirmed_at_local` | Local timestamp for confirmation. | Candidate timestamp. |
| `confirmation_method` | How confirmation was recorded. | Candidate values: `task_prompt`, `local_note`, `commit_message`, `packet_file`. |

## Candidate confirmation checklist fields

| Field | Candidate meaning | Notes |
| --- | --- | --- |
| `confirmed_scope_understood` | Operator confirms allowed and disallowed scope was reviewed. | Candidate boolean. |
| `confirmed_docs_only` | Operator confirms docs-only boundary when applicable. | Candidate boolean. |
| `confirmed_no_runtime_change` | Operator confirms no runtime code was changed. | Candidate boolean. |
| `confirmed_no_provider_call` | Operator confirms no hosted or local model provider call was made. | Candidate boolean. |
| `confirmed_no_database_or_queue` | Operator confirms no database table, queue, worker, or scheduler was created. | Candidate boolean. |
| `confirmed_no_api_or_dashboard_route` | Operator confirms no API or dashboard route was created or exposed. | Candidate boolean. |
| `confirmed_no_evidence_promotion` | Operator confirms no evidence was promoted beyond the packet boundary. | Candidate boolean. |
| `confirmed_changed_files_scope` | Operator confirms changed files stayed within allowed paths. | Candidate boolean. |
| `confirmation_exception_notes` | Notes for any false or not-applicable confirmation. | Candidate text. |
