# Required review artifacts

The future first-code lane's PR must carry the review artifacts below so a reviewer can confirm the change stayed inside this scope contract.

## Required artifacts in the PR

- The recorded output of `git diff --name-only` and `git diff --cached --name-only`.
- The recorded output of `git diff --check` and `git diff --cached --check`.
- The changed-file scope proof showing every changed file is an allowed static test file, an allowed inert fixture, or the lane's own docs packet.
- An explicit statement that the change is static test scaffold only and that no runtime Self Operator behavior was implemented.
- A statement that no forbidden file category and no forbidden behavior is present: no runtime code, provider code, API route exposure, dashboard route exposure, CLI behavior change, credentials, browser automation, deployment, billing, fallback, provider calls, external API calls, evidence promotion, or source-artifact mutation.
- The checks-run record for the lane.

## Reviewer gate

A reviewer must reject the PR if any required artifact is missing or if any artifact shows an out-of-scope or forbidden change.
