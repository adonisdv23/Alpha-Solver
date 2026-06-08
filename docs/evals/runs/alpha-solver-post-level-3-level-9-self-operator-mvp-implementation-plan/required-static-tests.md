# Required Static Tests

The first code lane must implement static tests before any runtime wrapper or CLI behavior. The tests must be deterministic, offline, and runnable without hosted providers, local models, browser drivers, credentials, deployment targets, or billable services. This packet does not implement or run these tests.

## Required static guardrail coverage

The static test scaffold must fail closed when future Self Operator code introduces any of the following:

| Guardrail | Must fail when code shows |
| --- | --- |
| No provider calls | Hosted provider SDK imports, provider clients, provider endpoints, or model invocation helpers. |
| No hosted model calls | Hosted model clients, hosted inference endpoints, or remote model invocation. |
| No external API calls | Outbound HTTP clients, sockets, webhooks, or non-local service URLs. |
| No credentials | Token env var reads, secret files, credential stores, API key literals, or auth headers. |
| No browser automation | Playwright, Selenium, Puppeteer, CDP, or browser driver usage. |
| No deployment | Deploy CLIs, container push, infrastructure clients, or release commands. |
| No billing | Billing APIs, account APIs, payment clients, or spend-mutation calls. |
| No route exposure | Route decorators or router registration exposing Self Operator behavior, including `/v1/solve` or dashboards. |
| No fallback | Fallback configuration, fallback-enabling code, local-to-provider fallback, or hosted fallback paths. |
| No evidence promotion | Evidence-, readiness-, benchmark-, or score-promotion labels on untrusted output. |
| Approval required | Any side-effect operation lacking explicit operator-approval metadata. |
| Artifact persistence | Missing required artifact fields or persistence locations. |
| Stop-state | Missing, non-terminal, or promotional stop states. |

## Ordering requirement

Static tests are required before any runtime wrapper or CLI behavior. No runtime scaffold, runner, or CLI may be implemented before this static layer exists and passes.

## Staged and unstaged diff checks required before code

Before any code is edited, and again before committing, the future lane must run and record both staged and unstaged diff checks:

- `git status --short` to show staged and unstaged state together.
- `git diff --name-only` for unstaged changes and `git diff --name-only --cached` for staged changes.
- `git diff --check` for unstaged whitespace errors and `git diff --cached --check` for staged whitespace errors.

The future lane must confirm the changed-file set stays inside the approved static-test scope before committing, and must not use a commit to normalize or hide an out-of-scope diff.
