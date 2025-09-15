---
id: NEW-RATE-001
title: API Rate Limiting
owner: alpha-solver
phase: Next
priority: P2A
track: RES_Infra
spec_version: 1.0
---
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
