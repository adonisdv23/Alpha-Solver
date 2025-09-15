---
id: NEW-HEALTH-001
title: Health Check Endpoints
owner: alpha-solver
phase: Next
priority: P2A
track: RES_Infra
spec_version: 1.0
---
## Goal
Expose /health with dependency checks (Redis, VectorDB, provider ping).
## Acceptance Criteria
/health returns JSON {"app":"ok","redis":"ok|down","vectordb":"ok|down","provider":"ok|down","ts":...}; local p95 <50ms; 10/10 CI tests.
## Workspace Recipe
- Launch app
- curl /health and verify JSON + latency
## Code Targets
alpha/api/health.py (proposed)
tests/api/test_health.py
docs/HEALTH.md
## CI
Add tests under tests/api/test_health.py; assert <50ms in local CI with warm cache.
