# Budget Stop Conditions

## Purpose

This file defines future budget stop conditions for provider-related paths. It does not implement enforcement, alerts, billing, provider calls, or quota checks.

## Stop condition categories

| Stop condition | Future review meaning |
| --- | --- |
| `stop_missing_budget_policy` | No approved budget policy exists for the provider path. |
| `stop_unknown_cost_state` | Cost state is unknown and no approved fail-open exception applies. |
| `stop_unknown_quota_state` | Quota state is unknown and no approved fail-open exception applies. |
| `stop_budget_limit_reached` | Approved budget threshold has been reached or exceeded. |
| `stop_quota_limit_reached` | Approved quota threshold has been reached or exceeded. |
| `stop_unapproved_provider` | Provider is not approved for the request context. |
| `stop_unapproved_model` | Model label or model version is not approved for the request context. |
| `stop_unapproved_surface` | Surface label is not approved for provider usage. |
| `stop_unapproved_account_label` | Account label is not approved for provider usage. |
| `stop_sensitive_data_risk` | Request or response handling may expose sensitive data outside approved boundaries. |
| `stop_usage_recording_unavailable` | Required usage accounting record cannot be created or linked under future policy. |
| `stop_observability_recording_unavailable` | Required trace or provenance record cannot be created or linked under future policy. |

## Stop behavior expectations

- Stop conditions should be evaluated before provider calls when possible.
- A stopped path should record a bounded stop condition label and must not imply that a provider was called.
- Budget stops should be distinct from provider errors, safety refusals, route failures, and runtime crashes.
- Missing cost, quota, observability, or usage state should default to a review blocker unless a future Level 7-approved exception explicitly says otherwise.
- Stop condition records should be reviewable without raw prompt content, raw response content, provider credentials, payment data, or private identifiers.

## Post-stop review outcomes

| Outcome | Meaning |
| --- | --- |
| `blocked_no_provider_call` | Provider path was blocked before call. |
| `safe_out_no_provider_call` | A safe-out response was used without a provider call. |
| `fallback_local_no_provider_call` | Local fallback was used without a hosted provider call. |
| `manual_review_required` | A reviewer must resolve the blocked state before further action. |
| `superseded_by_level_7` | Future Level 7 decision replaced the stop rule or outcome. |

## Level 7 control

Level 7 controls whether and how any budget stop condition is implemented, enforced, replaced, or rejected.
