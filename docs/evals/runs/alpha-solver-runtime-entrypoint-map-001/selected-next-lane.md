# Runtime-Map-Local Recommended Follow-up Candidate

This packet names exactly one **runtime-map-local recommended follow-up candidate**:

`ALPHA-SOLVER-RUNTIME-ENTRYPOINT-DOCS-CROSS-LINK-001`

This packet does **not** change the repo-global selected next lane. The repo-global selected next lane remains controlled by `docs/CURRENT_STATE.md` and `docs/LANE_REGISTRY.md`.

At the time of this packet update, those central source-of-truth docs continue to identify `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-002` as the repo-global authoritative selected next lane.

## Purpose

Documentation-only cross-link and operator navigation candidate that would update central entrypoint/current-state documentation to point to this packet while preserving the repo-global selected next lane and clarifying that runtime/public exposure remains unauthorized.

## Why this candidate

The map reveals several product-shaped entrypoints whose status can be misread. A local docs-only cross-link candidate is a low-risk follow-up for this runtime map, but it is not selected as the repo-global next lane and does not supersede the central lane registry.

## Boundaries

- Docs-only.
- No runtime, tests, CI, service, dashboard, provider, model, API, auth, tenancy, CORS, or credential-handling implementation changes.
- No provider calls, tokens, credentials, deployment, dashboard mounting, or `/v1/solve` exposure.
- No runtime consolidation, exposure decision, security implementation, or readiness claim.

## Not selected by this packet as repo-global next work

- `ALPHA-SOLVER-RUNTIME-ENTRYPOINT-DOCS-CROSS-LINK-001` — recommended only as a runtime-map-local follow-up candidate, not as the repo-global selected next lane.
- Auth/CORS remediation lane — valuable but code/config-changing and outside this docs map.
- Dashboard settings secret migration — code-changing and requires operator decision.
- Provider smoke/value experiment — already governed by the central source-of-truth docs and not replaced by this map.
