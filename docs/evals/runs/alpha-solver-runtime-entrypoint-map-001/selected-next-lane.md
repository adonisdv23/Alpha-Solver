# Selected Next Lane

Exactly one next lane selected by this map:

`ALPHA-SOLVER-RUNTIME-ENTRYPOINT-DOCS-CROSS-LINK-001`

## Purpose

Documentation-only cross-link and operator navigation lane that updates the central entrypoint/current-state docs to point to this packet and clarifies that runtime/public exposure remains unauthorized.

## Why this lane

The map reveals several product-shaped entrypoints whose status can be misread. The lowest-risk follow-up is to make the central docs point to the map before any code consolidation or exposure decision.

## Boundaries

- Docs-only.
- No runtime, tests, CI, service, dashboard, provider, model, or auth code changes.
- No provider calls, tokens, credentials, deployment, dashboard mounting, or `/v1/solve` exposure.
- No readiness claims.

## Not selected

- Auth/CORS remediation lane — valuable but code/config-changing and outside this docs map.
- Dashboard settings secret migration — code-changing and requires operator decision.
- Provider smoke/value experiment — already governed by current lane registry and not replaced by this map.
