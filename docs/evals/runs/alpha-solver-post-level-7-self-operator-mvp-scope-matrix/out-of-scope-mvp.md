# Out-of-Scope MVP

Lane: `ALPHA-SOLVER-POST-LEVEL-7-SELF-OPERATOR-MVP-SCOPE-MATRIX-PACKET-001`

The following items are explicitly out of scope for the earliest safe Self Operator MVP:

| Exclusion | Boundary |
| --- | --- |
| Browser takeover | No autonomous browser control, site navigation, form submission, scraping, account access, purchasing, posting, messaging, or external workflow execution. |
| Provider calls | No local, hosted, third-party, fallback, benchmark, or quality-evaluation model calls. |
| Provider routing | No provider registry activation, provider selection, implicit routing, hidden fallback, or provider-backed `/v1/solve` behavior. |
| Billing and payments | No billing setup, metering, invoice reconciliation, purchase authorization, cost-incurring provider calls, or customer billing claims. |
| Production readiness | No claim that Self Operator, providers, API routes, dashboards, deployments, billing, or operational support are production-ready. |
| Autonomous merges | No autonomous branch merges, PR approvals, squash merges, release tagging, or evidence promotion. |
| Autonomous deployments | No deployment to local, staging, hosted, production, customer, or public environments. |
| Credential handling | No creation, collection, validation, storage, display, logging, dashboard rendering, evidence embedding, or use of credentials/secrets. |
| External actions | No emails, chats, tickets, repository writes outside approved local scope, package publication, issue edits, cloud changes, account actions, or network-side effects. |
| Runtime modification | No changes to runtime behavior, provider adapters, API routes, dashboard routes, orchestration logic, SAFE-OUT behavior, observability pipelines, or replay/determinism logic. |
| Benchmarks and scoring | No benchmark runs, comparative scoring, model ranking, or provider quality claims. |
| Unapproved fallback | No fallback behavior unless a later accepted lane defines an explicit, operator-visible, fail-closed fallback policy and implementation boundary. |

If a requested MVP behavior touches any excluded area, the Self Operator MVP must stop and hand control back to the operator.
