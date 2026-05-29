# Rate Limiting (NEW-RATE-001)

## Status

`NEW-RATE-001` remains unresolved/partial as a Redis-backed alpha-layer middleware target. It is not implemented as written by the current in-memory service and tenant rate limiting behavior.

The currently implemented in-memory tenant limiter behavior is documented in [`docs/TENANCY_LIMITS.md`](TENANCY_LIMITS.md). Current service API-key rate limiting exists in `service/app.py`. These existing in-memory service and tenant limiters are not the same as the Redis-backed tenant/global token bucket behavior described by `NEW-RATE-001`.

## Related placeholder targets

- `alpha/middleware/ratelimit.py`
- `tests/middleware/test_ratelimit.py`

These placeholder code, test, and documentation targets should not be treated as completed coverage for `NEW-RATE-001`.

## Current implemented references

- `service/app.py`
- `service/tenancy/limiter.py`
- `service/middleware/tenant_middleware.py`
- `tests/test_rate_limits.py`
- `tests/test_api_auth_ratelimit.py`
- `docs/TENANCY_LIMITS.md`

## Future decision needed

Future work must decide whether `NEW-RATE-001` should:

- remain a Redis-backed distributed rate-limit implementation target,
- be revised to document the current in-memory limiters,
- be split into existing limiter documentation and a future Redis implementation,
- or be retired/superseded.
