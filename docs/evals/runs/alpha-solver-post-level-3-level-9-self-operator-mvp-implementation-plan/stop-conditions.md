# Stop Conditions

These docs-only stop conditions bind any future implementation lane derived from this plan. This packet does not implement code.

## Hard stops before editing

A future lane must stop before editing if any of these is true:

- Level 8 acceptance or this Level 9 plan is absent, stale, or ambiguous.
- The Level 10 lane is not separately approved by an operator.
- The branch is not current-main-based.
- The requested edit exceeds the allowed first-implementation scope (static tests, fixtures, and shared helpers only).
- The edit would introduce a runtime wrapper or CLI behavior before static tests exist.
- The edit would introduce provider calls, hosted model calls, external API calls, credentials, browser automation, deployment, billing, route exposure, fallback, or evidence promotion.
- The edit would modify runtime, provider, API, dashboard, CLI, checker scripts, existing tests, the Makefile, CI, or source-artifact files.

## Stop before commit and PR

A future lane must not commit or open a PR if the staged or unstaged diff shows out-of-scope files, any forbidden integration, or whitespace errors. The lane must run staged and unstaged diff checks (`git status --short`, `git diff --name-only`, `git diff --name-only --cached`, `git diff --check`, `git diff --cached --check`) and confirm the changed-file set before committing. It must not use a commit to normalize or hide an out-of-scope diff.

## Stop handling

When any stop condition applies, the future lane must leave the working tree unchanged where possible, capture raw artifacts and reviewer notes for the stop, report the blocker, and use the blocker fallback lane if a docs-only correction is needed.
