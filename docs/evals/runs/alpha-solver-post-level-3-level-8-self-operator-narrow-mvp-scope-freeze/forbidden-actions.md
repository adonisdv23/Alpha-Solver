# Forbidden Actions

Lane: `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-8-SELF-OPERATOR-NARROW-MVP-SCOPE-FREEZE-PACKET-001`

The frozen future MVP must never perform the following actions:

- External actions of any kind.
- Network calls, provider calls, local or hosted model calls, benchmark calls, or routing/fallback calls.
- Browser automation, account access, form submission, scraping, purchasing, posting, messaging, email, chat, ticket, or issue actions.
- Credential or secret collection, validation, storage, display, logging, or use.
- Billing, payment, metering, invoice, quota, or spend-affecting actions.
- Deployment, release, merge, PR approval, evidence promotion, tag creation, package publication, or production changes.
- Runtime, API, dashboard, provider, SAFE-OUT, budget, replay, determinism, observability, or MCP behavior changes.
- File writes outside the future approved local artifact boundary, unless a later separate scope-expansion packet supersedes this freeze. A normal implementation lane must not expand this boundary.
- Command execution that is not explicitly allowlisted and specifically operator-confirmed.
- Continuation after missing, ambiguous, stale, conflicting, or overly broad operator confirmation.

Forbidden action handling must be fail-closed: stop locally, record a stop-state artifact, and return control to the operator.
