# Health Endpoint

`alpha.api.health.get_health` returns a dictionary describing the health of the
application and its dependencies. The data is suitable for wiring into a `/health`
HTTP endpoint but no web server is required for tests.

```python
from alpha.api.health import get_health
from fakeredis import FakeRedis

# succeed with all dependencies healthy
get_health(FakeRedis(), vectordb_ok=True, provider_ok=True)
```

The payload has the following shape:

```json
{
  "app": "ok",
  "redis": "ok|down",
  "vectordb": "ok|down",
  "provider": "ok|down",
  "ts": "2024-01-01T00:00:00+00:00"
}
```

Each probe is lightweight so a call should complete in well under 50 ms on a
warm cache.
