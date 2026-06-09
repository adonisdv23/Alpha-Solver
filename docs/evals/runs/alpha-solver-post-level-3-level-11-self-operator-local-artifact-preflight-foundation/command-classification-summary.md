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

## PR #454 review-thread safety fix

The command allowlist now applies command-specific safe-argument checks before returning `allowed_local_read_check`. Mutating forms such as `find . -delete`, `find . -exec ...`, `git branch -D main`, `git branch --delete main`, `git branch -m old new`, and `git diff --output=artifact.json` fail closed as `source_artifact_mutation` instead of being accepted solely because their prefixes are allowlisted.

Safe read/check examples remain allowed, including `git status --short`, `git diff --name-only`, `git diff --check`, `rg -n pattern path`, focused `python -m pytest`, and non-mutating `find` listings.
