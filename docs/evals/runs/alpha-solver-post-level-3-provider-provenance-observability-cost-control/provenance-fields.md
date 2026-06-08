# Provenance Fields

## Purpose

These fields define a future documentation contract for provider provenance and response provenance. They are not implemented by this packet.

## Provider provenance field families

| Field family | Future requirement |
| --- | --- |
| `provider_name` | Bounded provider label selected from an approved provider registry or explicit `local_only` / `unknown_not_called` value. |
| `provider_endpoint_class` | Coarse endpoint class, such as local runtime, hosted API, proxy, gateway, or disabled provider path. |
| `provider_region_label` | Non-sensitive region or locality label when approved; otherwise `not_recorded`. |
| `provider_account_label` | Non-billing account label or internal alias that does not expose credentials, payment details, or private identifiers. |
| `model_label` | Provider-facing or local model label used for routing review, without implying benchmark quality or promotional performance. |
| `model_version_label` | Version, digest, or release label when available and approved; otherwise explicit `not_available` or `not_recorded`. |
| `provider_capability_label` | Bounded capability category used for routing review, such as text, tool-use, embedding, or disabled. |
| `provider_call_state` | Explicit state such as not_called, blocked_before_call, attempted, succeeded, failed, retried, or unknown. |
| `provider_response_id` | Provider response identifier when approved for retention; otherwise redacted, omitted, or unavailable. |
| `provider_error_class` | Bounded error category for failed or blocked provider paths without raw sensitive payloads. |
| `provider_policy_ref` | Reference to the policy, allowlist, or block rule that governed the provider path. |

## Request tracing field families

| Field family | Future requirement |
| --- | --- |
| `run_id` | Stable run or packet identifier when a request is tied to a reviewed run. |
| `request_id` | Stable request identifier that does not embed prompt text, user content, secrets, or billing data. |
| `trace_id` | Stable trace identifier for all records in one request path. |
| `parent_trace_id` | Optional parent identifier for retries, delegated calls, or nested operations. |
| `timestamp_utc` | UTC timestamp for trace record creation. |
| `surface_label` | Bounded surface label such as CLI, API, dashboard, bridge, evaluator, or operator tool. |
| `route_decision_label` | Bounded routing outcome such as local_only, hosted_allowed, blocked, fallback, retry, or safe_out. |
| `redaction_state` | Explicit state showing whether sensitive content was absent, redacted, summarized, hashed, omitted, or blocked. |

## Response provenance field families

| Field family | Future requirement |
| --- | --- |
| `response_id` | Internal response identifier generated without embedding user content. |
| `response_source_label` | Bounded source label such as local_solver, local_model, hosted_provider, cached_response, safe_out, or blocked_no_response. |
| `response_provider_link` | Link to provider provenance record when a provider path was attempted and approved for retention. |
| `response_trace_link` | Link to trace identifiers needed for review. |
| `response_redaction_state` | Redaction state for retained response content or summaries. |
| `response_evidence_state` | Non-promotional evidence status, such as design_only, raw_unreviewed, reviewed_non_promotional, blocked, or superseded. |
| `response_claim_boundary` | Boundary label stating that response provenance does not prove quality, safety, latency, cost savings, or production readiness. |

## Usage provenance field families

| Field family | Future requirement |
| --- | --- |
| `usage_record_state` | Explicit state such as not_created, estimated, provider_reported, normalized, reconciled, disputed, or blocked. |
| `input_unit_count` | Future input usage count only when approved and sourced; otherwise absent or not_recorded. |
| `output_unit_count` | Future output usage count only when approved and sourced; otherwise absent or not_recorded. |
| `usage_unit_type` | Bounded unit label, such as tokens, characters, requests, seconds, tool calls, or provider_native_unit. |
| `usage_source_label` | Source of usage data, such as provider_report, local_estimate, runtime_meter, dashboard_export, or not_available. |
| `usage_confidence_label` | Bounded confidence label such as exact_provider_reported, estimated, partial, stale, or unknown. |

## Field safety rules

- Provider provenance fields must not store secrets, API keys, raw credentials, payment details, private account identifiers, or full prompt/response content unless later approved by Level 7.
- Missing data must be represented explicitly as not available, not recorded, blocked, redacted, or not called.
- Field names are design labels only and do not create schemas, logs, provider adapters, dashboards, or usage records.
- Level 7 controls whether and how these provenance fields are used.
