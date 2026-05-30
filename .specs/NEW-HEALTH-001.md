---
id: NEW-HEALTH-001
title: Health Check Endpoints
owner: alpha-solver
phase: Next
priority: P2A
track: RES_Infra
spec_version: 1.0
---
# NEW-HEALTH-001 · Health Check Endpoints

## Current status

This spec is a future/placeholder target. It is not the current service runtime contract and is not implemented as written.

Current service health/readiness behavior is implemented in `service/health.py` and wired in `service/app.py`. The current `/health` and `/ready` endpoints use lightweight local probes for the adapter registry and model-provider import availability. They do not check Redis, VectorDB, or perform live provider pings. The compatibility `/healthz` and `/readyz` endpoints remain even lighter service-state probes.

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

## Future implementation note
Any future implementation that adds Redis, VectorDB, or provider-ping checks must be introduced by an approved behavior change and tests. Until then, this file should be read as an intended target only, not as evidence that those dependency checks exist in the running service.
