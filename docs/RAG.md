# Retrieval-Augmented Generation Broker & Semantic Cache

## Overview

EPIC_RAG_001 introduces a deterministic retrieval broker paired with a semantic
cache that supports TTL-driven eviction, LFU/LRU policies, and policy-aware
routing. The implementation targets local determinism and replay performance by
combining a lightweight provider shim, strict tenant isolation, and observable
retrieval traces.

## Retrieval Broker

The broker (`alpha/retrieval/broker.py`):

- normalises provider outputs into `RetrievedDocument` objects and sorts them by
  descending score (and source identifier for ties) to guarantee deterministic
  citations;
- enforces tenant/role policy constraints through the `PolicyGuard`
  abstraction (with a `StaticPolicyGuard` allow-list implementation);
- integrates with the semantic cache to reuse responses via semantic keys that
  include the requested `top_k` size;
- emits an observability card per query in the format
  `route=rag path=<...> cache_hit=<0/1> latency_ms=<int> provider=<name> cache_hits=<n> cache_misses=<n> cache_size=<n>`
  so replay diagnostics capture retrieval path and cache statistics.

The broker accepts any provider that implements the simple `ProviderShim`
protocol (`name` attribute and `retrieve` method). The included tests ship with
an in-memory seed provider that demonstrates the minimal contract.

## Semantic Cache

The semantic cache (`alpha/cache/semantic.py`) delivers:

- deterministic hashing of embedded query text (default embedder derives a
  stable vector from token counts and character features);
- TTL support for every entry (configurable globally and per write);
- both LRU and LFU eviction strategies with optional metrics hooks;
- counters for hits/misses plus namespace scoping (`tenant:role`) to prevent
  cross-tenant leakage.

Consumers can extract stats via `cache.stats()` or a dictionary snapshot for
observability/metrics pipelines. Hooks receive event payloads for `miss`,
`store`, `hit`, `evict`, and `clear` transitions.

## Workspace Recipe

Local and CI validation focuses on the dedicated retrieval test suite:

```bash
pytest tests/retrieval
```

The tests exercise:

- ≥95% citation accuracy against the bundled seed dataset;
- retrieval latency p95 below 100 ms (measured with `time.monotonic()`);
- ≥60% cache hit rate on replay of the seed queries;
- strict tenant isolation and policy enforcement guardrails.

## Metrics & Observability

The observability card emitted by the broker surfaces cache hits/misses and
latency in-line with the EPIC acceptance criteria. Cache metrics hooks allow
exporting counters to custom telemetry sinks without coupling cache lifecycle to
metrics delivery.
