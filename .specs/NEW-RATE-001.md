# NEW-RATE-001 · API Rate Limiting

Introduce Redis-backed token bucket rate limiting for tenant and global scopes.

- Configurable per-tenant and global limits.
- Redis-backed with overhead <10ms at p95.
- Prometheus metrics exporting throttle counts and bucket levels.
- Tests cover burst to steady state, per-tenant isolation, and documentation
  example.
