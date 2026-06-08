# Operator Runbook Skeleton

This is a future operator-facing skeleton only. It does not run Self Operator, acceptance, or evidence review.

## 1. Prerequisites

- TBD_AFTER_ARTIFACT_PREFLIGHT_FOUNDATION: implementation PRs merged and GS done.
- TBD_AFTER_ARTIFACT_PREFLIGHT_FOUNDATION: approved lane ID and run ID.
- TBD_AFTER_ARTIFACT_PREFLIGHT_FOUNDATION: operator-facing approval copy available.

## 2. Local-only scope

- The run remains `local-only` and operator-supervised.
- No providers, hosted model calls, external APIs, browser automation, deployment, billing, Google Sheets updates, credentials, source-artifact mutation, or evidence promotion are allowed.

## 3. Operator confirmation

- TBD_AFTER_ARTIFACT_PREFLIGHT_FOUNDATION: exact confirmation text.
- Hard stop: stop if explicit operator confirmation is missing.

## 4. Preflight

- TBD_AFTER_ARTIFACT_PREFLIGHT_FOUNDATION: preflight command placeholder.
- TBD_AFTER_ARTIFACT_PREFLIGHT_FOUNDATION: expected local preflight artifact path.

## 5. Approved local commands

- TBD_AFTER_ARTIFACT_PREFLIGHT_FOUNDATION: approved local command list.
- Do not fabricate commands or outputs in this skeleton.

## 6. Blocked commands

- Provider calls.
- Hosted model calls.
- External API calls.
- Browser automation.
- Deployment or billing commands.
- Google Sheets updates.
- Commands that mutate source artifacts.

## 7. Stop states

- Missing explicit operator confirmation.
- Scope unclear.
- Changed files or outputs outside allowed scope.
- Evidence boundary cannot be preserved.
- Artifact path unsafe or unredacted.

## 8. Artifact output location

- TBD_AFTER_ARTIFACT_PREFLIGHT_FOUNDATION: allowed local output directory.
- TBD_AFTER_ARTIFACT_PREFLIGHT_FOUNDATION: redacted artifact path.

## 9. Redaction review

- Confirm no secrets, credentials, provider output, external API responses, browser data, deployment output, billing data, or Google Sheets data are present.

## 10. Dry-run procedure

- TBD_AFTER_ARTIFACT_PREFLIGHT_FOUNDATION: local dry-run command placeholder.
- Record only local, redacted, operator-supervised artifacts.

## 11. Acceptance procedure

- TBD_AFTER_ACCEPTANCE_LANE: acceptance cannot start until prerequisite implementation PRs are merged and GS done.
- TBD_AFTER_ACCEPTANCE_LANE: acceptance command/output placeholders.

## 12. Abort conditions

- Any boundary violation.
- Any missing operator confirmation.
- Any unredacted artifact.
- Any attempt to claim MVP readiness before acceptance evidence exists and is interpreted.

## 13. Post-run review

- TBD_AFTER_ARTIFACT_PREFLIGHT_FOUNDATION: review artifact path.
- Verify checklist completion, redaction, stop-state behavior, and evidence boundary.

## 14. Evidence boundary

- Future evidence remains local-only and operator-supervised unless a later approved lane changes the boundary.
- This skeleton does not import, interpret, promote, or validate evidence.

## 15. Support/escalation notes

- Escalate to a human operator if the scope, commands, artifact paths, redaction status, or stop state is unclear.

## 16. Future fill-in placeholders

- TBD_AFTER_ARTIFACT_PREFLIGHT_FOUNDATION: commands.
- TBD_AFTER_ARTIFACT_PREFLIGHT_FOUNDATION: artifact paths.
- TBD_AFTER_ACCEPTANCE_LANE: acceptance outputs.
- TBD_AFTER_RELEASE_CLOSEOUT: release closeout references.
