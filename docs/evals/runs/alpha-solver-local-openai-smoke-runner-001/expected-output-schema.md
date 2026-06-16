# Expected output schema

The runner prints one sanitized JSON object.

```json
{
  "mode": "local | openai",
  "provider": "ollama | openai",
  "model": "string or null",
  "status": "passed | failed_closed",
  "reason": "string",
  "smoke_evidence_only": true,
  "behavior_evidence": false,
  "quality_evidence": false,
  "readiness_evidence": false,
  "latency_ms": "integer or null",
  "finish_reason": "string or null",
  "usage": "object or null",
  "estimated_cost_usd": "number or null",
  "model_set": "string or null",
  "output_preview": "sanitized bounded string",
  "redaction_status": "sanitized_no_secrets_printed",
  "errors": "array"
}
```

Forced values:

- `smoke_evidence_only: true`
- `behavior_evidence: false`
- `quality_evidence: false`
- `readiness_evidence: false`

The schema is for smoke transport and gating evidence only. It is not a scoring schema.
