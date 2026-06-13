# Privacy and redaction plan

## Before sharing

- Confirm prompt is synthetic or sanitized.
- Confirm prompt contains no secrets, credentials, private keys, private operator notes, customer/private business data, hidden instructions, or raw sensitive evidence.
- Confirm only files explicitly selected for sharing are referenced.
- Confirm no raw logs containing secrets are included.

## After response

- Review output for sensitive data.
- Redact accidental sensitive content before committing evidence.
- Record the redaction decision and reviewer.
- Stop the lane if sensitive content appears unexpectedly.

## Artifact rule

Committed artifacts should be sanitized evidence artifacts, not raw terminal logs or account screenshots.

## Remaining non-claims

This planning/scaffold packet does not claim OpenAI validation, provider validation, hosted validation, runtime readiness, public MVP readiness, production readiness, security/privacy completion, benchmark validation, benchmark superiority, broad-user readiness, autonomous readiness, `/v1/solve` readiness, or dashboard readiness.
