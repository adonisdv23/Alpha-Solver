# Candidate Artifact Reference Fields

## Scope

These fields define candidate references to output artifacts. They do not create artifact storage, uploads, databases, object stores, dashboards, API responses, or evidence promotion.

## Candidate artifact fields

| Field | Candidate meaning | Notes |
| --- | --- | --- |
| `artifact_id` | Stable local identifier for an artifact. | Candidate string. |
| `job_id` | Candidate job associated with the artifact. | Candidate reference only. |
| `artifact_type` | Type of artifact. | Candidate values: `markdown_doc`, `check_log`, `diff_summary`, `commit`, `pr`, `screenshot`, `other`. |
| `artifact_path` | Repo-relative path or local packet path. | Candidate text. |
| `artifact_uri` | Optional URL or external reference. | Candidate text; avoid secrets. |
| `artifact_created_at_local` | Local timestamp when artifact was created or recorded. | Candidate timestamp. |
| `artifact_digest` | Optional checksum or digest. | Candidate text; no checksum generation is implemented here. |
| `artifact_redaction_status` | Redaction state for sharing. | Candidate values: `not_required`, `redacted`, `requires_review`, `do_not_share`. |
| `artifact_evidence_boundary_label` | Evidence boundary label applied to the artifact. | Example: `DOCS_ONLY_SCHEMA_DESIGN`. |
| `artifact_notes` | Concise audit note for context and limits. | Candidate text. |

## Candidate output references for this packet

The output artifacts for this lane are the markdown files in `docs/evals/runs/alpha-solver-post-level-7-self-operator-task-job-schema/` and the resulting git commit and PR reference.
