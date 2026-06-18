"""Configurable model catalog for backend routing previews.

This module is deliberately metadata-only. Loading the catalog does not contact
hosted providers, Ollama, or any local model runtime.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Iterable, Literal

Mode = Literal["local", "openai"]
BackendType = Literal["local", "hosted", "future_provider", "external"]
Tier = Literal["low", "medium", "high", "unknown"]
ReviewStatus = Literal["operator_metadata", "smoke_only", "not_verified", "catalog_only"]

DEFAULT_CATALOG_PATH = Path(__file__).resolve().parents[1] / "configs" / "model_catalog.json"
DEFAULT_EVIDENCE_BOUNDARY: dict[str, bool] = {
    "runs_provider": False,
    "runs_local_model": False,
    "quality_evidence": False,
    "readiness_evidence": False,
    "benchmark_evidence": False,
}


def _require_bool(raw: dict[str, Any], field: str) -> bool:
    value = raw[field]
    if not isinstance(value, bool):
        raise ValueError(f"model catalog field must be boolean: {field}")
    return value


def _require_str_list(raw: dict[str, Any], field: str, *, allow_empty: bool = False) -> tuple[str, ...]:
    value = raw[field]
    if not isinstance(value, list) or (not allow_empty and not value) or not all(isinstance(item, str) and item for item in value):
        requirement = "a string list" if allow_empty else "a non-empty string list"
        raise ValueError(f"model catalog field must be {requirement}: {field}")
    return tuple(value)


def _require_evidence_boundary(value: Any) -> dict[str, bool]:
    if not isinstance(value, dict):
        raise ValueError("model catalog evidence_boundary must be an object")
    boundary = dict(DEFAULT_EVIDENCE_BOUNDARY)
    for key, flag in value.items():
        if key not in DEFAULT_EVIDENCE_BOUNDARY:
            raise ValueError(f"unsupported model catalog evidence boundary flag: {key}")
        if not isinstance(flag, bool):
            raise ValueError(f"model catalog evidence boundary flag must be boolean: {key}")
        boundary[key] = flag
    if any(boundary.values()):
        raise ValueError("model catalog entries must not imply validation evidence")
    return boundary


@dataclass(frozen=True)
class ModelCatalogEntry:
    provider: str
    mode: Mode
    model_id: str
    id: str
    display_name: str
    enabled_by_default: bool
    backend_type: BackendType
    model_family: str
    availability_status: str
    requires_provider_key: bool
    local_only: bool
    routing_roles: tuple[str, ...]
    task_families: tuple[str, ...]
    capability_tags: tuple[str, ...]
    cost_tier: Tier
    latency_tier: Tier
    context_tier: Tier
    privacy_tier: str
    supports_json: bool
    supports_tools: bool
    supports_vision: bool
    smoke_eligible: bool
    route_tags: tuple[str, ...]
    tool_compatibility: tuple[str, ...]
    best_for: tuple[str, ...]
    avoid_for: tuple[str, ...]
    fallback_eligible: bool
    requires_network: bool
    requires_credentials: bool
    evidence_boundary: dict[str, bool]
    quality_claim: bool
    last_reviewed: str
    reviewed_at: str
    catalog_reviewed_at: str
    review_status: ReviewStatus
    operator_notes: str

    @classmethod
    def from_mapping(cls, raw: dict[str, Any]) -> "ModelCatalogEntry":
        required = (
            "provider",
            "mode",
            "model_id",
            "display_name",
            "id",
            "enabled_by_default",
            "backend_type",
            "model_family",
            "availability_status",
            "requires_provider_key",
            "local_only",
            "routing_roles",
            "task_families",
            "capability_tags",
            "cost_tier",
            "latency_tier",
            "context_tier",
            "privacy_tier",
            "supports_json",
            "supports_tools",
            "supports_vision",
            "smoke_eligible",
            "route_tags",
            "tool_compatibility",
            "best_for",
            "avoid_for",
            "fallback_eligible",
            "requires_network",
            "requires_credentials",
            "evidence_boundary",
            "quality_claim",
            "last_reviewed",
            "reviewed_at",
            "catalog_reviewed_at",
            "review_status",
            "operator_notes",
        )
        missing = [field for field in required if field not in raw]
        if missing:
            raise ValueError(f"model catalog entry missing required fields: {', '.join(missing)}")
        mode = str(raw["mode"])
        if mode not in {"local", "openai"}:
            raise ValueError(f"unsupported model catalog mode: {mode}")
        quality_claim = _require_bool(raw, "quality_claim")
        if quality_claim:
            raise ValueError("model catalog entries must not carry quality claims")
        boundary = _require_evidence_boundary(raw["evidence_boundary"])
        backend_type = str(raw["backend_type"])
        if backend_type not in {"local", "hosted", "future_provider", "external"}:
            raise ValueError(f"unsupported backend_type: {backend_type}")
        if mode == "local" and backend_type != "local":
            raise ValueError("local catalog entries must use backend_type local")
        if mode == "openai" and backend_type != "hosted":
            raise ValueError("openai catalog entries must use backend_type hosted")
        review_status = str(raw["review_status"])
        if review_status not in {"operator_metadata", "smoke_only", "not_verified", "catalog_only"}:
            raise ValueError(f"unsupported model catalog review_status: {review_status}")
        tiers = {"low", "medium", "high", "unknown"}
        for tier_field in ("cost_tier", "latency_tier", "context_tier"):
            if str(raw[tier_field]) not in tiers:
                raise ValueError(f"unsupported {tier_field}: {raw[tier_field]}")
        return cls(
            provider=str(raw["provider"]),
            mode=mode,  # type: ignore[arg-type]
            model_id=str(raw["model_id"]),
            id=str(raw["id"]),
            display_name=str(raw["display_name"]),
            enabled_by_default=_require_bool(raw, "enabled_by_default"),
            backend_type=backend_type,  # type: ignore[arg-type]
            model_family=str(raw["model_family"]),
            availability_status=str(raw["availability_status"]),
            requires_provider_key=_require_bool(raw, "requires_provider_key"),
            local_only=_require_bool(raw, "local_only"),
            routing_roles=_require_str_list(raw, "routing_roles"),
            task_families=_require_str_list(raw, "task_families"),
            capability_tags=_require_str_list(raw, "capability_tags"),
            cost_tier=str(raw["cost_tier"]),  # type: ignore[arg-type]
            latency_tier=str(raw["latency_tier"]),  # type: ignore[arg-type]
            context_tier=str(raw["context_tier"]),  # type: ignore[arg-type]
            privacy_tier=str(raw["privacy_tier"]),
            supports_json=_require_bool(raw, "supports_json"),
            supports_tools=_require_bool(raw, "supports_tools"),
            supports_vision=_require_bool(raw, "supports_vision"),
            smoke_eligible=_require_bool(raw, "smoke_eligible"),
            route_tags=_require_str_list(raw, "route_tags"),
            tool_compatibility=_require_str_list(raw, "tool_compatibility", allow_empty=True),
            best_for=_require_str_list(raw, "best_for", allow_empty=True),
            avoid_for=_require_str_list(raw, "avoid_for", allow_empty=True),
            fallback_eligible=_require_bool(raw, "fallback_eligible"),
            requires_network=_require_bool(raw, "requires_network"),
            requires_credentials=_require_bool(raw, "requires_credentials"),
            evidence_boundary=boundary,
            quality_claim=quality_claim,
            last_reviewed=str(raw["last_reviewed"]),
            reviewed_at=str(raw["reviewed_at"]),
            catalog_reviewed_at=str(raw["catalog_reviewed_at"]),
            review_status=review_status,  # type: ignore[arg-type]
            operator_notes=str(raw["operator_notes"]),
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "mode": self.mode,
            "model_id": self.model_id,
            "id": self.id,
            "display_name": self.display_name,
            "enabled_by_default": self.enabled_by_default,
            "backend_type": self.backend_type,
            "model_family": self.model_family,
            "availability_status": self.availability_status,
            "requires_provider_key": self.requires_provider_key,
            "local_only": self.local_only,
            "routing_roles": list(self.routing_roles),
            "task_families": list(self.task_families),
            "capability_tags": list(self.capability_tags),
            "cost_tier": self.cost_tier,
            "latency_tier": self.latency_tier,
            "context_tier": self.context_tier,
            "privacy_tier": self.privacy_tier,
            "supports_json": self.supports_json,
            "supports_tools": self.supports_tools,
            "supports_vision": self.supports_vision,
            "smoke_eligible": self.smoke_eligible,
            "route_tags": list(self.route_tags),
            "tool_compatibility": list(self.tool_compatibility),
            "best_for": list(self.best_for),
            "avoid_for": list(self.avoid_for),
            "fallback_eligible": self.fallback_eligible,
            "requires_network": self.requires_network,
            "requires_credentials": self.requires_credentials,
            "evidence_boundary": dict(self.evidence_boundary),
            "quality_claim": self.quality_claim,
            "last_reviewed": self.last_reviewed,
            "reviewed_at": self.reviewed_at,
            "catalog_reviewed_at": self.catalog_reviewed_at,
            "review_status": self.review_status,
            "operator_notes": self.operator_notes,
        }


@dataclass(frozen=True)
class ModelCatalog:
    version: str
    models: tuple[ModelCatalogEntry, ...]
    evidence_boundary: dict[str, bool]

    @classmethod
    def load(cls, path: str | Path = DEFAULT_CATALOG_PATH) -> "ModelCatalog":
        catalog_path = Path(path)
        data = json.loads(catalog_path.read_text(encoding="utf-8"))
        models = tuple(ModelCatalogEntry.from_mapping(item) for item in data.get("models", []))
        if not models:
            raise ValueError("model catalog must contain at least one model")
        model_ids = [model.model_id for model in models]
        if len(model_ids) != len(set(model_ids)):
            raise ValueError("model catalog model_id values must be unique")
        boundary = _require_evidence_boundary(data.get("evidence_boundary", {}))
        return cls(version=str(data.get("version", "unversioned")), models=models, evidence_boundary=boundary)

    def enabled(self) -> tuple[ModelCatalogEntry, ...]:
        return tuple(model for model in self.models if model.enabled_by_default)

    def by_model_id(self, model_id: str) -> ModelCatalogEntry | None:
        return next((model for model in self.models if model.model_id == model_id), None)

    def by_mode(self, mode: Mode, *, enabled_only: bool = True) -> tuple[ModelCatalogEntry, ...]:
        source: Iterable[ModelCatalogEntry] = self.enabled() if enabled_only else self.models
        return tuple(model for model in source if model.mode == mode)
