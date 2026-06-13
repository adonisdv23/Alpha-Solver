# Alpha Solver Runtime Entrypoint Map 001

Lane: `ALPHA-SOLVER-RUNTIME-ENTRYPOINT-MAP-001`

Verdict: `RUNTIME_ENTRYPOINT_MAP_CAPTURED`

## Purpose

This packet maps Alpha Solver runtime, service, dashboard, provider, API, CLI, and portable-contract entrypoints before any architecture consolidation or public exposure decision.

## Scope

Read-only documentation only. No runtime code, tests, CI, service/dashboard/provider/model/auth code, credentials, tokens, provider calls, deployment, or `/v1/solve` exposure were changed or exercised.

## Files in this packet

| File | Purpose |
|---|---|
| `entrypoint-inventory.md` | Product/runtime entrypoints and status classification. |
| `boundary-map.md` | Auth, CORS, tenancy, rate-limit, settings, secret, provider, telemetry, and evidence boundaries. |
| `provider-call-paths.md` | Static provider-call paths and non-call paths. |
| `auth-tenancy-cors-map.md` | Exposure-layer auth, tenancy, and CORS wiring. |
| `dashboard-and-v1-solve-map.md` | Dashboard mounting and `/v1/solve` surface map. |
| `duplicate-surface-map.md` | Overlapping `alpha/`, `service/`, dashboard, portable, and CLI surfaces. |
| `consolidation-candidates.md` | Staged consolidation candidates only; no implementation authorization. |
| `do-not-consolidate-yet.md` | No-touch zones until value proof and security boundaries are proven. |
| `selected-next-lane.md` | Exactly one low-risk next lane selected by this packet. |
| `evidence-boundary.md` | Evidence reviewed and claim boundaries. |
| `non-actions.md` | Explicit non-actions and safety confirmations. |

## Summary

The repository contains multiple runtime-shaped surfaces: the FastAPI service app, `/v1/solve`, a fail-closed mounted dashboard preview, standalone dashboard route modules, the modular/reference `alpha_solver_entry.py` and `alpha-solver-v91-python.py` CLI/import path, the portable monolith contract, provider adapters, evidence API router, middleware components, config/settings paths, and observability dashboards. These are not one consolidated public product surface.

The highest-risk boundaries remain public exposure prerequisites: default API key and CORS defaults, `/v1/solve` not using the separate JWT/tenant middleware stack, dashboard settings routes capable of storing provider keys when mounted outside the bundled fail-closed service path, and OpenAI provider calls gated by environment but live-capable when explicitly enabled.
