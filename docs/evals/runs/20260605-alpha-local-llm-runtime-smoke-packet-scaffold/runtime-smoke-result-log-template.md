# Runtime Smoke Result Log Template

Do not fill this log with execution results in the scaffold lane. This is a future-use template.

## Result Log

- Lane:
- Execution authorized by:
- Runtime implementation PR:
- Execution timestamp:
- Endpoint locality: `<localhost | 127.0.0.1 | ::1>`
- Exact local model name:
- Timeout seconds:
- Hosted fallback disabled: `<yes | no>`
- Provider keys required for local mode: `<no required>`
- Raw artifacts preserved: `<yes | no>`
- Sanitized import completed: `<yes | no>`
- `behavior_evidence=false` preserved: `<yes | no>`
- Outcome: `<blocked | pass | fail>`
- Failure classification:
- Notes:

## Result Constraints

The result log may report only the smoke outcome for the local runtime integration. It must not make readiness, validation, superiority, benchmark, production, MVP, billing, hosted provider, or provider-orchestration claims.
