# Privacy and Redaction Boundaries

## Privacy requirements

Before any `/v1/solve` route exists, a later implementation spec must define:

- what request fields may be logged;
- what request fields must be redacted, hashed, truncated, or omitted;
- what response fields may include user-provided text;
- what evidence references may be returned to callers;
- retention windows for request, run, idempotency, and decision-log records;
- operator access boundaries for raw requests and diagnostics;
- provider payload boundaries for hosted and local execution modes;
- incident handling for accidental secret or personal-data submission.

## Redaction requirements

A future implementation must redact or omit:

- provider API keys, tokens, credentials, cookies, and secrets;
- billing identifiers not explicitly approved for caller exposure;
- hidden reasoning and raw chain-of-thought;
- unrestricted local filesystem paths;
- private user data not needed in the response;
- raw provider request and response payloads unless a later spec allows safe capture;
- raw evidence artifacts containing sensitive material;
- stack traces, environment variables, and internal host details.

## Response disclosure boundary

Responses may describe redaction classes, evidence-reference IDs, and safe diagnostic categories. Responses must not disclose the sensitive values that were redacted. Privacy boundaries apply to success, safe-out, blocked, timeout, and failed responses equally.
