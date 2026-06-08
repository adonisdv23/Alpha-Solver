# Stop Conditions

Work must stop and move to the blocker fallback lane if any of the following occur during review or future planning:

- A provider call is proposed, attempted, or required.
- Browser automation is proposed, attempted, or required.
- Credentials, API keys, browser secrets, deployment secrets, or billing secrets are proposed, read, stored, or required.
- Hosted fallback, provider fallback, or implicit local fallback is proposed or observed.
- Deployment, production rollout, public route exposure, or dashboard exposure is proposed.
- Billing, spend, tenant accounting, invoices, or live budget enforcement are proposed.
- Autonomous merge, auto-approval, or bypass of human review is proposed.
- Local artifact persistence is implemented without an approved persistence contract.
- Human approval controls are implemented without an approved approval contract.
- A local run harness is implemented without an approved command, timeout, output, and stop-reason contract.
- Acceptance tests are treated as optional before implementation readiness is claimed.
- Unrelated files or branches are modified outside the approved scope.
- Level 3/local evidence is promoted to MVP readiness, production readiness, provider evidence, billing evidence, dashboard readiness, or broad runtime readiness.

## Required stop response

If a stop condition is encountered, do not continue implementation. Record the blocker, preserve existing evidence boundaries, and use the blocker fallback lane recorded in `blocker-fallback-lane.md`.
