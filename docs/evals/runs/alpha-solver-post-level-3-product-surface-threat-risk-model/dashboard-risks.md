# Dashboard Risks

## dashboard risks

- A dashboard may expose prompts, responses, traces, provider metadata, cost metadata, user identifiers, credentials, session values, cookies, CSRF tokens, or operational secrets.
- Dashboard access may be mistaken for product readiness, route readiness, provider readiness, quality evidence, or production readiness.
- Screenshots may capture sensitive data or imply unsupported claims if reused in PRs, docs, tickets, or external materials.
- Request metrics may be interpreted as quality, safety, or benchmark results even when they are operational-only signals.

## Access and session risks

- Missing or weak authentication, authorization, session expiry, secret rotation, CSRF protection, or role boundaries.
- Overbroad dashboard permissions that allow data export, reruns, replay, provider calls, or billing-impacting actions.
- Inconsistent local versus hosted dashboard configuration that obscures what data is visible or retained.

## Stop conditions

- Stop if dashboard exposure is required before Level 6 authorizes dashboard scope and controls.
- Stop if screenshots, logs, or exports may include unredacted sensitive data.
- Stop if dashboard metrics are used as evidence-promotion or unsupported product-surface claims.

## Boundary

This packet does not expose, call, test, configure, or modify dashboards. It does not implement dashboard mitigations, route behavior, provider calls, fallback, billing, model inference, benchmark execution, or evidence promotion.
