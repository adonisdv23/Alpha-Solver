---
id: EPIC_RAG_001
title: RAG & Semantic Cache Pack
owner: alpha-solver
phase: Next
priority: P2A
track: RES_RAG
spec_version: 1.0
---
## Goal
Deterministic RAG broker with semantic cache (TTL + LFU/LRU) and policy guardrails.

## Acceptance Criteria
- Citation accuracy ≥95% on seed; retrieval p95 < 100ms (local); cache hit rate ≥60% on replay
- Strict tenant/role isolation with policy enforcement
- Obs-card prints retrieval path + cache stats
- 10/10 CI tests covering retrieval + cache behaviour

## Workspace Recipe
- `pytest tests/retrieval`

## Code Targets
- alpha/retrieval/broker.py
- alpha/cache/semantic.py
- tests/retrieval/test_broker.py
- tests/retrieval/test_cache.py
- docs/RAG.md

## Notes
- Provider shim must yield deterministic citations (stable ordering, source ids)
- Cache exposes hit/miss counters and eviction metrics via hook
- Replay metrics measured with `time.monotonic()` in tests
