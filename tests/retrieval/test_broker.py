"""Tests for the retrieval broker and seed dataset acceptance criteria."""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from alpha.cache.semantic import SemanticCache
from alpha.retrieval.broker import (
    BrokerResponse,
    PolicyDeniedError,
    RetrievedDocument,
    RetrievalBroker,
    StaticPolicyGuard,
)

TENANT = "tenant-alpha"
ROLE = "researcher"


@dataclass
class SeedQuery:
    query: str
    prefix: str


SEED_QUERIES: Sequence[SeedQuery] = (
    SeedQuery("alpha energy roadmap", "energy"),
    SeedQuery("beta risk controls", "risk"),
    SeedQuery("gamma product faq", "product"),
    SeedQuery("delta release checklist", "release"),
    SeedQuery("epsilon incident review", "incident"),
    SeedQuery("zeta sla summary", "sla"),
    SeedQuery("eta observability guide", "observability"),
    SeedQuery("theta data retention", "data"),
    SeedQuery("iota compliance matrix", "compliance"),
    SeedQuery("kappa outage drill", "outage"),
)


def _build_seed_dataset() -> Tuple[Dict[str, List[RetrievedDocument]], Dict[str, List[str]]]:
    dataset: Dict[str, List[RetrievedDocument]] = {}
    expectations: Dict[str, List[str]] = {}
    for index, seed in enumerate(SEED_QUERIES, start=1):
        primary_score = 0.92 + index * 0.004
        summary_score = primary_score - 0.045
        support_score = summary_score - 0.06
        docs = [
            RetrievedDocument(
                source_id=f"{seed.prefix}-support-{index:02d}",
                content=f"supporting note for {seed.query}",
                score=support_score,
                metadata={"section": "support", "topic": seed.prefix},
            ),
            RetrievedDocument(
                source_id=f"{seed.prefix}-primary-{index:02d}",
                content=f"primary guidance on {seed.query}",
                score=primary_score,
                metadata={"section": "primary", "topic": seed.prefix},
            ),
            RetrievedDocument(
                source_id=f"{seed.prefix}-summary-{index:02d}",
                content=f"summary for {seed.query}",
                score=summary_score,
                metadata={"section": "summary", "topic": seed.prefix},
            ),
        ]
        # Intentionally shuffle order to confirm broker sorting logic.
        dataset[seed.query] = [docs[0], docs[2], docs[1]]
        expectations[seed.query] = [docs[1].source_id, docs[2].source_id]
    return dataset, expectations


class SeedProvider:
    """Minimal deterministic provider for tests."""

    name = "seed-provider"

    def __init__(self, dataset: Dict[str, List[RetrievedDocument]]) -> None:
        self._dataset = dataset
        self.calls: List[Tuple[str, str, str, int]] = []

    def retrieve(
        self,
        *,
        query: str,
        top_k: int,
        tenant: str,
        role: str,
    ) -> Iterable[RetrievedDocument]:
        self.calls.append((query, tenant, role, top_k))
        return list(self._dataset.get(query, ()))


def _percentile(values: Sequence[float], percentile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    rank = max(0, math.ceil(percentile * len(ordered)) - 1)
    return ordered[rank]


def test_broker_seed_dataset_metrics() -> None:
    dataset, expectations = _build_seed_dataset()
    cache = SemanticCache(max_size=64, ttl_seconds=120.0)
    provider = SeedProvider(dataset)
    obs_events: List[str] = []
    policy = StaticPolicyGuard({TENANT: [ROLE], "tenant-beta": [ROLE]})
    broker = RetrievalBroker(
        provider,
        cache,
        policy=policy,
        obs_sink=obs_events.append,
    )

    first_pass: Dict[str, BrokerResponse] = {}
    latencies: List[float] = []
    for seed in SEED_QUERIES:
        response = broker.retrieve(seed.query, tenant=TENANT, role=ROLE, top_k=2)
        first_pass[seed.query] = response
        latencies.append(response.latency_ms)
        assert response.cache_hit is False
        assert response.provider == provider.name
        assert len(response.documents) == 2
        assert tuple(response.citations) == tuple(expectations[seed.query])
        assert response.documents[0].score >= response.documents[1].score
        assert response.obs_card.startswith("route=rag ")
        assert f"provider={provider.name}" in response.obs_card
        assert "cache_hits=" in response.obs_card
        assert "cache_hit=0" in response.obs_card

    accuracy_numerator = 0
    accuracy_denominator = 0
    for seed in SEED_QUERIES:
        expected = expectations[seed.query]
        actual = list(first_pass[seed.query].citations)
        for idx, expected_citation in enumerate(expected):
            accuracy_denominator += 1
            if idx < len(actual) and actual[idx] == expected_citation:
                accuracy_numerator += 1
    citation_accuracy = accuracy_numerator / max(1, accuracy_denominator)
    assert citation_accuracy >= 0.95

    p95_latency = _percentile(latencies, 0.95)
    assert p95_latency < 100.0

    hits_before = cache.stats().hits
    for seed in SEED_QUERIES:
        response = broker.retrieve(seed.query, tenant=TENANT, role=ROLE, top_k=2)
        assert response.cache_hit is True
        assert list(response.citations) == expectations[seed.query]
        assert "cache_hit=1" in response.obs_card
    hits_after = cache.stats().hits
    replay_hit_rate = (hits_after - hits_before) / len(SEED_QUERIES)
    assert replay_hit_rate >= 0.6

    # Tenant isolation: new tenant should miss cache and trigger provider call.
    isolation_response = broker.retrieve(
        SEED_QUERIES[0].query,
        tenant="tenant-beta",
        role=ROLE,
        top_k=2,
    )
    assert isolation_response.cache_hit is False
    assert len(provider.calls) == len(SEED_QUERIES) + 1

    # Observability events recorded for each invocation.
    assert len(obs_events) == len(SEED_QUERIES) * 2 + 1


def test_policy_guard_enforced() -> None:
    dataset, _ = _build_seed_dataset()
    cache = SemanticCache(max_size=8, ttl_seconds=60.0)
    provider = SeedProvider(dataset)
    policy = StaticPolicyGuard({TENANT: [ROLE]})
    broker = RetrievalBroker(provider, cache, policy=policy)

    with pytest.raises(PolicyDeniedError):
        broker.retrieve(SEED_QUERIES[0].query, tenant=TENANT, role="viewer", top_k=2)
