# Evidence Reference Rules

## Purpose

Evidence references let reviewers connect a run ID, request ID, trace record, decision log, or error log to bounded artifacts without promoting evidence beyond its accepted boundary.

## Rules

1. Evidence references must identify a bounded artifact location, artifact type, and review state.
2. Evidence references must distinguish design documents from execution evidence.
3. Evidence references must not claim product readiness, API readiness, dashboard readiness, provider readiness, billing readiness, benchmark results, or model quality unless a later accepted packet explicitly supports that claim.
4. Evidence references should include enough metadata for reviewers to find the artifact without duplicating sensitive content in logs.
5. Evidence references must preserve redaction state and retention class.
6. Evidence references must not point to private credentials, raw provider payloads, raw billing data, or unredacted personal data.
7. Evidence references should state when an artifact is superseded, blocked, stale, or review-only.

## Required reference shape

A future reference should include:

- evidence reference ID;
- artifact path or controlled storage pointer;
- artifact type;
- run ID, if applicable;
- request ID, if applicable;
- review state;
- redaction state;
- retention class;
- claim boundary.
