"""Semantic cache with TTL and LFU/LRU eviction policies."""
from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, MutableMapping, Optional, Sequence, Tuple


@dataclass
class CacheEntry:
    """Internal representation of cached values."""

    value: Any
    created_at: float
    expiry: float
    last_access: float
    frequency: int = 1

    def is_expired(self, now: float) -> bool:
        return now >= self.expiry


@dataclass(frozen=True)
class CacheStats:
    """Snapshot of cache counters."""

    size: int
    hits: int
    misses: int
    policy: str
    ttl_seconds: float


class SemanticCache:
    """Semantic cache keyed by embeddings with TTL and eviction policies.

    The cache hashes embedded representations of text queries and maintains
    hit/miss counters as well as TTL-aware eviction. Entries are isolated by
    tenant and role to prevent data bleed across security boundaries.
    """

    def __init__(
        self,
        *,
        max_size: int = 128,
        ttl_seconds: float = 30.0,
        policy: str = "lru",
        embedder: Optional[Callable[[str], Sequence[float]]] = None,
        metrics_hook: Optional[Callable[[Dict[str, Any]], None]] = None,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if max_size <= 0:
            raise ValueError("max_size must be positive")
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        normalised_policy = policy.lower()
        if normalised_policy not in {"lru", "lfu"}:
            raise ValueError("policy must be either 'lru' or 'lfu'")

        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.policy = normalised_policy
        self.embedder = embedder or self._default_embedder
        self.metrics_hook = metrics_hook
        self.clock = clock

        self._entries: MutableMapping[Tuple[str, str, str], CacheEntry] = {}
        self.hits = 0
        self.misses = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def get(self, text: str, *, tenant: str, role: str) -> Optional[Any]:
        """Retrieve a cached value.

        Args:
            text: The query text used to derive the semantic key.
            tenant: Tenant identifier for isolation.
            role: Role identifier for isolation.

        Returns:
            The cached value if present and valid, otherwise ``None``.
        """

        now = self.clock()
        self._purge_expired(now)

        cache_key = self._make_key(text, tenant=tenant, role=role)
        entry = self._entries.get(cache_key)
        if entry is None:
            self._register_miss(cache_key)
            return None
        if entry.is_expired(now):
            del self._entries[cache_key]
            self._register_miss(cache_key)
            return None

        entry.last_access = now
        entry.frequency += 1
        self._register_hit(cache_key)
        return entry.value

    def set(
        self,
        text: str,
        value: Any,
        *,
        tenant: str,
        role: str,
        ttl_seconds: Optional[float] = None,
    ) -> None:
        """Insert or update a cached value."""

        now = self.clock()
        effective_ttl = float(ttl_seconds) if ttl_seconds is not None else self.ttl_seconds
        if effective_ttl <= 0:
            raise ValueError("ttl_seconds must be positive")

        self._purge_expired(now)

        cache_key = self._make_key(text, tenant=tenant, role=role)
        replacing_existing = cache_key in self._entries
        expiry = now + effective_ttl
        entry = CacheEntry(value=value, created_at=now, expiry=expiry, last_access=now)
        self._entries[cache_key] = entry
        self._ensure_capacity(protected_key=None if replacing_existing else cache_key)
        self._emit_metrics("store", cache_key)

    def clear(self) -> None:
        """Remove all cache entries and reset counters."""

        self._entries.clear()
        self.hits = 0
        self.misses = 0
        self._emit_metrics("clear", None)

    def stats(self) -> CacheStats:
        """Return cache statistics."""

        return CacheStats(
            size=len(self._entries),
            hits=self.hits,
            misses=self.misses,
            policy=self.policy,
            ttl_seconds=self.ttl_seconds,
        )

    def snapshot(self) -> Dict[str, Any]:
        """Return a dictionary snapshot for observability hooks."""

        stats = self.stats()
        return {
            "size": stats.size,
            "hits": stats.hits,
            "misses": stats.misses,
            "policy": stats.policy,
            "ttl_seconds": stats.ttl_seconds,
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _make_key(self, text: str, *, tenant: str, role: str) -> Tuple[str, str, str]:
        embedding = self.embedder(text)
        hashed = self._hash_embedding(embedding)
        return tenant, role, hashed

    def _hash_embedding(self, embedding: Sequence[float]) -> str:
        if not isinstance(embedding, Iterable):  # type: ignore[arg-type]
            raise TypeError("embedding must be iterable")
        materialised = list(embedding)  # type: ignore[arg-type]
        payload = ",".join(self._normalise_component(component) for component in materialised)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    @staticmethod
    def _normalise_component(component: Any) -> str:
        if isinstance(component, (float, int)):
            return f"{float(component):.12f}"
        return str(component)

    def _purge_expired(self, now: Optional[float] = None) -> None:
        reference = self.clock() if now is None else now
        expired_keys = [key for key, entry in self._entries.items() if entry.is_expired(reference)]
        for key in expired_keys:
            del self._entries[key]

    def _ensure_capacity(self, protected_key: Optional[Tuple[str, str, str]] = None) -> None:
        if len(self._entries) <= self.max_size:
            return

        while len(self._entries) > self.max_size:
            candidates = [
                (key, entry)
                for key, entry in self._entries.items()
                if key != protected_key or len(self._entries) <= self.max_size
            ]
            if not candidates:
                candidates = list(self._entries.items())

            if self.policy == "lru":
                eviction_key = min(
                    candidates,
                    key=lambda item: (item[1].last_access, item[0]),
                )[0]
            else:  # lfu
                eviction_key = min(
                    candidates,
                    key=lambda item: (item[1].frequency, item[1].last_access, item[0]),
                )[0]
            del self._entries[eviction_key]
            self._emit_metrics("evict", eviction_key)

    def _register_hit(self, cache_key: Tuple[str, str, str]) -> None:
        self.hits += 1
        self._emit_metrics("hit", cache_key)

    def _register_miss(self, cache_key: Tuple[str, str, str]) -> None:
        self.misses += 1
        self._emit_metrics("miss", cache_key)

    def _emit_metrics(self, event: str, cache_key: Optional[Tuple[str, str, str]]) -> None:
        if not self.metrics_hook:
            return
        payload = self.snapshot()
        payload.update({
            "event": event,
            "namespace": None if cache_key is None else f"{cache_key[0]}:{cache_key[1]}",
        })
        try:
            self.metrics_hook(payload)
        except Exception:
            # Metrics hooks must never destabilise cache operations.
            pass

    @staticmethod
    def _default_embedder(text: str) -> Sequence[float]:
        if not text:
            return (0.0, 0.0, 0.0)
        tokens = text.split()
        char_sum = sum(ord(char) for char in text)
        word_lengths = sum(len(token) ** 2 for token in tokens)
        return (
            float(len(tokens)),
            float(len(text)),
            float(char_sum % 10_000),
            float(word_lengths % 10_000),
        )
