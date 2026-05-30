---
id: NEW-RATE-001
title: API Rate Limiting
owner: alpha-solver
phase: Next
priority: P2A
track: RES_Infra
spec_version: 1.0
---
# NEW-RATE-001 · API Rate Limiting

## Current status

This spec is a future/placeholder target. It is not implemented as written and is not the current service runtime contract.

Current service API rate limiting is an in-process sliding-window dependency in `service/app.py`. Current tenant limiting is in-memory token-bucket/quota behavior implemented by `service/tenancy/limiter.py` and enforced through `service/middleware/tenant_middleware.py`. Redis-backed tenant/global rate limiting is not implemented.

## Goal
Introduce Redis-backed token bucket rate limiting for tenant/global scopes.

## Acceptance Criteria
Configurable per-tenant and global limits; Redis-backed; overhead <10ms @ p95; 10/10 CI tests green; metrics exported to Prometheus.

## Workspace Recipe
- Start Redis
- Run pytest -q -k "ratelimit"
- Load sample tenants and assert throttle behavior

## Code Targets
alpha/middleware/ratelimit.py (proposed)
tests/middleware/test_ratelimit.py
docs/RATE_LIMITING.md

## CI
Add tests under tests/middleware/test_ratelimit.py; wire into GitHub Actions matrix.

## Future implementation note
Any future Redis-backed tenant/global limiter, SlowAPI integration, distributed quota store, or Prometheus metric expansion must be introduced by an approved behavior change and focused tests. Until then, this file should be read as an intended target only, not as evidence that Redis-backed limiting exists in the running service.
