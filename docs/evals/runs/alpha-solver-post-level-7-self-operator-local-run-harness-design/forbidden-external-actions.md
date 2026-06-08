# Forbidden External Actions

A future Self Operator local run harness must not perform, trigger, or require any of the following actions.

## Forbidden actions

- Provider calls to hosted or local-provider APIs that are not explicitly authorized by a future implementation lane.
- Model execution, model download, or model warmup.
- Dashboard exposure, dashboard publishing, or dashboard screenshot capture.
- Deployment to cloud, container registry, preview environment, production, staging, or any remote host.
- Browser control, browser automation, profile loading, cookie access, or web navigation.
- Credential use, credential discovery, secret loading, API-key validation, OAuth flow, token refresh, or cloud identity lookup.
- Billing, metering, quota mutation, cost-incurring call, or account-level usage check.
- Evidence promotion, registry promotion, score promotion, benchmark claim, or production-readiness claim.
- External issue creation, pull request creation by the harness, ticket mutation, notification sending, or chat posting.
- Network-based remediation, package installation, remote fetch, or dependency update.

## Required response to forbidden actions

If a forbidden action is requested, the future harness must:

1. Refuse the action.
2. Emit `FORBIDDEN_EXTERNAL_ACTION_REQUESTED`.
3. Capture a local stop-state artifact.
4. Avoid partial execution of the forbidden action.
5. Avoid substituting another external action.
6. Preserve the evidence boundary as local and non-promotional.
