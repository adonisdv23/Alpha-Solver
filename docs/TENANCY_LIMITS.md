# Tenant Rate Limits

The service enforces per-tenant rate limits and optional daily quotas using a
simple in-memory token bucket.  Limits are configured via YAML.

## Configuration

`service/config/tenants.yaml`

```yaml
default:
  rate_per_sec: 5  # tokens refilled each second
  burst: 10        # bucket capacity
  quota_per_day: 100

tenants:
  tenant_a:
    rate_per_sec: 2
    burst: 3
    quota_per_day: 5
```

Each tenant inherits the `default` values with the ability to override any of
them.  `quota_per_day` is optional; omit it to disable quota enforcement.

## Hot Reload

Configuration can be reloaded at runtime without restarting the server:

```python
from service.tenancy.limiter import TenantLimiter
limiter = TenantLimiter("service/config/tenants.yaml")
limiter.reload_config()  # re-read the YAML file
```

Tests trigger reloads by mutating the YAML file and calling `reload_config`.

## Observability

The limiter keeps simple in-memory counters of allowed/denied requests per
tenant (`limiter.metrics`) and a chronological event log (`limiter.events`).
These structures contain no secrets and make it easy to assert tenant isolation
in tests.
