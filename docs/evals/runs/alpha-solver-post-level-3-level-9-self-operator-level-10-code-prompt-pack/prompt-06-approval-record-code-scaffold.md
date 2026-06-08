# prompt-06-approval-record-code-scaffold

Create only approval record code scaffold if explicitly selected. Require explicit operator confirmation and local-only redacted records.

## Required hard stops

Stop unless Level 9 implementation plan is accepted and GS done.
Stop unless the selected Level 10 lane matches this prompt.
Stop if current branch is not current-main-based.
Stop if changed files exceed allowed scope.
Stop on provider call risk.
Stop on credential risk.
Stop on browser automation.
Stop on deployment.
Stop on billing.
Stop on `/v1/solve` or dashboard exposure.
Stop on fallback.
Stop on evidence promotion.
Stop on source-artifact mutation.

## Output requirements

Return changed files, exact checks run, scope confirmation, evidence boundary, and explicit non-actions.
