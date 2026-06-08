# Candidate Response Schema

## Status

These are candidate `/v1/solve` response envelope fields only. They are not implemented, returned by runtime code, exposed through a route, or populated by provider calls in this packet.

## Candidate response envelope

A future response envelope should define these fields before any route exists:

| Field | Candidate requirement | Notes |
| --- | --- | --- |
| `request_id` | Echoes the accepted request identifier or generated request identifier. | Required for caller correlation. |
| `run_id` | Server-generated run identifier. | Required for audit and replay review. |
| `status` | Machine-readable terminal state. | Examples may include success, refused, blocked, timed out, or error. |
| `answer` | Bounded answer payload when allowed. | Must not imply quality, readiness, or superiority claims. |
| `stop_reason` | Required when no answer is returned or execution stops. | Must distinguish validation, safety, timeout, provider, and blocked-execution cases. |
| `errors` | Structured error array. | Must use the future accepted validation and error taxonomy. |
| `evidence_boundary` | Explicit evidence-boundary statement. | Must preserve local orchestration and design-only boundaries. |
| `evidence_references` | Bounded references to accepted evidence artifacts, if applicable. | Must not invent, promote, or overstate evidence. |
| `decision_log_ref` | Reference to the decision log or audit artifact. | Required even for blocked/refused outcomes. |
| `provenance` | Execution and provider provenance, if applicable and authorized. | Must be absent or explicit when no provider/model is called. |
| `redactions` | Summary of redaction actions. | Must avoid leaking the redacted values. |
| `limits` | Confidence, scope, and claim-boundary limitations. | Required for user-facing outputs. |

## Required response posture

A future response must make blocked, refused, timeout, unsupported, unsafe, and provider-unavailable outcomes explicit. Silent fallback, hidden provider calls, unlogged execution, unsupported claims, and evidence promotion are prohibited.
