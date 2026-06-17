"""Metadata-only tool catalog for deterministic routing previews.

Loading this catalog does not execute tools, browse, call providers, call GitHub,
mutate files, or expand runtime authority.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

DEFAULT_CATALOG_PATH = Path(__file__).resolve().parents[1] / "configs" / "tool_catalog.json"
DEFAULT_EVIDENCE_BOUNDARY = "metadata_only_recommendation_preview_no_tool_execution"
PRIVACY_RISKS = {"low", "medium", "high"}
UNTRUSTED_INPUT_RISKS = {"low", "medium", "high"}


@dataclass(frozen=True)
class ToolCatalogEntry:
    tool_id: str
    display_name: str
    tool_family: str
    task_families: tuple[str, ...]
    best_for: tuple[str, ...]
    not_for: tuple[str, ...]
    requires_network: bool
    requires_credentials: bool
    privacy_risk: str
    untrusted_input_risk: str
    execution_authorized: bool
    enabled_by_default: bool
    routing_weight: int
    confidence_effect: str
    evidence_boundary: str
    operator_notes: str
    match_keywords: tuple[str, ...]

    @classmethod
    def from_mapping(cls, raw: dict[str, Any]) -> "ToolCatalogEntry":
        required = (
            "tool_id",
            "display_name",
            "tool_family",
            "task_families",
            "best_for",
            "not_for",
            "requires_network",
            "requires_credentials",
            "privacy_risk",
            "untrusted_input_risk",
            "execution_authorized",
            "enabled_by_default",
            "routing_weight",
            "confidence_effect",
            "evidence_boundary",
            "operator_notes",
        )
        missing = [field for field in required if field not in raw]
        if missing:
            raise ValueError(f"tool catalog entry missing required fields: {', '.join(missing)}")

        entry = cls(
            tool_id=_nonempty(raw, "tool_id"),
            display_name=_nonempty(raw, "display_name"),
            tool_family=_nonempty(raw, "tool_family"),
            task_families=_strings(raw, "task_families"),
            best_for=_strings(raw, "best_for"),
            not_for=_strings(raw, "not_for"),
            requires_network=bool(raw["requires_network"]),
            requires_credentials=bool(raw["requires_credentials"]),
            privacy_risk=str(raw["privacy_risk"]),
            untrusted_input_risk=str(raw["untrusted_input_risk"]),
            execution_authorized=bool(raw["execution_authorized"]),
            enabled_by_default=bool(raw["enabled_by_default"]),
            routing_weight=int(raw["routing_weight"]),
            confidence_effect=_nonempty(raw, "confidence_effect"),
            evidence_boundary=_nonempty(raw, "evidence_boundary"),
            operator_notes=_nonempty(raw, "operator_notes"),
            match_keywords=_strings(raw, "match_keywords", required=False),
        )
        entry.validate()
        return entry

    def validate(self) -> None:
        if self.privacy_risk not in PRIVACY_RISKS:
            raise ValueError(f"unsupported privacy_risk for {self.tool_id}: {self.privacy_risk}")
        if self.untrusted_input_risk not in UNTRUSTED_INPUT_RISKS:
            raise ValueError(f"unsupported untrusted_input_risk for {self.tool_id}: {self.untrusted_input_risk}")
        if self.execution_authorized:
            raise ValueError(f"tool catalog entry must not authorize execution: {self.tool_id}")
        if self.routing_weight < 0:
            raise ValueError(f"routing_weight must be non-negative: {self.tool_id}")
        if self.evidence_boundary != DEFAULT_EVIDENCE_BOUNDARY:
            raise ValueError(f"unsupported evidence boundary for {self.tool_id}: {self.evidence_boundary}")
        if not self.task_families or not self.best_for:
            raise ValueError(f"tool catalog entry must include task_families and best_for: {self.tool_id}")

    def as_dict(self) -> dict[str, Any]:
        return {
            "tool_id": self.tool_id,
            "display_name": self.display_name,
            "tool_family": self.tool_family,
            "task_families": list(self.task_families),
            "best_for": list(self.best_for),
            "not_for": list(self.not_for),
            "requires_network": self.requires_network,
            "requires_credentials": self.requires_credentials,
            "privacy_risk": self.privacy_risk,
            "untrusted_input_risk": self.untrusted_input_risk,
            "execution_authorized": self.execution_authorized,
            "enabled_by_default": self.enabled_by_default,
            "routing_weight": self.routing_weight,
            "confidence_effect": self.confidence_effect,
            "evidence_boundary": self.evidence_boundary,
            "operator_notes": self.operator_notes,
            "match_keywords": list(self.match_keywords),
        }


@dataclass(frozen=True)
class ToolCatalog:
    version: str
    tools: tuple[ToolCatalogEntry, ...]
    evidence_boundary: str

    @classmethod
    def load(cls, path: str | Path = DEFAULT_CATALOG_PATH) -> "ToolCatalog":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        boundary = str(data.get("evidence_boundary", DEFAULT_EVIDENCE_BOUNDARY))
        if boundary != DEFAULT_EVIDENCE_BOUNDARY:
            raise ValueError("tool catalog evidence boundary must remain metadata-only")
        tools = tuple(ToolCatalogEntry.from_mapping(item) for item in data.get("tools", []))
        if not tools:
            raise ValueError("tool catalog must contain at least one tool")
        ids = [tool.tool_id for tool in tools]
        if len(ids) != len(set(ids)):
            raise ValueError("tool catalog contains duplicate tool_id values")
        return cls(version=str(data.get("version", "unversioned")), tools=tools, evidence_boundary=boundary)

    def enabled(self) -> tuple[ToolCatalogEntry, ...]:
        return tuple(tool for tool in self.tools if tool.enabled_by_default)

    def by_tool_id(self, tool_id: str) -> ToolCatalogEntry | None:
        return next((tool for tool in self.tools if tool.tool_id == tool_id), None)


def _nonempty(raw: dict[str, Any], key: str) -> str:
    value = str(raw[key]).strip()
    if not value:
        raise ValueError(f"tool catalog field must be non-empty: {key}")
    return value


def _strings(raw: dict[str, Any], key: str, *, required: bool = True) -> tuple[str, ...]:
    if key not in raw:
        if required:
            raise ValueError(f"tool catalog field missing: {key}")
        return ()
    value = raw[key]
    if not isinstance(value, list):
        raise ValueError(f"tool catalog field must be a list: {key}")
    strings = tuple(str(item).strip() for item in value if str(item).strip())
    if required and not strings:
        raise ValueError(f"tool catalog field must not be empty: {key}")
    return strings
