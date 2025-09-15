"""Tests for the semantic cache implementation."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from alpha.cache.semantic import CacheStats, SemanticCache


class FakeClock:
    def __init__(self, start: float = 0.0) -> None:
        self._now = start

    def __call__(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        self._now += seconds


def test_semantic_cache_metrics_and_ttl() -> None:
    events: List[Dict[str, object]] = []
    clock = FakeClock()
    cache = SemanticCache(
        max_size=4,
        ttl_seconds=5.0,
        metrics_hook=events.append,
        clock=clock,
    )

    assert cache.get("alpha", tenant="tenant-a", role="reader") is None
    cache.set("alpha", {"payload": 1}, tenant="tenant-a", role="reader")
    assert cache.get("alpha", tenant="tenant-a", role="reader") == {"payload": 1}

    clock.advance(6.0)
    assert cache.get("alpha", tenant="tenant-a", role="reader") is None

    stats = cache.stats()
    assert isinstance(stats, CacheStats)
    assert stats.hits == 1
    assert stats.misses == 2
    assert stats.size == 0

    assert events[0]["event"] == "miss"
    assert events[0]["namespace"] == "tenant-a:reader"
    assert events[1]["event"] == "store"
    assert events[2]["event"] == "hit"
    assert events[3]["event"] == "miss"


def test_semantic_cache_eviction_policies() -> None:
    clock = FakeClock()
    cache_lru = SemanticCache(max_size=2, ttl_seconds=50.0, policy="lru", clock=clock)
    cache_lru.set("q1", 1, tenant="t", role="r")
    clock.advance(1.0)
    cache_lru.set("q2", 2, tenant="t", role="r")

    assert cache_lru.get("q1", tenant="t", role="r") == 1
    clock.advance(1.0)
    cache_lru.set("q3", 3, tenant="t", role="r")

    assert cache_lru.get("q2", tenant="t", role="r") is None
    assert cache_lru.get("q1", tenant="t", role="r") == 1
    assert cache_lru.get("q3", tenant="t", role="r") == 3

    clock_lfu = FakeClock()
    cache_lfu = SemanticCache(max_size=2, ttl_seconds=50.0, policy="lfu", clock=clock_lfu)
    cache_lfu.set("a", "A", tenant="t", role="r")
    cache_lfu.set("b", "B", tenant="t", role="r")

    assert cache_lfu.get("a", tenant="t", role="r") == "A"
    assert cache_lfu.get("a", tenant="t", role="r") == "A"
    assert cache_lfu.get("b", tenant="t", role="r") == "B"

    clock_lfu.advance(1.0)
    cache_lfu.set("c", "C", tenant="t", role="r")

    assert cache_lfu.get("a", tenant="t", role="r") == "A"
    assert cache_lfu.get("c", tenant="t", role="r") == "C"
    assert cache_lfu.get("b", tenant="t", role="r") is None


def test_semantic_cache_namespace_isolation() -> None:
    cache = SemanticCache(max_size=4, ttl_seconds=30.0)
    cache.set("shared", 1, tenant="tenant-a", role="reader")
    cache.set("shared", 2, tenant="tenant-b", role="reader")
    cache.set("shared", 3, tenant="tenant-a", role="editor")

    assert cache.get("shared", tenant="tenant-a", role="reader") == 1
    assert cache.get("shared", tenant="tenant-b", role="reader") == 2
    assert cache.get("shared", tenant="tenant-a", role="editor") == 3

    cache.clear()
    assert cache.stats().hits == 0
    assert cache.stats().misses == 0
    assert cache.stats().size == 0
