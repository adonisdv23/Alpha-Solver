from __future__ import annotations

"""Registry for configured model sets.

Loads ``service/config/model_sets.yaml`` and exposes validated model
information for routing and cost estimation.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Mapping, Optional
import yaml

__all__ = ["ModelSet", "ModelSetRegistry", "ModelSetError"]


ALLOWED_PROVIDERS = {"openai", "anthropic"}


class ModelSetError(ValueError):
    """Raised for configuration problems with model sets."""


@dataclass(frozen=True)
class ModelSet:
    name: str
    provider: str
    model: str
    max_tokens: int
    timeout_ms: int
    price_hint: Optional[Mapping[str, float]] = None


class ModelSetRegistry:
    """Load and validate model set configuration."""

    def __init__(self, path: str | Path | None = None):
        cfg_path = (
            Path(path)
            if path is not None
            else Path(__file__).resolve().parents[1] / "config" / "model_sets.yaml"
        )
        self._path = cfg_path
        self._model_sets: Dict[str, ModelSet] = self._load(cfg_path)

    # ------------------------------------------------------------------
    def _load(self, path: Path) -> Dict[str, ModelSet]:
        if not path.exists():
            raise ModelSetError(f"model set config not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}

        if "model_sets" not in raw or not isinstance(raw["model_sets"], dict):
            raise ModelSetError("model_sets.yaml missing 'model_sets' mapping")

        sets = {}
        for name in sorted(raw["model_sets"].keys()):
            cfg = raw["model_sets"][name] or {}
            self._validate_set(name, cfg)
            sets[name] = ModelSet(
                name=name,
                provider=cfg["provider"],
                model=cfg["model"],
                max_tokens=cfg["max_tokens"],
                timeout_ms=cfg["timeout_ms"],
                price_hint=cfg.get("price_hint"),
            )

        if len(sets) < 2:
            raise ModelSetError("model_sets.yaml must define at least two model sets")

        return sets

    # ------------------------------------------------------------------
    def _validate_set(self, name: str, cfg: Mapping[str, object]) -> None:
        provider = cfg.get("provider")
        if provider not in ALLOWED_PROVIDERS:
            raise ModelSetError(
                f"Model set '{name}' has unknown provider '{provider}'"
            )

        model = cfg.get("model")
        if not isinstance(model, str) or not model.strip():
            raise ModelSetError(f"Model set '{name}' missing required field 'model'")

        max_tokens = cfg.get("max_tokens")
        if not isinstance(max_tokens, int) or max_tokens <= 0:
            raise ModelSetError(
                f"Model set '{name}' has invalid 'max_tokens': {max_tokens}"
            )

        timeout_ms = cfg.get("timeout_ms")
        if not isinstance(timeout_ms, int) or timeout_ms <= 0:
            raise ModelSetError(
                f"Model set '{name}' has invalid 'timeout_ms': {timeout_ms}"
            )

        if "price_hint" in cfg:
            ph = cfg["price_hint"]
            if not isinstance(ph, Mapping):
                raise ModelSetError(
                    f"Model set '{name}' has invalid price_hint: {ph!r}"
                )
            for key in ("input_per_1k", "output_per_1k"):
                if key not in ph:
                    raise ModelSetError(
                        f"Model set '{name}' price_hint missing '{key}'"
                    )
                val = ph[key]
                if not isinstance(val, (int, float)) or val < 0:
                    raise ModelSetError(
                        f"Model set '{name}' price_hint.{key} invalid: {val}"
                    )

    # ------------------------------------------------------------------
    def get(self, name: str) -> ModelSet:
        try:
            return self._model_sets[name]
        except KeyError as exc:  # pragma: no cover - guard
            raise ModelSetError(f"Unknown model set '{name}'") from exc

    # ------------------------------------------------------------------
    def names(self) -> list[str]:
        return list(self._model_sets.keys())

    # ------------------------------------------------------------------
    def __iter__(self) -> Iterable[ModelSet]:
        return iter(self._model_sets.values())

