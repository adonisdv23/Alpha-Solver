# Error Log Requirements

## Purpose

An error log records failure conditions for future product-surface requests without turning failures into promotional evidence or exposing sensitive payloads.

## Required fields

- Error log entry ID.
- run ID when applicable.
- request ID.
- trace ID.
- error category.
- severity.
- bounded message.
- component or surface category.
- detected-at UTC timestamp.
- recovery or fallback state.
- related decision log reference, if any.
- evidence reference, if any.
- redaction status.
- retention class.

## Error categories

Future implementation design should distinguish at least:

- validation failure;
- policy or safety block;
- authentication or authorization failure;
- provider unavailable;
- provider timeout;
- local runtime unavailable;
- route unavailable;
- dashboard surface unavailable;
- malformed request;
- reviewer-blocked state;
- retention or redaction violation.

## Requirements

- Error logs must not include raw prompt content unless a later accepted policy explicitly allows and redacts it.
- Error logs must not include secrets, provider keys, billing account identifiers, session tokens, or raw personal data.
- Error logs must be sufficient for reviewers to determine whether the issue is product-surface behavior, provider behavior, local runtime behavior, policy behavior, or documentation-only blocker state.
