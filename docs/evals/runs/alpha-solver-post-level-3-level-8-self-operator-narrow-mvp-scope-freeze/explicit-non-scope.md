# Explicit Non-Scope

Lane: `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-8-SELF-OPERATOR-NARROW-MVP-SCOPE-FREEZE-PACKET-001`

The following are not in the frozen future MVP scope:

- Autonomous agent execution.
- Browser control, website navigation, scraping, form submission, account access, purchasing, posting, or messaging.
- Provider calls, local model calls, hosted model calls, model routing, fallback, failover, benchmarking, scoring, or quality claims.
- API route exposure, dashboard exposure, product UI changes, or customer-facing surfaces.
- Runtime behavior changes, orchestration changes, SAFE-OUT changes, replay/determinism changes, observability pipeline changes, or budget-guard changes.
- Credential creation, collection, validation, storage, use, rendering, logging, or evidence embedding.
- External repository operations, PR approval, merge, release, tag, publish, deployment, package publication, or evidence promotion.
- Billing, metering, quota, invoice, purchase, payment, or cost-incurring operations.
- Broad artifact generation outside the local packet/checker/summary/stop-state boundary.
- Any action not explicitly allowlisted by a later accepted implementation lane.

If a requested future behavior touches non-scope, the MVP must stop and produce a local stop-state artifact instead of proceeding.
