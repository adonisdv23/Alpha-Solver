# Raw Artifact Capture Template

Do not create runtime smoke artifacts in this scaffold lane. This template defines what a later authorized lane should preserve.

## Raw Artifact Fields

- Lane:
- Future implementation PR:
- Future review gate:
- Execution timestamp:
- Operator:
- Endpoint, recorded as localhost or loopback only:
- Exact local model name:
- Finite timeout:
- Hosted fallback disabled confirmation:
- Provider keys absent for local mode confirmation:
- Command used:
- Exit code:
- Raw stdout path:
- Raw stderr path:
- Raw request metadata path:
- Raw response metadata path:
- Failure classification, if any:
- `behavior_evidence=false` preserved:

## Preservation Rule

Raw artifacts must be preserved before sanitization. Sanitized imports must not replace, overwrite, or obscure the raw artifact record.
