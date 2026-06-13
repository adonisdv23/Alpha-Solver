# Entrypoint Inventory

Status terms: **active** means importable/mounted in current code or directly executable; **test-only** means primarily exercised in tests; **docs-only** means documentation/observability artifact only; **legacy** means reference/back-compat path; **unknown** means runtime role needs confirmation; **unsafe-to-expose** means do not expose without remediation/explicit operator decision.

| Entrypoint / surface | Evidence | Classification | Notes |
|---|---|---:|---|
| FastAPI app object `service.app:app` | `service/app.py` constructs `FastAPI`, middleware, health/OpenAPI-ish routes, dashboard conditional mount, and `/v1/solve`. | active / unsafe-to-expose | Runnable app surface, but not public-ready. |
| `POST /v1/solve` | `service/app.py` route depends on `rate_limiter`, sanitizes query, then branches to OpenAI provider only when `MODEL_PROVIDER=openai`; otherwise local ToT. | active / unsafe-to-expose | Main product API shape; exposure remains unauthorized. |
| Dashboard bundled mount | `service/app.py` mounts only dashboard auth plus `expert_preview` when non-default dashboard password and explicit secret are configured. | active / unsafe-to-expose | Fail-closed by default; preview can become provider-backed if env enables it. |
| `alpha/webapp/routes/auth.py` | Login/session/CSRF middleware and router. | active support / unsafe-to-expose alone | Safe only when mounted with explicit password/secret expectations. |
| `alpha/webapp/routes/expert_preview.py` | `/dashboard/expert-preview` route and live OpenAI preview guard. | active support / unsafe-to-expose | Bundled dashboard route; guarded but live-capable. |
| `alpha/webapp/routes/settings.py` | Settings UI for provider API keys with file-backed secrets and audit log. | unknown / unsafe-to-expose | Not mounted by bundled service app; risky if mounted elsewhere. |
| `alpha/webapp/routes/requests.py`, `jobs.py`, `run.py` | Mock request/job/demo routes. | unknown / test/demo-only | Not mounted by bundled service app; can look product-like. |
| `alpha_solver_entry.py` | Imports `alpha-solver-v91-python.py`, exposes `AlphaSolver`, `_tree_of_thought`, `get_solver`. | active legacy/reference | Used by service local fallback and tests. |
| `alpha-solver-v91-python.py` | `_tree_of_thought` implementation and CLI `main()`. | active legacy/reference | Direct CLI executable; emits JSON. |
| `alpha_solver_portable.py` | Portable spec monolith with argparse and behavior contract. | active portable-contract / unsafe-to-consolidate | Canonical standalone behavior contract, not a service API. |
| `alpha/providers/openai.py` | Live OpenAI Responses API client using `OPENAI_API_KEY`. | active provider path / unsafe-to-call here | Tests may inject fake clients; real call requires explicit env/key. |
| `alpha/providers/fake.py` | Fake provider. | test-only | Local deterministic provider test utility. |
| `service/evidence/api.py` | Separate evidence router with `/evidence` endpoints. | active component / unknown mount | Router exists; not mounted on `service.app` in inspected path. |
| Auth/JWT/API-key middleware modules | `service/middleware/auth_middleware.py`, `jwt_middleware.py`, `service/auth/*`. | active component / unknown mount | Exists but not wired onto bundled `/v1/solve`. |
| Tenant middleware / limiter | `service/middleware/tenant_middleware.py`, `service/tenancy/*`. | active component / unknown mount | Tested separately; not mounted on bundled `/v1/solve`. |
| Prometheus/Grafana dashboards | `dashboards/*`, `infrastructure/grafana/...`. | docs/ops-only | Observability artifacts, not request entrypoints. |
| Tests hitting service/dashboard/provider/portable | `tests/test_api_auth_ratelimit.py`, `tests/test_client_sdk.py`, `tests/test_local_llm_provider_adapter.py`, provider/security tests. | test-only | Validate slices; do not imply public readiness. |
