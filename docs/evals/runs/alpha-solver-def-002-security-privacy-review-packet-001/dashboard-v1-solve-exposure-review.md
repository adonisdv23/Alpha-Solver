# Dashboard and `/v1/solve` exposure review

Covers: dashboard mounting/exposure, `/v1/solve` exposure surface, and the
auth/rate-limit controls in front of them.

> Boundary note: this review reads the exposure-relevant code only. It does not
> start the service, mount the dashboard, or exercise `/v1/solve`.

## Dashboard exposure

- The dashboard is mounted **fail-closed**. `service/app.py:183-188`
  (`_dashboard_enabled`) requires **both** a non-default
  `ALPHA_DASHBOARD_PASSWORD` and an explicit `ALPHA_DASHBOARD_SECRET_KEY` before
  mounting. Otherwise the routes are not mounted (return 404), a warning is
  logged, and the JSON API keeps working (`service/app.py:200-207`).
- The mount is intentionally minimal: only auth (login/session + CSRF) plus the
  supervised expert-preview page are installed via `_mount_dashboard`
  (`service/app.py:193-196`). The full settings/run/jobs dashboard routes are not
  mounted by the bundled app (comment at `service/app.py:170-182`).
- Dashboard security (auth + CSRF) is installed through
  `dashboard_auth.install_dashboard_security` (`alpha/webapp/routes/auth.py`).

**Control (strong):** fail-closed mounting prevents the dashboard from sitting
behind the well-known default password or an ephemeral signing secret.

**Finding (DASH-1):** The default dashboard password constant is the well-known
literal `alpha-dashboard` (`DEFAULT_DASHBOARD_PASSWORD`,
`alpha/webapp/routes/auth.py:42`). The fail-closed check specifically rejects this
default, which mitigates it; the residual is that the default exists in source and
operators must set a strong password. Tracked as RR-03 (shared with the
`dev-secret` default-credential theme).

## `/v1/solve` exposure surface

- Route: `@app.post("/v1/solve", dependencies=[Depends(rate_limiter)])`
  (`service/app.py:943`). A rate limiter is applied as a route dependency.
- Input is sanitized first: `query = sanitize_query(req.query)`
  (`service/app.py:945`).
- Authentication actually mounted on this route: API-key auth via
  `validate_api_key(request, cfg)`, invoked inside the `rate_limiter` route
  dependency (`service/app.py:927`). `validate_api_key` (`service/security.py:19-27`)
  checks the configured `X-API-Key` header against `cfg.auth.keys` and raises
  `401` on mismatch when auth is enabled. `request.state.api_key` is set on the
  authenticated path (`service/app.py:928`). No JWT or tenant middleware is mounted
  on the bundled app for this route (see the exposure-layer section below).
- Rate limiting: `ServiceRateLimitConfig` (`alpha/core/config.py:29-41`) is
  enabled by default with a sliding window (default 60s window, 120 requests),
  enforced by the same `rate_limiter` dependency, with `record_rate_limit`
  telemetry.
- Failure handling: errors route through `record_safe_out(request.url.path)` and
  SAFE-OUT responses (`service/app.py:894-895`, `922`, and provider error paths),
  so `/v1/solve` does not leak stack traces or raw provider errors to clients.

**Boundary note:** This packet does **not** expose `/v1/solve` and does not change
its exposure. The hard boundary "Do not expose `/v1/solve`" is respected; this is
a read-only assessment of the existing surface.

**Finding (SOLVE-1):** `/v1/solve` is protected by API-key auth + rate limiting,
but the *default* API key is `dev-secret` (see `credential-handling-review.md`,
RR-03). The exposure control is only as strong as the deployment overriding the
default key. CORS in front of the API also defaults to wildcard (RR-01).

## Auth / JWT / tenancy / audit / evidence at the exposure layer

It is important to distinguish controls **actually mounted on the bundled
`/v1/solve` route** from security machinery that **exists elsewhere in the repo
but is not confirmed wired onto this exposure path**. The bundled service app
(`service/app.py`) mounts only `_RequestSpanMiddleware`, `_SimpleTracingMiddleware`,
`CORSMiddleware`, and an `add_request_id` HTTP middleware (`service/app.py:149-166`,
`:884`). It does **not** add `AuthMiddleware`, a JWT middleware, or a tenant
middleware.

### Controls actually mounted on `/v1/solve`

- **Route dependency / rate limiter:** `Depends(rate_limiter)`
  (`service/app.py:943`), enforcing the sliding-window rate limit.
- **API-key auth path:** `validate_api_key(request, cfg)` invoked inside
  `rate_limiter` (`service/app.py:927`; `service/security.py:19-27`) — header
  `X-API-Key` checked against `cfg.auth.keys`, `401` on mismatch when auth is
  enabled.
- **Input sanitization:** `sanitize_query(req.query)` (`service/app.py:945`;
  `service/security.py:30+`).
- **SAFE-OUT / error handling:** the HTTP exception handler and `add_request_id`
  wrapper degrade failures to SAFE-OUT responses via `record_safe_out(...)`
  (`service/app.py:884-922`), so the route does not leak stack traces or raw
  provider errors.

### Controls that exist elsewhere but are NOT confirmed mounted on this route

- **JWT middleware / RS256 verification** — `service/middleware/jwt_middleware.py`,
  `service/middleware/auth_middleware.py`, `service/auth/jwt_utils.py` (RS256-only,
  bounded leeway). Not added to the bundled app; not an active `/v1/solve`
  protection here.
- **Tenant middleware / per-tenant limiter** — `service/middleware/tenant_middleware.py`,
  `service/tenancy/limiter.py`, `service/tenancy/context.py`. Not mounted on the
  bundled app; per-tenant scoping is not enforced on this exposure path.
- **Evidence API controls** — `service/evidence/api.py` is a separate router; it
  is not part of the `/v1/solve` request path.
- **Audit hash-chain machinery** — `service/audit/hash_chain.py` provides
  tamper-evident audit integrity, but it is not invoked by the bundled
  `/v1/solve` handler.

**Finding (SOLVE-2):** The bundled `/v1/solve` route appears to rely on API-key
auth plus rate limiting, **not** mounted JWT/tenant middleware. The JWT and
tenant middleware exist in the repository but are not wired onto this exposure
path in `service/app.py`. Before public/runtime exposure, the intended
auth/tenancy model for `/v1/solve` must be explicitly confirmed or wired. Tracked
in `risk-register.md` as RR-09. This packet does not expose `/v1/solve` and makes
no readiness claim.

## Summary

| Surface | Mounted controls | Exists-but-not-mounted | Residual |
| --- | --- | --- | --- |
| Dashboard | Fail-closed mount, minimal routes, CSRF | — | Default password constant in source (RR-03) |
| `/v1/solve` | API-key auth (`validate_api_key`) + rate limit + input sanitize + SAFE-OUT | JWT middleware, tenant middleware, evidence API, audit hash-chain | Default `dev-secret` key (RR-03); wildcard CORS (RR-01); unconfirmed auth/tenancy model (RR-09) |

The mounted exposure controls are API-key auth and rate limiting with input
sanitization and SAFE-OUT. The residuals are insecure defaults a deployment must
override, the CORS default, and the unconfirmed/unmounted JWT-and-tenancy model
for `/v1/solve`.
