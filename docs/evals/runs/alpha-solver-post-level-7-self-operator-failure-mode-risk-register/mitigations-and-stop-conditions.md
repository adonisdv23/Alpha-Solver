# Mitigations and Stop Conditions

## Mitigation themes for future implementation

A future Self Operator implementation must define and test these controls before enabling action-taking behavior:

- Default-deny action policy with explicit allowlists by lane and file path.
- Human approval gates for provider calls, credential access, deployment, API exposure, dashboard exposure, merges, auto-merge, branch-protection changes, and evidence promotion.
- Branch hygiene checks before commit and before PR update.
- Stale-state checks for base branch, selected-next files, source-of-truth instructions, and review comments.
- Evidence-class labels that distinguish docs-only planning, local smoke evidence, provider evidence, benchmark evidence, readiness review, and production claims.
- Exact source-evidence logging with reviewed files and commands.
- Secret redaction, private URL handling, and pre-commit secret scanning.
- Provider and fallback fail-closed behavior with no implicit hosted calls.
- Product-surface gates for routes, dashboards, previews, health endpoints, metrics, and API exposure.
- Incident path for suspected credential exposure, provider misuse, unsafe merge, or evidence overclaim.

## Global stop conditions

Stop Self Operator work if any of the following occurs:

- The requested action exceeds the approved lane scope.
- The changed-file set includes paths outside the approved allowlist.
- Runtime, provider, API, dashboard, CI, deployment, credential, branch-protection, or merge behavior is requested under a docs-only packet.
- Credentials, private URLs, or non-redacted sensitive content appear in output or diffs.
- A command can call local or hosted providers without explicit approval.
- The operator cannot identify exact source evidence.
- Evidence is being promoted beyond its accepted boundary.
- A PR branch is stale, polluted, or contains unrelated changes.
- A readiness claim is requested without a dedicated readiness decision.

## Future review requirement

Before any implementation starts, reviewers must confirm that the proposed Self Operator design maps every allowed action to a mitigation, every blocked action to a stop condition, and every evidence output to a claim boundary.
