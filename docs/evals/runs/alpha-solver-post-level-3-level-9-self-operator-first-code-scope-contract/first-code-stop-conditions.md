# First-code stop conditions

The future first-code lane must stop, make no further changes, and open no PR if any condition below is present.

## Hard stop conditions

- The controlling Level 9 packet has not authorized a first-code lane.
- The work would exceed static test scaffold scope and the controlling Level 9 packet has not explicitly widened scope.
- A changed file falls outside the allowed categories in `allowed-files.md`.
- Any forbidden file category in `forbidden-files.md` appears in the diff.
- Any forbidden behavior in `forbidden-code-behavior.md` appears in the diff.
- `git diff --check` or `git diff --cached --check` reports an error.
- The changed-file scope proof cannot be produced clean before commit or before PR creation.
- The branch is not based on current main.
- Source artifacts would be modified, or evidence would be promoted.

## Stop behavior

If a stop condition appears after edits have already been made, the future operator must not commit and must not open a PR. The operator must not use a commit, squash, or reformat to hide an out-of-scope diff. If a corrective docs-only follow-up is needed, the operator must use the blocker fallback lane in `blocker-fallback-lane.md`.
