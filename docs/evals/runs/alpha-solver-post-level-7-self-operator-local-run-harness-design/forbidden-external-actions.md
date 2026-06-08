# Forbidden External Actions

A future Self Operator local run harness must remain local-only and must not leave any provider-call path inside the harness.

## Forbidden actions

The local run harness design requires:

- no provider calls.
- no hosted model calls.
- no local model execution unless a later explicit local-only implementation lane authorizes it.
- no external API calls.
- no fallback.
- no credential use.
- no billing.
- no dashboard exposure.
- no `/v1/solve` exposure.

The harness must not perform, trigger, or require any of the following actions:

- Provider API calls, hosted model API calls, local-provider API calls, or any other external API calls.
- Hosted model calls, model download, model warmup, or model execution by default.
- Local model execution unless a later explicit local-only implementation lane authorizes it.
- Fallback execution, fallback provider routing, fallback model routing, or fallback remediation.
- Dashboard exposure, dashboard publishing, dashboard screenshot capture, or `/v1/solve` exposure.
- Deployment to cloud, container registry, preview environment, production, staging, or any remote host.
- Browser control, browser automation, profile loading, cookie access, or web navigation.
- Credential use, credential discovery, secret loading, API-key validation, OAuth flow, token refresh, or cloud identity lookup.
- Billing, metering, quota mutation, cost-incurring call, or account-level usage check.
- Evidence promotion, registry promotion, score promotion, benchmark claim, or production-readiness claim.
- External issue creation, pull request creation by the harness, ticket mutation, notification sending, or chat posting.
- Network-based remediation, package installation, remote fetch, dependency update, or any other external action.

## Allowed local-only scope

The harness may only perform bounded local preflights, local artifact capture, and local docs/checker commands that are explicitly allowed by a future implementation lane.

## Required response to forbidden actions

If a forbidden action is requested, the future harness must:

1. Refuse the action.
2. Emit `FORBIDDEN_EXTERNAL_ACTION_REQUESTED`.
3. Capture a local stop-state artifact.
4. Avoid partial execution of the forbidden action.
5. Avoid substituting another external action or fallback path.
6. Preserve the evidence boundary as local and non-promotional.
