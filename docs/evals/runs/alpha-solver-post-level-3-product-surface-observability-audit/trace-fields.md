# Trace Fields

## Required trace field families

Future product-surface trace records should be designed around these field families before implementation:

| Field family | Requirement |
| --- | --- |
| `run_id` | Stable run ID for an evaluation, readiness review, operator-controlled session, or release-readiness packet when applicable. |
| `request_id` | Stable request ID for a single product-surface attempt, generated without embedding user content. |
| `trace_id` | Stable trace identifier that links trace records for one request path. |
| `parent_trace_id` | Optional parent trace identifier for nested, retried, replayed, or delegated work. |
| `timestamp_utc` | UTC timestamp for record creation. |
| `surface` | Product surface name or placeholder category, such as API, dashboard, CLI bridge, or operator tool. |
| `actor_type` | Bounded actor category, such as operator, reviewer, service, or unauthenticated user, without personal identifiers unless approved. |
| `decision_log_ref` | Reference to any decision log entry produced for the request. |
| `error_log_ref` | Reference to any error log entry produced for the request. |
| `evidence_ref` | Reference to bounded evidence artifacts, if any, using the evidence-reference rules. |
| `redaction_state` | Status indicating whether sensitive content was absent, redacted, summarized, or blocked from capture. |
| `retention_class` | Retention boundary category assigned before storage. |
| `review_state` | Reviewability status, such as pending review, reviewed, blocked, or superseded. |

## Identifier rules

- A run ID must not encode user content, secrets, prompt text, provider credentials, billing data, or private operator notes.
- A request ID must be unique enough for review and correlation without exposing sensitive content.
- A trace record must not rely on raw payload capture as its only review mechanism.
- If no run ID applies, the trace record should explicitly state that the request was not part of a run-scoped packet.
