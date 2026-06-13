# Dashboard and `/v1/solve` Map

## `/v1/solve`

- Route: `POST /v1/solve` on `service.app`.
- Input: `SolveRequest` with `query`, optional `strategy`, and optional `context`.
- Controls: API-key validation through the route dependency, sliding-window rate limit, query sanitizer, request ID middleware, SAFE-OUT exception handling, and provider SAFE-OUT paths.
- Provider branch: only when `MODEL_PROVIDER=openai`.
- Local branch: calls the modular/reference `_tree_of_thought` path through `alpha_solver_entry.py`.
- Missing from bundled route: separate JWT middleware, tenant middleware, evidence API, and full dashboard settings route.

## Dashboard

- Bundled mount is fail-closed unless a non-default `ALPHA_DASHBOARD_PASSWORD` and explicit `ALPHA_DASHBOARD_SECRET_KEY` are set.
- Bundled mount includes only dashboard auth and expert preview, not full settings/request/run/jobs routes.
- Expert preview is supervised-only by wording and has a separate live OpenAI guard/cap.
- Standalone dashboard modules are product-shaped and should not be assumed safe merely because they exist.

## Exposure decision

This packet does not expose `/v1/solve` or dashboard routes and does not claim either is ready. Both remain unsafe-to-expose until the intended security model, CORS policy, secret storage, provider disclosure, tenancy behavior, and operational controls are resolved.
