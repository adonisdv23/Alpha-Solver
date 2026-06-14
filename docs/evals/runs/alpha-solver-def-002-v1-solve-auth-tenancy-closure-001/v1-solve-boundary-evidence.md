# `/v1/solve` Boundary Evidence

## Route

`service/app.py` defines `@app.post("/v1/solve", dependencies=[Depends(rate_limiter)])` and handler `solve(req: SolveRequest, request: Request)`.

## Active on path

- API key: active through `rate_limiter`, which calls `validate_api_key(request, cfg)`.
- Rate limit: active through `rate_limiter` when `cfg.ratelimit.enabled` is true; scope is API key, not tenant middleware.
- SAFE-OUT: active for `HTTPException` through `http_exception_handler`, returning `SAFE-OUT: ...` and recording safe-out metrics.
- CORS: active globally through `CORSMiddleware`; this branch preserves the PR #532 behavior where origins default to localhost/loopback, credentials are controlled by `ServiceCorsConfig.allow_credentials`, and wildcard origins are rejected when credentials are enabled.
- Logging: active globally through `add_request_id`, which logs request metadata and attaches `X-Request-ID`.
- Provider default: `MODEL_PROVIDER=local` is the default gate, so provider construction/calls are not used unless `MODEL_PROVIDER=openai` is explicitly set.

## Not active / not closed

- `AuthMiddleware` and `JWTAuthMiddleware` are present in `service/middleware/` but are not mounted on the bundled FastAPI app for `/v1/solve`.
- `TenantMiddleware` is present but is not mounted on the bundled FastAPI app for `/v1/solve`.
- Tenant is accepted as request context/header metadata for provider telemetry, but there is no enforced authenticated tenant binding on this path.
