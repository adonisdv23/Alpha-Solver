# Residual Risks

- JWT/key-to-tenant binding remains unresolved.
- Whether `TenantMiddleware` should mount on `/v1/solve` remains unresolved.
- Whether `JWTAuthMiddleware` should mount on `/v1/solve` remains unresolved.
- `/v1/solve` should remain unexposed until an operator/security decision resolves the identity and tenancy model.
- Local-only tests are not provider-readiness, public-readiness, production-readiness, or security/privacy-completion evidence.
