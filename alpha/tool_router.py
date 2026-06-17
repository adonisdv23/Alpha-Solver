"""Deterministic metadata-only tool recommendation preview."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from .tool_catalog import DEFAULT_EVIDENCE_BOUNDARY, ToolCatalog, ToolCatalogEntry

Status = Literal["preview_only", "failed_closed"]
_INJECTION_MARKERS = (
    "ignore previous",
    "ignore all previous",
    "override",
    "developer message",
    "system prompt",
    "execution_authorized",
    "enabled_by_default",
    "set execution",
    "authorize tool",
    "run tool",
    "call github",
    "browse",
)


@dataclass(frozen=True)
class ToolRecommendationRequest:
    task_text: str = ""
    task_family: str | None = None
    requested_tool_id: str | None = None
    include_disabled: bool = False
    untrusted_context: str = "task_text"


@dataclass(frozen=True)
class ToolRecommendationPreview:
    status: Status
    recommended_tool_id: str | None
    recommended_tool_family: str | None
    reasons: tuple[str, ...]
    warnings: tuple[str, ...]
    execution_authorized: bool = False
    untrusted_input_risk: str | None = None
    evidence_boundary: str = DEFAULT_EVIDENCE_BOUNDARY
    candidates: tuple[str, ...] = field(default_factory=tuple)

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "recommended_tool_id": self.recommended_tool_id,
            "recommended_tool_family": self.recommended_tool_family,
            "reasons": list(self.reasons),
            "warnings": list(self.warnings),
            "execution_authorized": self.execution_authorized,
            "untrusted_input_risk": self.untrusted_input_risk,
            "evidence_boundary": self.evidence_boundary,
            "candidates": list(self.candidates),
        }


def recommend_tool(request: ToolRecommendationRequest | None = None, catalog: ToolCatalog | None = None) -> ToolRecommendationPreview:
    req = request or ToolRecommendationRequest()
    cat = catalog or ToolCatalog.load()
    reasons = ["tool_recommendation_preview_only", "no_tool_execution_authorized"]
    warnings = _untrusted_warnings(req)
    tools = cat.tools if req.include_disabled else cat.enabled()
    if not tools:
        return _failed("no_enabled_tools", reasons, warnings)

    if req.requested_tool_id:
        selected = cat.by_tool_id(req.requested_tool_id)
        if selected is None:
            return _failed("requested_tool_not_in_catalog", reasons, warnings, candidates=[tool.tool_id for tool in tools])
        reasons.append("requested_tool_found_in_catalog")
        if not selected.enabled_by_default and not req.include_disabled:
            return _failed("requested_tool_disabled", reasons, warnings, candidates=[tool.tool_id for tool in tools])
        return _preview(selected, reasons, warnings, tools)

    scored = sorted(((_score(tool, req), _reverse_for_descending_tiebreak(tool.tool_id)), tool) for tool in tools)
    (best_score, _tie), selected = scored[-1]
    if best_score <= 0:
        return _failed("no_matching_tool_family", reasons, warnings, candidates=[tool.tool_id for tool in tools])
    if req.task_family:
        reasons.append("task_family_matched" if _contains(selected.task_families, req.task_family) else "task_family_recorded")
    reasons.append("deterministic_keyword_and_weight_selection")
    return _preview(selected, reasons, warnings, tools)


def _score(tool: ToolCatalogEntry, req: ToolRecommendationRequest) -> int:
    score = 0
    haystack = f"{req.task_family or ''} {req.task_text}".lower()
    if req.task_family and _contains(tool.task_families, req.task_family):
        score += 100
    for keyword in tool.match_keywords + tool.task_families + tool.best_for:
        if keyword.lower() in haystack:
            score += 10
    if score:
        score += tool.routing_weight
    return score


def _preview(selected: ToolCatalogEntry, reasons: list[str], warnings: list[str], tools: tuple[ToolCatalogEntry, ...]) -> ToolRecommendationPreview:
    if selected.requires_network:
        warnings.append("recommended_tool_requires_network_if_execution_is_separately_authorized")
    if selected.requires_credentials:
        warnings.append("recommended_tool_requires_credentials_if_execution_is_separately_authorized")
    if selected.untrusted_input_risk in {"medium", "high"}:
        warnings.append(f"untrusted_input_risk_{selected.untrusted_input_risk}")
    if selected.privacy_risk in {"medium", "high"}:
        warnings.append(f"privacy_risk_{selected.privacy_risk}")
    return ToolRecommendationPreview(
        status="preview_only",
        recommended_tool_id=selected.tool_id,
        recommended_tool_family=selected.tool_family,
        reasons=tuple(dict.fromkeys(reasons)),
        warnings=tuple(dict.fromkeys(warnings)),
        execution_authorized=False,
        untrusted_input_risk=selected.untrusted_input_risk,
        evidence_boundary=selected.evidence_boundary,
        candidates=tuple(tool.tool_id for tool in tools),
    )


def _failed(reason: str, reasons: list[str], warnings: list[str], candidates: list[str] | None = None) -> ToolRecommendationPreview:
    reasons.append(reason)
    return ToolRecommendationPreview(
        status="failed_closed",
        recommended_tool_id=None,
        recommended_tool_family=None,
        reasons=tuple(dict.fromkeys(reasons)),
        warnings=tuple(dict.fromkeys(warnings)),
        execution_authorized=False,
        untrusted_input_risk=None,
        evidence_boundary=DEFAULT_EVIDENCE_BOUNDARY,
        candidates=tuple(candidates or ()),
    )


def _untrusted_warnings(req: ToolRecommendationRequest) -> list[str]:
    text = f"{req.task_text} {req.task_family or ''} {req.requested_tool_id or ''}".lower()
    warnings = ["untrusted_input_cannot_authorize_execution"]
    if any(marker in text for marker in _INJECTION_MARKERS):
        warnings.append("possible_prompt_injection_or_authority_escalation_text")
    if req.untrusted_context:
        warnings.append(f"untrusted_context:{req.untrusted_context}")
    return warnings


def _contains(values: tuple[str, ...], needle: str) -> bool:
    return needle.lower() in {value.lower() for value in values}


def _reverse_for_descending_tiebreak(value: str) -> str:
    return "".join(chr(255 - ord(char)) for char in value)
