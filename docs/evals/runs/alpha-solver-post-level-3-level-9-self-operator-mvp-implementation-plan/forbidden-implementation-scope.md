# Forbidden Implementation Scope

The following work is forbidden for the first actual code lane and for any implementation lane derived from this plan, unless a later, separate, explicitly approved scope-expansion lane supersedes this plan. A normal implementation lane must not expand this boundary.

## Forbidden in the first code lane

- Any runtime wrapper, runner, CLI behavior, or Self Operator execution path. Static tests are required before any runtime wrapper or CLI behavior.
- Provider calls, hosted model calls, hosted LLM calls, paid API calls, provider adapters, model routing, or remote inference. The first code lane has no provider calls and no hosted model calls.
- External API calls, outbound HTTP clients, sockets, webhooks, or remote service clients. The first code lane has no external API calls.
- Credential creation, reads, writes, validation, storage, rotation, display, logging, or transmission. The first code lane has no credentials.
- Browser automation, browser control, DOM automation, scraping, or remote UI driving. The first code lane has no browser automation.
- Deployment, release automation, image publishing, infrastructure changes, or production configuration. The first code lane has no deployment.
- Billing, metering, spend enablement, paid-provider configuration, or budget changes. The first code lane has no billing.
- Route exposure, `/v1/solve` exposure, dashboard exposure, UI controls, or public endpoints.
- Fallback configuration, fallback-enabling code, local-to-provider fallback paths, or hosted fallback paths.
- Evidence promotion, readiness promotion, benchmark promotion, or score promotion. The first code lane has no evidence promotion.
- Autonomous merges or unattended repository writes outside the operator-approved local branch.
- Edits to runtime, provider, API, dashboard, CLI, checker scripts, existing tests, the Makefile, CI, or source-artifact files.

## Stop rule

If a future implementation proposal requires any forbidden change, it must stop before modification and use the blocker fallback lane. The proposal must not partially implement forbidden scope.
