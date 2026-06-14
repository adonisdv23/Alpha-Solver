# Selected Next Lane

Recommended next lane: operator/security design decision for `/v1/solve` identity and tenancy model.

Decision needed: keep API-key-only with explicit key-to-tenant binding, require JWT for service-to-service use, mount tenant middleware for all `/v1/solve` requests, or keep `/v1/solve` unexposed until a separate API gateway provides those controls.
