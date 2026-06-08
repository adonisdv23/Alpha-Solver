# Artifact Capture Requirements

## Purpose

A future local-only harness should capture enough local artifacts for human review of preflights, bounded local commands, stop states, and closeout without promoting those artifacts as validation evidence.

## Required local artifacts

A future run should capture local artifacts such as:

- Run manifest with lane, task identifier, branch, commit, operator approval state, and declared local scope.
- Preflight results with pass/fail state and stop-before-start reasons.
- Command ledger containing only local command names, arguments, exit codes, start times, end times, and working directories.
- Redacted stdout/stderr summaries where allowed by the future implementation lane.
- File-change manifest for local files changed by the run.
- Stop-state record when a stop condition is reached.
- Closeout summary for operator review.

## Artifact boundaries

Artifact capture must remain local. It must not upload artifacts, expose dashboards, publish reports, call external APIs, call providers, call hosted models, use credentials, incur billing, deploy, automate browsers, expose `/v1/solve`, add fallback, or promote evidence.

Artifacts produced by a future harness are local run records only unless a separate accepted evidence lane later reviews and promotes them. This packet itself does not promote evidence.
