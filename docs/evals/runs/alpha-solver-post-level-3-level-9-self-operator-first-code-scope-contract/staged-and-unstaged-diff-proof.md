# Staged and unstaged diff proof

The future first-code lane must produce diff proof of its full change set before committing and before opening a PR. This proof shows that the change set stays inside the allowed static-test-scaffold scope.

## Required commands

The future first-code lane must run and record the output of all of the following, both before commit and before PR creation:

- `git diff --name-only` — unstaged changed files.
- `git diff --cached --name-only` — staged changed files.
- `git diff --check` — unstaged whitespace and conflict-marker check.
- `git diff --cached --check` — staged whitespace and conflict-marker check.

## Required changed-file scope proof

In addition to the four commands above, the future first-code lane must record a **changed-file scope proof** before commit and before PR creation. The scope proof must show that every changed file is an allowed static test file, an allowed inert fixture, or the lane's own docs packet, and that no forbidden file category appears.

## Proof template

```
git diff --name-only
git diff --cached --name-only
git diff --check
git diff --cached --check
# changed-file scope proof: confirm every path above is allowed and none is forbidden
```

If any command shows an out-of-scope file, a whitespace or conflict-marker error, or a forbidden file category, the future first-code lane must stop under `first-code-stop-conditions.md`.
