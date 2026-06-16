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
    enabled_default: bool
    smoke_eligible: bool
    notes: str
    quality_claim: bool = False

    @classmethod
    def from_mapping(cls, raw: dict[str, Any]) -> "ModelCatalogEntry":
        required = ("provider", "mode", "model_id", "display_name", "enabled_default", "smoke_eligible", "notes")
        missing = [field for field in required if field not in raw]
        if missing:
            raise ValueError(f"model catalog entry missing required fields: {', '.join(missing)}")
        mode = str(raw["mode"])
        if mode not in {"local", "openai"}:
            raise ValueError(f"unsupported model catalog mode: {mode}")
        quality_claim = bool(raw.get("quality_claim", False))
        if quality_claim:
            raise ValueError("model catalog entries must not carry quality claims")
        return cls(
            provider=str(raw["provider"]),
            mode=mode,  # type: ignore[arg-type]
            model_id=str(raw["model_id"]),
            display_name=str(raw["display_name"]),
            enabled_default=bool(raw["enabled_default"]),
            smoke_eligible=bool(raw["smoke_eligible"]),
            notes=str(raw["notes"]),
            quality_claim=quality_claim,
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "mode": self.mode,
            "model_id": self.model_id,
            "display_name": self.display_name,
            "enabled_default": self.enabled_default,
            "smoke_eligible": self.smoke_eligible,
            "notes": self.notes,
            "quality_claim": self.quality_claim,
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
        return tuple(model for model in self.models if model.enabled_default)

    def by_model_id(self, model_id: str) -> ModelCatalogEntry | None:
        return next((model for model in self.models if model.model_id == model_id), None)

    def by_mode(self, mode: Mode, *, enabled_only: bool = True) -> tuple[ModelCatalogEntry, ...]:
        source: Iterable[ModelCatalogEntry] = self.enabled() if enabled_only else self.models
        return tuple(model for model in source if model.mode == mode)
