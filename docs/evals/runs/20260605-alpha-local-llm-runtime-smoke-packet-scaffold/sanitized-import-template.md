# Sanitized Import Template

Do not import smoke results in this scaffold lane. This template is for a future authorized import after runtime smoke execution.

## Import Metadata

- Source raw artifact packet:
- Redaction reviewer:
- Sanitization timestamp:
- Import authorization:
- Runtime implementation PR:
- Smoke authorization gate:
- Endpoint locality confirmation:
- Exact local model name:
- Finite timeout:
- Hosted fallback disabled:
- Provider keys absent for local mode:
- `behavior_evidence=false` preserved unless explicitly changed by a later evidence-model lane:

## Sanitized Result Summary

- Outcome: `<not-run | blocked | pass | fail>`
- Failure classification:
- Sanitized output summary:
- Sanitized error summary:
- Redactions applied:
- Evidence boundary retained:

## Import Boundary

A sanitized import may document runtime smoke outcome only. It must not claim local model quality, hosted provider evidence, `/v1/solve` readiness, dashboard preview readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, billing readiness, or Alpha superiority.
