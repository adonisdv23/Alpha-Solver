# API exposure gate

## Required conditions

1. Public API auth model is explicitly selected and documented.
2. Every externally reachable API route has authenticated negative tests.
3. Anonymous access is denied except deliberately documented health/static endpoints.
4. Scope/role requirements are documented per route.
5. Rate limits and abuse controls are keyed to authenticated principal/tenant, not only source IP.
6. CORS permits only approved origins and credential semantics are tested.
7. Logs and errors do not reveal tokens, prompts beyond approved policy, secrets, or tenant data.

## Current classification

| Condition | Status | Rationale |
| --- | --- | --- |
| Explicit auth model | Fail now | `/v1/solve` uses an API-key dependency while separate JWT/API-key middleware exists; DEF-002 RR-09 requires a product/security decision before exposure. |
| Route-by-route auth tests | Unknown / requires implementation | This packet did not run route tests and does not prove full external route coverage. |
| Anonymous denial | Unknown / requires implementation | Must be proven for all public routes, including dashboard-adjacent routes if mounted. |
| Scope/role boundaries | Unknown / requires implementation | Middleware supports scopes, but public route scope policy is not captured as exposure evidence. |
| Rate limits | Fail now | Current `/v1/solve` limiter is not sufficient exposure evidence for per-tenant abuse/cost controls. |
| CORS | Fail now | DEF-002 records permissive/default CORS risk. |

## Gate result

No public API exposure is allowed until every condition is pass-now or explicitly accepted by a later operator risk-acceptance lane where acceptance is allowed.
