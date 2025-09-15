# Health Endpoint

The Alpha Solver exposes a JSON health endpoint that reports the status of its
critical dependencies. The endpoint is designed for infrastructure and
observability systems that need to quickly decide whether the API is ready to
serve traffic.

## Route

- `GET /health`

## Response Schema

```json
{
  "app": "ok",
  "redis": "ok",
  "vectordb": "ok",
  "provider": "ok",
  "ts": "2024-03-22T18:25:43.511Z"
}
```

Key fields:

- `app` – Aggregated service status. The value is `"ok"` when all dependency
  probes succeed, otherwise `"down"`.
- `redis` – Result of the Redis connectivity probe (`ping` style check).
- `vectordb` – Result of the vector database probe.
- `provider` – Result of the configured model provider probe.
- `ts` – ISO-8601 UTC timestamp indicating when the health result was produced.

## Implementation Notes

The endpoint is backed by `alpha.api.health.HealthChecker`. Probes are provided
as callables and may be synchronous or `async def`. Failures (exceptions or
falsey return values) are mapped to the string `"down"`.

To keep tail latencies low, the checker memoises the dependency results for a
short window (default 5 seconds). With a warm cache, health responses complete
well within the 50 ms latency target.

### Example Integration

```python
from fastapi import FastAPI
from alpha.api.health import HealthChecker, build_health_router

app = FastAPI()
checker = HealthChecker(redis_client.ping, vectordb.health, provider.ping)
app.include_router(build_health_router(checker))
```

## Testing

Unit tests for the health endpoint live in `tests/api/test_health.py`. They
exercise the payload schema, failure handling and warm-cache latency budget.
