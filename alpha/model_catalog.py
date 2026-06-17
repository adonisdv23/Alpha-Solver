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
Tier = Literal["low", "medium", "high", "unknown"]
ReviewStatus = Literal["operator_metadata", "smoke_only"]

DEFAULT_CATALOG_PATH = Path(__file__).resolve().parents[1] / "configs" / "model_catalog.json"
DEFAULT_EVIDENCE_BOUNDARY: dict[str, bool] = {
    "runs_provider": False,
    "runs_local_model": False,
    "quality_evidence": False,
    "readiness_evidence": False,
    "benchmark_evidence": False,
}


@dataclass(frozen=True)
class ModelCatalogEntry:
    provider: str
    mode: Mode
    model_id: str
    display_name: str
    enabled_by_default: bool
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
    requires_network: bool
    requires_credentials: bool
    evidence_boundary: dict[str, bool]
    quality_claim: bool
    last_reviewed: str
    review_status: ReviewStatus
    operator_notes: str

    @classmethod
    def from_mapping(cls, raw: dict[str, Any]) -> "ModelCatalogEntry":
        required = (
            "provider",
            "mode",
            "model_id",
            "display_name",
            "enabled_by_default",
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
            "requires_network",
            "requires_credentials",
            "evidence_boundary",
            "quality_claim",
            "last_reviewed",
            "review_status",
            "operator_notes",
        )
        missing = [field for field in required if field not in raw]
        if missing:
            raise ValueError(f"model catalog entry missing required fields: {', '.join(missing)}")
        mode = str(raw["mode"])
        if mode not in {"local", "openai"}:
            raise ValueError(f"unsupported model catalog mode: {mode}")
        quality_claim = bool(raw["quality_claim"])
        if quality_claim:
            raise ValueError("model catalog entries must not carry quality claims")
        boundary = dict(DEFAULT_EVIDENCE_BOUNDARY)
        boundary.update({key: bool(value) for key, value in raw["evidence_boundary"].items()})
        if any(boundary.values()):
            raise ValueError("model catalog entries must not imply validation evidence")
        review_status = str(raw["review_status"])
        if review_status not in {"operator_metadata", "smoke_only"}:
            raise ValueError(f"unsupported model catalog review_status: {review_status}")
        tiers = {"low", "medium", "high", "unknown"}
        for tier_field in ("cost_tier", "latency_tier", "context_tier"):
            if str(raw[tier_field]) not in tiers:
                raise ValueError(f"unsupported {tier_field}: {raw[tier_field]}")
        return cls(
            provider=str(raw["provider"]),
            mode=mode,  # type: ignore[arg-type]
            model_id=str(raw["model_id"]),
            display_name=str(raw["display_name"]),
            enabled_by_default=bool(raw["enabled_by_default"]),
            routing_roles=tuple(str(item) for item in raw["routing_roles"]),
            task_families=tuple(str(item) for item in raw["task_families"]),
            capability_tags=tuple(str(item) for item in raw["capability_tags"]),
            cost_tier=str(raw["cost_tier"]),  # type: ignore[arg-type]
            latency_tier=str(raw["latency_tier"]),  # type: ignore[arg-type]
            context_tier=str(raw["context_tier"]),  # type: ignore[arg-type]
            privacy_tier=str(raw["privacy_tier"]),
            supports_json=bool(raw["supports_json"]),
            supports_tools=bool(raw["supports_tools"]),
            supports_vision=bool(raw["supports_vision"]),
            smoke_eligible=bool(raw["smoke_eligible"]),
            requires_network=bool(raw["requires_network"]),
            requires_credentials=bool(raw["requires_credentials"]),
            evidence_boundary=boundary,
            quality_claim=quality_claim,
            last_reviewed=str(raw["last_reviewed"]),
            review_status=review_status,  # type: ignore[arg-type]
            operator_notes=str(raw["operator_notes"]),
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "mode": self.mode,
            "model_id": self.model_id,
            "display_name": self.display_name,
            "enabled_by_default": self.enabled_by_default,
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
            "requires_network": self.requires_network,
            "requires_credentials": self.requires_credentials,
            "evidence_boundary": dict(self.evidence_boundary),
            "quality_claim": self.quality_claim,
            "last_reviewed": self.last_reviewed,
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
        boundary = dict(DEFAULT_EVIDENCE_BOUNDARY)
        boundary.update({key: bool(value) for key, value in data.get("evidence_boundary", {}).items()})
        if any(boundary.values()):
            raise ValueError("model catalog evidence boundary must remain preview-only")
        return cls(version=str(data.get("version", "unversioned")), models=models, evidence_boundary=boundary)

    def enabled(self) -> tuple[ModelCatalogEntry, ...]:
        return tuple(model for model in self.models if model.enabled_by_default)

    def by_model_id(self, model_id: str) -> ModelCatalogEntry | None:
        return next((model for model in self.models if model.model_id == model_id), None)

    def by_mode(self, mode: Mode, *, enabled_only: bool = True) -> tuple[ModelCatalogEntry, ...]:
        source: Iterable[ModelCatalogEntry] = self.enabled() if enabled_only else self.models
        return tuple(model for model in source if model.mode == mode)
