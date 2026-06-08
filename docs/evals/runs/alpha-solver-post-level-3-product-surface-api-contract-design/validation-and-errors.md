# Validation and Errors

## Validation posture

A future `/v1/solve` implementation must validate before execution and fail closed when required controls, provenance, evidence-boundary labels, authorization, audit identifiers, or opt-in settings are absent. This packet does not implement those validators.

## Required error categories

A future error taxonomy must include at least these categories:

| Category | Required meaning | Required handling posture |
| --- | --- | --- |
| `invalid_input` | The request is malformed, oversized, contradictory, missing required fields, or contains disallowed field values. | Reject before execution. |
| `missing_evidence` | Required evidence references, evidence-boundary labels, or accepted source artifacts are absent. | Reject or block without promoting claims. |
| `unsupported_route` | The request attempts a route, capability, task family, or execution mode that is not accepted. | Reject without fallback. |
| `unsafe_claim` | The request or response would create unsupported quality, superiority, readiness, provider, billing, or production claims. | Refuse or block with an evidence-boundary explanation. |
| `provider_unavailable` | A separately authorized provider path is unavailable. | Return explicit unavailability; do not silently fallback. |
| `timeout` | A bounded execution or validation deadline is exceeded. | Stop and return traceable timeout details. |
| `blocked_execution` | Operator controls, policy, safety gates, budget gates, or environment restrictions block execution. | Stop before execution or continue only with a separately accepted safe path. |

## Error response requirements

Every error response should include request correlation, run correlation if allocated, a machine-readable category, a human-readable safe explanation, an evidence-boundary statement, and a decision-log reference. Error responses must not leak secrets, hidden prompts, provider credentials, unredacted sensitive data, or unsupported product claims.
