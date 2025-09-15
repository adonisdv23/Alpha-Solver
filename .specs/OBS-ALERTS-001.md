# CODE SPEC — OBS-ALERTS-001 · Prometheus Alerts + CI Validation (RES_Dash)

## Goal
Implement Prometheus Alerts + CI Validation in track RES_Dash with enforceable tests.

## Acceptance Criteria
- Alert rules for retry_p95>=2, breaker_p95>=100ms, 5xx>1%.
- Rules validate in CI.
- 10/10 tests parse rule files.
- Docs list rule semantics.

## Code Targets
- alpha/dashboard/alerts.json
- tests/dashboard/test_alerts.py
- docs/DASHBOARDS.md

## Template
- dashboards_alerts_v1

## Notes
- Alerts for: retry_p95>=2, breaker_open_p95_ms>=100, http_5xx_ratio>0.01.
- tests/dashboard/test_alerts.py loads alerts.json, checks required keys, and basic expression sanity.
- Update docs/DASHBOARDS.md with alert meanings + how to import.
