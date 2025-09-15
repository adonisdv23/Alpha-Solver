---
id: EPIC_DASH_001
title: Dashboards & Admin
owner: alpha-solver
phase: Next
priority: P2A
track: RES_Dash
spec_version: 1.0
---
## Goal
Ship production-ready dashboards for gates, replay, budget, adapters, reliability SLOs.

## Acceptance Criteria
- All panels render from live metrics; dashboard loads < 2s locally
- Prometheus queries pass validation; 10/10 CI checks
- Obs-card snippet prints per run; README section updated

## Code Targets
- alpha/dashboard/panels.json (proposed)
- alpha/dashboard/alerts.json (proposed)
- tests/dashboard/test_dash_config.py
- docs/DASHBOARDS.md
