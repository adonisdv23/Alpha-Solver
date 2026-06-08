# Candidate Request Schema

## Status

These are candidate `/v1/solve` request fields only. They are not implemented, validated by runtime code, exposed through a route, or sent to any provider by this packet.

## Candidate top-level fields

A future request schema should define these fields before any route exists:

| Field | Candidate requirement | Notes |
| --- | --- | --- |
| `request_id` | Optional or required client-provided idempotency key, depending on the future authorization lane. | Must not be reused for conflicting payloads. |
| `task` | Required user task text. | Must have size, content, and safety validation. |
| `context` | Optional bounded context supplied by the caller. | Must be redacted and size-limited. |
| `task_family` | Optional declared task family or routing hint. | Must not silently enable unsupported routes. |
| `evidence_boundary` | Required evidence-boundary label. | Must preserve the accepted non-promotional boundary. |
| `execution_mode` | Required operator-selected execution mode. | Must default to safe local/no-provider behavior until separately authorized. |
| `allowed_capabilities` | Optional explicit capability allowlist. | Must fail closed if it implies external, paid, fallback, or unsafe behavior without authorization. |
| `idempotency_key` | Optional retry/replay key. | Must bind to a normalized request fingerprint. |
| `trace` | Optional trace preferences. | Must not disable required audit or decision logs. |
| `redaction_preferences` | Optional caller redaction preferences. | Must not weaken mandatory redaction. |
| `metadata` | Optional bounded caller metadata. | Must exclude secrets, credentials, and unredacted sensitive data. |

## Required validation posture

A future implementation must reject requests that are missing required evidence-boundary, execution-mode, operator-control, safety, authorization, or traceability fields. A future implementation must also reject any request that attempts to force provider orchestration, fallback, billing, readiness promotion, or unsupported route behavior outside a separately accepted implementation scope.
