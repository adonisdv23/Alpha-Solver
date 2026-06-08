# Closeout Criteria

The earliest Self Operator MVP may be called released only when every required criterion below is satisfied and documented in the release packet.

## Mandatory release gates

1. **All planned tests pass.** Every planned static, local smoke, blocked-action, approval-gate, artifact-preservation, stop-condition, and release-notes check required for the MVP must pass with no unresolved release-blocking failures.
2. **Raw artifacts are preserved.** Raw inputs, outputs, logs, transcripts, operator decisions, approval records, checks, and generated evidence required by the release packet must be preserved in the approved artifact location without destructive rewriting.
3. **Runbook is updated.** The operator runbook must describe the exact operator-only workflow, required setup, required approvals, stop conditions, artifact-retention steps, and non-goals for the release.
4. **Operator approvals are documented.** Human operator approvals must be recorded before release closeout, including who approved, what was approved, when it was approved, and the evidence reviewed.
5. **No provider calls occurred.** Release validation must not call hosted providers, billable model APIs, remote inference endpoints, or any provider fallback path.
6. **No browser automation occurred.** Release validation must not drive a browser, headless browser, remote browser session, crawler, or UI automation tool.
7. **No deployment occurred.** Release validation must not deploy, publish, expose, tunnel, mutate, or promote any service or remote environment.
8. **No production claim is made.** The release can be described only as an operator-only MVP if supported by evidence; it must not be described as production-ready, generally available, or suitable for unattended production use.
9. **No autonomous operation claim is made.** The release must not claim autonomous operation, unsupervised operation, automatic provider use, automatic browser use, or automatic deployment.

## Closeout decision rule

If any mandatory release gate is incomplete, ambiguous, contradicted by evidence, or missing an artifact, the Self Operator MVP is not released. The packet must use the fallback lane instead of making or implying a release claim.
