# Auth, tenancy, and CORS gate

## Pass criteria

- A single public auth model is selected for API and dashboard surfaces, with documented exceptions.
- JWT/API-key/session boundaries are not mixed accidentally across API and dashboard routes.
- Tenant identity is mandatory for billable/provider-backed work.
- Tenant quotas and rate limits are enforced before provider calls.
- CORS has no wildcard credentialed public default and has tests for allowed/denied origins.
- Auth, tenant, and CORS failures produce safe responses and audit events.

## Current classification

| Area | Status | Rationale |
| --- | --- | --- |
| API auth implementation pieces | Pass now for code existence | `AuthMiddleware`, API-key validation, JWT utilities, and `/v1/solve` API-key dependency exist. |
| Public auth decision | Fail now | DEF-002 RR-09 remains open and must be decided/proven. |
| Tenant enforcement | Fail now | Tenant middleware exists but public `/v1/solve` enforcement is not proven in the mounted app. |
| CORS | Fail now | DEF-002 RR-01 remains a must-fix item. |
| Cross-surface separation | Unknown / requires implementation | Need tests proving API credentials cannot operate dashboard routes and dashboard sessions cannot bypass API rules. |

## No-go rule

No external surface can be exposed until public auth, tenant, and CORS behavior is intentionally selected, implemented where needed, and tested.
