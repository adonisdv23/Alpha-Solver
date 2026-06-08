# Forbidden First Code Scope

The following work is forbidden for first Self Operator implementation and must not be included in the first runtime code lane.

## Forbidden changes

- Hosted provider calls, hosted LLM calls, paid API calls, provider fallback, or remote inference.
- Browser automation, browser control, DOM automation, web login automation, scraping, extension control, or remote UI driving.
- Credential creation, credential reads, secret storage, token handling, cookie handling, service account handling, secret validation, or secret logging.
- Deployment configuration, infrastructure changes, release automation, image publishing, production configuration, or Cloud Run changes.
- Billing integration, spend enablement, paid provider configuration, budget bypasses, or cost-reporting changes that imply live spend.
- Autonomous merges, unattended branch manipulation, pull request approval automation, or repository write operations outside explicit operator supervision.
- `/v1/solve` integration, API route exposure, dashboard exposure, UI controls, product surface exposure, public endpoints, or remote service exposure.
- Evidence promotion, benchmark claims, production readiness claims, accepted behavior evidence claims, or dashboard-visible evidence claims.
- Broad refactors of routing, MCP, SAFE-OUT, provider adapters, budget guards, determinism, observability, replay, SolverEnvelope behavior, deployment, or dashboard code.

## Stop rule

If a future first implementation proposal requires any forbidden change, the proposal must stop before runtime modification and use the blocker fallback lane.
