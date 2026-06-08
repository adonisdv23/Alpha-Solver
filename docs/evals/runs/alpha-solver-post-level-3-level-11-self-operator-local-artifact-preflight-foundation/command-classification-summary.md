# Command classification summary

Implemented a deterministic classifier for proposed command strings or argv lists. The classifier never executes commands.

Stable blocked reason codes include:

- `provider_call`
- `network_external_api`
- `browser_automation`
- `deployment`
- `billing`
- `credential_secret_access`
- `google_sheets`
- `source_artifact_mutation`
- `evidence_promotion`
- `unclear_requires_operator_review`

Safe local read/check commands such as `git status`, `git diff`, `rg`, `python -m pytest`, and the local packet checker are classified as allowed local read/check commands.
