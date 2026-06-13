# Boundary Map

| Boundary | Entrypoints affected | Static finding | Exposure note |
|---|---|---|---|
| Auth | `/v1/solve`; middleware stack; dashboard | `/v1/solve` uses API-key validation in `rate_limiter`; separate `AuthMiddleware` supports JWT/API key but is not mounted on bundled app. Dashboard uses session cookies/CSRF. | Public exposure blocked until intended auth model is confirmed and defaults remediated. |
| CORS | FastAPI app | `CORSMiddleware` is installed with configured origins and `allow_credentials=True`; config default origin is `*`. | Unsafe public default. |
| Tenancy | Middleware components; provider telemetry | Tenant middleware and limiter exist and tests exercise them; bundled `/v1/solve` does not mount tenant middleware. | Do not claim tenant isolation for `/v1/solve`. |
| Rate limit | `/v1/solve`; AuthMiddleware; TenantLimiter | `/v1/solve` has sliding-window per API key/client limiter. AuthMiddleware has optional per-tenant rate limit. TenantLimiter exists separately. | Multiple rate-limit systems overlap. |
| Settings/secrets | Dashboard settings route; OpenAI provider env | Dashboard settings route stores provider keys in a file backend; OpenAI provider reads `OPENAI_API_KEY` env. | Do not access secrets; settings route should remain unmounted publicly. |
| Provider | `/v1/solve`; expert preview; `alpha/providers/openai.py` | OpenAI path only when explicit env selects OpenAI; provider client posts to Responses API. Expert preview has extra live-preview guard. | No provider was called. |
| Telemetry | Service logging, metrics, provider telemetry, observability CLI | Request IDs, Prometheus server, OpenTelemetry fallback, provider events/accounting exist. | Telemetry is boundary metadata, not value proof. |
| Evidence | `service/evidence/api.py`, store/collector, eval packets | Evidence router accepts caller-provided manifests/metrics; docs packets are evidence artifacts. | Evidence API must not receive secrets. |
