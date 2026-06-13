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
- Authentication: the service supports API-key auth (`ServiceAuthConfig`,
  enabled by default, `alpha/core/config.py:17-26`) and JWT/API-key middleware
  (`service/middleware/auth_middleware.py`). `request.state.api_key` is set on the
  authenticated path (`service/app.py:928`).
- Rate limiting: `ServiceRateLimitConfig` (`alpha/core/config.py:29-41`) is
  enabled by default with a sliding window (default 60s window, 120 requests),
  and `record_rate_limit` telemetry is available.
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

- JWT verification is RS256-only with a bounded leeway
  (`service/auth/jwt_utils.py`), reducing algorithm-downgrade risk.
- Tenancy middleware and limiter scope requests per tenant
  (`service/middleware/tenant_middleware.py`, `service/tenancy/limiter.py`).
- Audit entries are tamper-evident (`service/audit/hash_chain.py`).
- The evidence API (`service/evidence/api.py`) is a separate router; callers must
  avoid placing secret material in evidence payloads (operational note).

## Summary

| Surface | Control | Residual |
| --- | --- | --- |
| Dashboard | Fail-closed mount, minimal routes, CSRF | Default password constant in source (RR-03) |
| `/v1/solve` | API-key auth + rate limit + SAFE-OUT + input sanitize | Default `dev-secret` key (RR-03); wildcard CORS (RR-01) |

The exposure architecture is sound; the residuals are insecure defaults that a
deployment must override, plus the CORS default.
