# Metadata schema

Proposed local-only fields:

- `schema_version`
- `run_id`
- `created_at_utc`
- `repo_branch`
- `commit_sha`
- `allowed_scope`
- `selected_lane`
- `artifact_boundary`
- `redaction_policy`

Forbidden fields include secrets, credentials, provider responses, external API responses, billing data, browser data, deployment output, and evidence-promotion labels.
