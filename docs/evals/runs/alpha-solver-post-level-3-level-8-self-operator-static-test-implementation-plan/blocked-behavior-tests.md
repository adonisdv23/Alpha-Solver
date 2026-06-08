# Blocked Behavior Tests

## Purpose

These planned tests define the first static blocks that should fail before Self Operator code can be trusted.

## Blocked behavior matrix

| Behavior | Static detection target | Finding ID | Expected output |
|---|---|---|---|
| No provider calls | Hosted provider SDK imports, provider clients, provider endpoints, model invocation helpers. | `SELF_OPERATOR_PROVIDER_CALL_BLOCKED` | Test fails and reports path, line, matched provider surface, and remediation. |
| No external API calls | `requests`, `httpx`, sockets, webhooks, non-local URLs, remote service clients. | `SELF_OPERATOR_EXTERNAL_API_BLOCKED` | Test fails and reports the outbound API surface. |
| No credentials | Token env vars, secret files, credential stores, API key literals, auth headers. | `SELF_OPERATOR_CREDENTIAL_ACCESS_BLOCKED` | Test fails and reports the credential access pattern without printing secret values. |
| No browser automation | Playwright, Selenium, Puppeteer, CDP, browser driver binaries. | `SELF_OPERATOR_BROWSER_AUTOMATION_BLOCKED` | Test fails and reports browser automation import or launch site. |
| No deployment | Cloud deploy CLIs, container push, infrastructure clients, release commands. | `SELF_OPERATOR_DEPLOYMENT_BLOCKED` | Test fails and reports deployment command or SDK surface. |
| No billing | Billing APIs, account APIs, payment clients, spend-limit mutation calls. | `SELF_OPERATOR_BILLING_BLOCKED` | Test fails and reports billing/account mutation surface. |
| No route exposure | FastAPI/Flask/Django route decorators or router registration exposing Self Operator behavior. | `SELF_OPERATOR_ROUTE_EXPOSURE_BLOCKED` | Test fails and reports route registration location. |
| No fallback configuration or fallback-enabling code | Fallback flags, fallback provider maps, fallback retry policies, fallback adapters, or configuration keys that enable fallback. | `SELF_OPERATOR_FALLBACK_BLOCKED` | Test fails and reports the fallback-enabling configuration or code path. |
| No local-to-provider fallback paths | Local model failure branches, local solver fallback maps, provider retry-after-local logic, or local-to-hosted escalation paths. | `SELF_OPERATOR_FALLBACK_BLOCKED` | Test fails and reports the local-to-provider fallback branch. |
| No hosted fallback paths | Hosted fallback provider labels, hosted fallback routes, hosted fallback clients, or remote fallback endpoint selection. | `SELF_OPERATOR_HOSTED_FALLBACK_BLOCKED` | Test fails and reports the hosted fallback surface. |
| No evidence/readiness/benchmark/score promotion labels | Labels or enums that mark untrusted output as evidence-promoted, readiness-promoted, benchmark-promoted, score-promoted, accepted, certified, or trusted. | `SELF_OPERATOR_EVIDENCE_PROMOTION_BLOCKED` | Test fails and reports the promotion label category without promoting evidence. |

## Expected failure format

Fallback and evidence-promotion gates carry forward the earlier static coverage expectations for local-to-provider fallback scans and evidence-promotion scans. The first static test layer must fail if Self Operator code introduces fallback configuration, hosted fallback, local-to-provider fallback, evidence-promotion labels, readiness-promotion labels, benchmark-promotion labels, or score-promotion labels. Each blocked behavior should produce a deterministic finding shaped like:

```text
<finding_id> path=<repo-relative-path> line=<line-number> behavior=<blocked-behavior> message=<short-remediation>
```

## Expected pass format

A safe fixture should produce no findings and should not require network, credentials, fallback configuration, promotion labels, browser drivers, deployment tools, billing accounts, or running services.
