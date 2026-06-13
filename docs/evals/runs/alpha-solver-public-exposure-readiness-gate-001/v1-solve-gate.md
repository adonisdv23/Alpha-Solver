# `/v1/solve` gate

## Required pass criteria

- Auth: selected API auth model rejects unauthenticated, malformed, revoked, wrong-scope, and wrong-tenant requests.
- Rate limit: rate and quota enforcement is per authenticated tenant/principal with tests for exhaustion and reset behavior.
- Tenancy: tenant identity is mandatory, logged safely, and isolated across requests, model-set selection, quotas, and evidence.
- CORS: browser access is allowed only from approved origins; credential behavior is explicitly tested.
- Logging: request logs include request id and safe metadata only; no secrets, raw tokens, or unapproved prompt content.
- SAFE-OUT: expected error paths return safe, non-sensitive responses.
- Provider-cost boundaries: provider path is opt-in, cost-capped, quota-enforced, and kill-switchable.

## Current classification

| Item | Status | Notes |
| --- | --- | --- |
| Sanitization | Pass now | Handler sanitizes the query before solving. |
| API-key dependency | Pass now for local dependency existence only | Dependency exists, but it is not enough for public exposure. |
| SAFE-OUT for HTTP exceptions | Pass now for that exception class only | Handler wraps HTTP exceptions with SAFE-OUT content. |
| Provider default-off | Pass now for default boundary | Provider branch requires explicit `MODEL_PROVIDER=openai`. |
| Auth model readiness | Fail now | DEF-002 RR-09 remains open. |
| Tenancy readiness | Fail now | Tenant middleware/utilities exist, but public `/v1/solve` tenant enforcement is not captured as mounted/proven. |
| Rate/cost readiness | Fail now | Public abuse and provider-cost caps are not proven. |
| CORS readiness | Fail now | CORS default hardening remains a DEF-002 must-fix lane. |
| Logging/redaction readiness | Unknown / requires implementation | Needs negative tests and prompt-content policy evidence. |

## Gate result

`/v1/solve` exposure is a no-go blocker until RR-09 and related CORS/cost/logging evidence are closed.
