# Observability Principles

## Audit-first before product surface

Any future product-surface implementation should be reviewable from stable identifiers, bounded records, and evidence references before it is exposed to users. Observability must support reconstruction of what happened without collecting unnecessary sensitive content.

## Required principles

1. Every product-surface attempt should be associated with a run ID when it belongs to an evaluation, review, release-readiness, or operator-controlled run.
2. Every externally meaningful user or operator attempt should be associated with a request ID.
3. Trace records should connect run ID, request ID, decision log entries, error log entries, and evidence references without requiring reviewers to inspect raw sensitive payloads.
4. Logs should preserve enough context for reviewability while respecting redaction and retention boundaries.
5. Decision logs should explain why a routed, blocked, allowed, retried, or escalated outcome occurred.
6. Error logs should distinguish system failures, validation failures, policy blocks, provider failures, timeout conditions, and reviewer-blocked states.
7. Evidence references should point to bounded artifacts and should not become evidence promotion claims by themselves.
8. Level 6 controls whether and how this packet is used.

## Non-goal

This document does not implement logging or alter runtime behavior.
