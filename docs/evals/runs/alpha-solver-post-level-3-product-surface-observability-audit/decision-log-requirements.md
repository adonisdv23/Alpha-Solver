# Decision Log Requirements

## Purpose

A decision log records why a future product-surface request was allowed, blocked, routed, retried, escalated, rejected, or marked reviewer-blocked.

## Required fields

- Decision log entry ID.
- run ID when the request is part of a run-scoped packet.
- request ID.
- trace ID.
- decision type.
- decision outcome.
- policy or gate consulted.
- bounded rationale suitable for reviewer inspection.
- evidence reference when the decision relies on a reviewed artifact.
- reviewer state when human review is required.
- redaction status.
- UTC timestamp.

## Requirements

- Decision logs must not include raw secrets, raw credentials, provider tokens, payment data, or unredacted personal data.
- Decision logs should identify blocked claims separately from blocked execution.
- Decision logs should distinguish automated decisions from reviewer decisions.
- Decision logs should be reviewable without running models, calling providers, or reproducing billing events.
