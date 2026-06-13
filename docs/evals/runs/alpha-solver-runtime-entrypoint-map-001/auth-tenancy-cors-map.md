# Auth, Tenancy, and CORS Map

| Surface | Auth | Tenancy | CORS | Rate limit | Classification |
|---|---|---|---|---|---|
| `POST /v1/solve` | API key via configured header and `validate_api_key`; default key path exists through config. | No mounted tenant middleware in bundled app; request context may carry tenant/model-set hints but is not enforcement. | App-level CORS applies; default origin is wildcard. | `rate_limiter` dependency. | active / unsafe-to-expose |
| Bundled dashboard preview | Dashboard password/session/CSRF only when fail-closed env requirements pass. | No tenant enforcement found at mount. | App-level CORS applies. | Live preview has provider-specific cap; dashboard auth has lockout. | active support / unsafe-to-expose |
| Standalone dashboard settings/request/run/jobs routers | Depend on caller mounting auth/security. | None intrinsic. | Depends on caller app. | Mock routes have no product rate limit. | unknown / unsafe-to-expose |
| `AuthMiddleware` component | JWT RS256/API-key support with scopes and audit. | Principal includes tenant; optional per-tenant limiter. | N/A. | Optional. | active component / not bundled solve path |
| `TenantMiddleware` component | None by itself. | Requires/extracts tenant and uses `TenantLimiter`. | N/A. | Tenant limiter. | active component / not bundled solve path |
| Evidence API router | No intrinsic auth in router. | None intrinsic. | Depends on caller app. | None intrinsic. | component / unsafe if mounted unauthenticated |

Conclusion: the repository has reusable auth/tenancy components, but `/v1/solve` exposure currently maps to the simpler API-key/rate-limit boundary rather than the full JWT/tenant middleware boundary.
