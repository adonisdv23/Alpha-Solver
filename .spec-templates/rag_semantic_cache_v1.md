Deterministic RAG broker with semantic cache (TTL + LFU/LRU) and policy guardrails.

### Details
- Provider shim, deterministic citations
- Cache hit/miss counters; exportable metrics

### PR Checklist
- [ ] ≥95% citation accuracy on seed
- [ ] retrieval p95 < 100ms; cache hit ≥60%
- [ ] isolation tests pass (no cross-tenant)
