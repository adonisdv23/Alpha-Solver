# NEW-HEALTH-001 — Health Check Endpoints

## Goal
Expose `/health` with dependency checks for Redis, the vector database and the
model provider.

## Acceptance Criteria
- `/health` returns `{"app": "ok", "redis": "ok|down", "vectordb": "ok|down", "provider": "ok|down", "ts": ...}`.
- Local p95 latency below 50 ms once the cache is warm.
- CI includes 10/10 tests for the endpoint.

## Implementation Notes
- `alpha.api.health.HealthChecker` orchestrates dependency probes and memoises
  the result for a short TTL to satisfy the latency budget.
- The FastAPI router returned by `build_health_router` exposes the `/health`
  route and can be mounted into the service application.
- Probes may be synchronous or asynchronous callables; exceptions or falsey
  return values mark the dependency as `"down"`.

## Testing
- `pytest tests/api/test_health.py`
