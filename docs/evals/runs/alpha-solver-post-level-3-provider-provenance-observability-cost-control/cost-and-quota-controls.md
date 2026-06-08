# Cost and Quota Controls

## Purpose

This file defines future cost and quota labels for review. It does not implement budget enforcement, billing, quota checks, dashboards, alerts, or provider calls.

## Cost labels

| Label | Meaning |
| --- | --- |
| `cost_not_applicable` | No provider path or billable path applies. |
| `cost_not_recorded` | Cost data was not captured or approved for retention. |
| `cost_estimated_local` | A local estimate exists and is not provider-reported billing data. |
| `cost_provider_reported` | Provider-reported cost data exists and is approved for retention. |
| `cost_reconciled` | Cost data has been reconciled against an approved source. |
| `cost_disputed` | Cost data conflicts across sources or remains under review. |
| `cost_blocked_sensitive` | Cost data exists or may exist but is blocked from normal review due to sensitivity. |

## Quota labels

| Label | Meaning |
| --- | --- |
| `quota_not_applicable` | No provider quota applies. |
| `quota_not_checked` | Quota was not checked or no approved quota source exists. |
| `quota_available` | Quota appears available according to an approved source. |
| `quota_near_limit` | Quota is approaching a future approved threshold. |
| `quota_exhausted` | Quota appears exhausted according to an approved source. |
| `quota_unknown` | Quota state cannot be determined. |
| `quota_blocked_sensitive` | Quota details are blocked from normal review due to sensitivity. |

## Control labels

| Label | Meaning |
| --- | --- |
| `budget_control_not_configured` | No approved budget control exists. |
| `budget_control_dry_run` | Control would record a decision but would not enforce a stop. |
| `budget_control_enforced` | Control is approved for enforcement by a future implementation. |
| `budget_control_bypassed` | Control was bypassed under an approved exception path. |
| `budget_control_failed_closed` | Missing or invalid budget state caused provider path blocking. |
| `budget_control_failed_open` | Missing or invalid budget state allowed continuation under an approved exception path. |

## Cost and quota safety rules

- Cost and quota labels must not include payment card details, billing account identifiers, secrets, provider credentials, or private user identifiers.
- Labels must separate estimates from provider-reported or reconciled values.
- Cost and quota labels must not be used as promotional cost-savings claims.
- Unknown quota or cost state should be visible to reviewers and must not be silently treated as available budget.

## Level 7 control

Level 7 controls whether and how these cost and quota controls are used.
