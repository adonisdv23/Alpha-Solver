# Privacy and Redaction Boundaries

## Privacy posture

A future `/v1/solve` contract must minimize collected data, reject unnecessary secrets, and record only the data required for validation, traceability, safety review, and operator audit. This packet does not collect data and does not call any route or provider.

## Redaction requirements

Before any route exists, a later authorized lane must define redaction requirements for:

- user task text and optional context;
- metadata supplied by clients or operators;
- request IDs, idempotency keys, run IDs, and decision-log references;
- evidence references and artifact paths;
- provider names, model identifiers, account identifiers, credentials, tokens, and billing identifiers, if any future provider path is separately authorized;
- error messages, validation details, logs, and dashboards;
- retained replay and audit artifacts.

## Non-leakage rules

A future implementation must not expose secrets, credentials, hidden prompts, unredacted sensitive data, private local paths beyond accepted evidence references, or unsupported product claims through answers, errors, logs, dashboards, or traces.

## Retention and review

A future implementation must define retention windows, deletion behavior, operator review access, and audit-export boundaries before collecting request or response data. Retention defaults must be conservative and must preserve the accepted evidence boundary.
