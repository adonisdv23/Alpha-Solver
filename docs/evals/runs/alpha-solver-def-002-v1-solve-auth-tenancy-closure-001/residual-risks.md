# Residual Risks

- `/v1/solve` is not production-ready or public-exposure-ready.
- JWT authentication is implemented as reusable middleware but is not mounted on the bundled `/v1/solve` path.
- Tenant middleware is implemented as reusable middleware but is not mounted on the bundled `/v1/solve` path.
- API-key authentication has no tenant identity binding in `service/app.py`; tenant values can be supplied as request metadata.
- Rate limiting on `/v1/solve` is API-key scoped, not tenant-policy scoped.
- Public allowed origins remain an operator deployment decision through `SERVICE_CORS_ORIGINS`.
