"""Deterministic retrieval broker backed by a semantic cache."""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Callable, Iterable, List, Mapping, Optional, Protocol, Sequence

from alpha.cache.semantic import SemanticCache


class PolicyDeniedError(RuntimeError):
    """Raised when the policy guard rejects a request."""


class ProviderError(RuntimeError):
    """Raised when the provider returns an invalid response."""


@dataclass(frozen=True)
class RetrievedDocument:
    """Document returned from the retrieval provider."""

    source_id: str
    content: str
    score: float
    metadata: Mapping[str, Any]


@dataclass(frozen=True)
class BrokerResponse:
    """Response payload emitted by the broker."""

    documents: Sequence[RetrievedDocument]
    citations: Sequence[str]
    latency_ms: float
    cache_hit: bool
    provider: str
    obs_card: str


class ProviderShim(Protocol):
    """Protocol describing the provider interface expected by the broker."""

    name: str

    def retrieve(
        self,
        query: str,
        *,
        top_k: int,
        tenant: str,
        role: str,
    ) -> Iterable[Any]:
        ...


class PolicyGuard(Protocol):
    """Protocol describing the policy interface expected by the broker."""

    def ensure_permitted(self, tenant: str, role: str, query: str) -> None:
        ...


class AllowAllPolicy:
    """Default policy that allows every request."""

    def ensure_permitted(self, tenant: str, role: str, query: str) -> None:  # noqa: D401
        """No-op policy that accepts all combinations."""


class StaticPolicyGuard:
    """Static allow-list policy with optional predicate for fine-grained checks."""

    def __init__(
        self,
        allow_map: Optional[Mapping[str, Sequence[str]]] = None,
        predicate: Optional[Callable[[str, str, str], bool]] = None,
    ) -> None:
        self._allow_map = {
            tenant: {role for role in roles}
            for tenant, roles in (allow_map or {}).items()
        }
        self._predicate = predicate

    def ensure_permitted(self, tenant: str, role: str, query: str) -> None:
        if self._allow_map:
            allowed_roles = self._allow_map.get(tenant)
            if not allowed_roles:
                raise PolicyDeniedError(f"tenant '{tenant}' is not authorised for retrieval")
            if "*" not in allowed_roles and role not in allowed_roles:
                raise PolicyDeniedError(
                    f"role '{role}' is not authorised for tenant '{tenant}'",
                )
        if self._predicate and not self._predicate(tenant, role, query):
            raise PolicyDeniedError("policy predicate rejected request")


class RetrievalBroker:
    """Coordinates retrieval with caching, policy enforcement and observability."""

    def __init__(
        self,
        provider: ProviderShim,
        cache: SemanticCache,
        *,
        policy: Optional[PolicyGuard] = None,
        obs_sink: Optional[Callable[[str], None]] = print,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.provider = provider
        self.cache = cache
        self.policy = policy or AllowAllPolicy()
        self.obs_sink = obs_sink
        self.clock = clock

    def retrieve(
        self,
        query: str,
        *,
        tenant: str,
        role: str,
        top_k: int = 3,
        cache_ttl_seconds: Optional[float] = None,
    ) -> BrokerResponse:
        if not query:
            raise ValueError("query must be non-empty")
        if top_k <= 0:
            raise ValueError("top_k must be positive")

        self.policy.ensure_permitted(tenant, role, query)

        cache_text = self._cache_text(query, top_k)
        start = self.clock()
        cached_payload = self.cache.get(cache_text, tenant=tenant, role=role)
        cache_hit = cached_payload is not None

        if cache_hit:
            payload = cached_payload
            documents = list(payload["documents"])
            citations = list(payload["citations"])
            provider_name = payload["provider"]
        else:
            documents = self._fetch_documents(query, tenant=tenant, role=role, top_k=top_k)
            citations = [doc.source_id for doc in documents]
            provider_name = getattr(self.provider, "name", self.provider.__class__.__name__)
            payload = {
                "documents": tuple(documents),
                "citations": tuple(citations),
                "provider": provider_name,
            }
            self.cache.set(
                cache_text,
                payload,
                tenant=tenant,
                role=role,
                ttl_seconds=cache_ttl_seconds,
            )

        latency_ms = (self.clock() - start) * 1000.0
        stats = self.cache.snapshot()
        path = "semantic-cache" if cache_hit else f"provider:{provider_name}"
        obs_line = (
            "route=rag "
            f"path={path} "
            f"cache_hit={int(cache_hit)} "
            f"latency_ms={int(round(latency_ms))} "
            f"provider={provider_name} "
            f"cache_hits={stats['hits']} "
            f"cache_misses={stats['misses']} "
            f"cache_size={stats['size']}"
        )
        if self.obs_sink is not None:
            self.obs_sink(obs_line)

        return BrokerResponse(
            documents=tuple(documents),
            citations=tuple(citations),
            latency_ms=latency_ms,
            cache_hit=cache_hit,
            provider=provider_name,
            obs_card=obs_line,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _cache_text(self, query: str, top_k: int) -> str:
        return f"{query}||top_k={top_k}"

    def _fetch_documents(
        self,
        query: str,
        *,
        tenant: str,
        role: str,
        top_k: int,
    ) -> List[RetrievedDocument]:
        raw_documents = list(
            self.provider.retrieve(query=query, top_k=top_k, tenant=tenant, role=role),
        )
        if not raw_documents:
            return []

        documents = [self._to_document(document) for document in raw_documents]
        documents.sort(key=lambda doc: (-float(doc.score), doc.source_id))
        return documents[:top_k]

    def _to_document(self, document: Any) -> RetrievedDocument:
        if isinstance(document, RetrievedDocument):
            return document
        if isinstance(document, Mapping):
            try:
                source_id = str(document["source_id"])
            except KeyError as exc:
                raise ProviderError("provider document missing 'source_id'") from exc
            content = str(document.get("content", ""))
            score = float(document.get("score", 0.0))
            metadata = document.get("metadata", {})
            if not isinstance(metadata, Mapping):
                raise ProviderError("metadata must be a mapping")
            return RetrievedDocument(
                source_id=source_id,
                content=content,
                score=score,
                metadata=dict(metadata),
            )
        raise ProviderError(f"Unsupported document type: {type(document)!r}")
