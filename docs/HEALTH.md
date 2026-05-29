# Health Endpoint (NEW-HEALTH-001)

## Status

`NEW-HEALTH-001` remains an unresolved alpha-layer placeholder/spec target. It is not implemented as written by the current service-layer health and readiness behavior.

The currently implemented service-layer `/health` and `/ready` behavior is documented in [`docs/HEALTH_READINESS.md`](HEALTH_READINESS.md) and implemented through the service references below. That implemented behavior has different schema and dependency expectations from `NEW-HEALTH-001`.

## Related placeholder targets

- `alpha/api/health.py`
- `tests/api/test_health.py`

These placeholder code, test, and documentation targets should not be treated as completed coverage for `NEW-HEALTH-001`.

## Current implemented references

- `service/health.py`
- `service/app.py`
- `tests/test_health_ready.py`
- `docs/HEALTH_READINESS.md`

## Future decision needed

Future work must decide whether `NEW-HEALTH-001` should:

- wrap the existing service health/readiness behavior,
- revise its schema and dependency expectations,
- implement a new alpha-layer health contract,
- or be retired/superseded.
