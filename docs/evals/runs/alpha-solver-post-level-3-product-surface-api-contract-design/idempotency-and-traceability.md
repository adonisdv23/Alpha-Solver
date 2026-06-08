# Idempotency and Traceability

## Request identifiers

A future `/v1/solve` contract must define request ID rules before any route exists. Request IDs must support caller correlation, replay review, duplicate detection, and conflict detection. If client-provided request IDs are accepted, the future implementation must reject reuse with materially different normalized payloads.

## Run identifiers

A future implementation must generate a run ID for each accepted attempt that passes initial request parsing. The run ID must be stable in audit artifacts and must not encode secrets, user content, provider credentials, or unredacted sensitive data.

## Decision logs

Every accepted, rejected, refused, blocked, timed-out, or errored request must produce or reference a decision log. Decision logs should record validation outcomes, evidence-boundary decisions, operator-control checks, stop reasons, error categories, redaction actions, and provenance status. Decision logs must be reviewable without provider access and without exposing sensitive payload content.

## Evidence references

A future response must use explicit evidence references when evidence is cited. Evidence references must point to accepted artifacts or accepted packet paths and must not infer missing evidence. Evidence references must preserve the boundary that this API contract packet is docs-only and subordinate to accepted Level 6 product-surface design.

## Idempotency rules

A future idempotency design must define payload fingerprinting, replay windows, retention limits, conflict responses, timeout replay behavior, and blocked-execution replay behavior. Silent re-execution through providers, fallback, billing, or model calls must be prohibited unless separately authorized.
