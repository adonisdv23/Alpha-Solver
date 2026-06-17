"""Deterministic routing preview over the model catalog.

The preview returns route metadata only. It never calls hosted providers, Ollama,
or any local model runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from tools.operator_smoke_runner import MAX_PROMPT_CHARS

from .model_catalog import DEFAULT_EVIDENCE_BOUNDARY, ModelCatalog, ModelCatalogEntry, Mode

Status = Literal["preview_only", "failed_closed"]


@dataclass(frozen=True)
class RouteFallback:
    mode: Mode
    model: str

    def as_dict(self) -> dict[str, str]:
        return {"mode": self.mode, "model": self.model}


@dataclass(frozen=True)
class RoutingPreviewRequest:
    requested_mode: Mode | None = None
    requested_model: str | None = None
    allow_hosted_providers: bool = True
    allow_local: bool = True
    prompt_length: int = 0
    task_profile: str | None = None
    cost_preference: str | None = None
    latency_preference: str | None = None
    required_capability: str | None = None
    local_only: bool = False


@dataclass(frozen=True)
class RoutingPreview:
    status: Status
    recommended_mode: Mode | None
    recommended_model: str | None
    fallbacks: tuple[RouteFallback, ...]
    reasons: tuple[str, ...]
    evidence_boundary: dict[str, bool] = field(default_factory=lambda: dict(DEFAULT_EVIDENCE_BOUNDARY))
    warnings: tuple[str, ...] = ()
    provider_or_local_execution_authorized: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "recommended_mode": self.recommended_mode,
            "recommended_model": self.recommended_model,
            "fallbacks": [fallback.as_dict() for fallback in self.fallbacks],
            "reasons": list(self.reasons),
            "evidence_boundary": dict(self.evidence_boundary),
            "warnings": list(self.warnings),
            "provider_or_local_execution_authorized": self.provider_or_local_execution_authorized,
        }


def preview_route(request: RoutingPreviewRequest | None = None, catalog: ModelCatalog | None = None) -> RoutingPreview:
    req = request or RoutingPreviewRequest()
    cat = catalog or ModelCatalog.load()
    reasons: list[str] = ["routing_preview_only", "no_provider_or_local_model_calls"]
    warnings: list[str] = []

    if req.local_only and req.allow_hosted_providers:
        warnings.append("local_only_request_suppresses_hosted_recommendations")
        req = RoutingPreviewRequest(
            requested_mode=req.requested_mode or "local",
            requested_model=req.requested_model,
            allow_hosted_providers=False,
            allow_local=req.allow_local,
            prompt_length=req.prompt_length,
            task_profile=req.task_profile,
            cost_preference=req.cost_preference,
            latency_preference=req.latency_preference,
            required_capability=req.required_capability,
            local_only=req.local_only,
        )
    if req.prompt_length > MAX_PROMPT_CHARS:
        warnings.append("prompt_length_exceeds_preview_smoke_boundary")
        return _failed("prompt_too_long_for_smoke_runner", cat, req, reasons, warnings)
    if not req.allow_hosted_providers and not req.allow_local:
        return _failed("no_modes_allowed", cat, req, reasons, warnings)

    if req.requested_mode:
        reasons.append(f"{req.requested_mode}_requested_by_operator")
    if req.task_profile:
        reasons.append("task_profile_recorded_no_quality_selection")
    if req.cost_preference:
        reasons.append("cost_preference_recorded_no_pricing_selection")
    if req.latency_preference:
        reasons.append("latency_preference_recorded_no_latency_claim")
    if req.required_capability:
        reasons.append("required_capability_matched_as_metadata_only")

    selected: ModelCatalogEntry | None = None
    if req.requested_model:
        selected = cat.by_model_id(req.requested_model)
        if selected is None:
            return _failed("requested_model_not_in_catalog", cat, req, reasons, warnings)
        reasons.append("model_available_in_catalog")
        if not selected.enabled_by_default:
            return _failed("requested_model_disabled", cat, req, reasons, warnings)
        if req.required_capability and req.required_capability not in selected.capability_tags:
            return _failed("requested_model_missing_required_capability", cat, req, reasons, warnings)
        if selected.mode == "openai" and not req.allow_hosted_providers:
            warnings.append("local_fallback_available" if cat.by_mode("local") and req.allow_local else "hosted_execution_disabled")
            return _failed("hosted_provider_not_allowed", cat, req, reasons, warnings)
        if selected.mode == "local" and not req.allow_local:
            return _failed("local_model_not_allowed", cat, req, reasons, warnings)
        if req.requested_mode and selected.mode != req.requested_mode:
            return _failed("requested_mode_model_mismatch", cat, req, reasons, warnings)
    else:
        selected = _default_for_request(cat, req, reasons)
        if selected is None:
            return _failed("no_eligible_model", cat, req, reasons, warnings)

    if selected.smoke_eligible:
        reasons.append("smoke_eligible")
    else:
        warnings.append("selected_model_not_smoke_eligible")

    return RoutingPreview(
        status="preview_only",
        recommended_mode=selected.mode,
        recommended_model=selected.model_id,
        fallbacks=_fallbacks(cat, exclude=selected.model_id, request=req),
        reasons=tuple(reasons),
        evidence_boundary=dict(selected.evidence_boundary),
        warnings=tuple(warnings),
    )


def _default_for_request(cat: ModelCatalog, req: RoutingPreviewRequest, reasons: list[str]) -> ModelCatalogEntry | None:
    mode_order: tuple[Mode, ...]
    if req.requested_mode == "openai" or not req.allow_local:
        mode_order = ("openai", "local")
    else:
        mode_order = ("local", "openai")
    for mode in mode_order:
        if mode == "openai" and not req.allow_hosted_providers:
            continue
        if mode == "local" and not req.allow_local:
            continue
        options = _metadata_filtered(cat.by_mode(mode), req)
        if options:
            reasons.append(f"{mode}_metadata_default_selected")
            return options[0]
    return None


def _metadata_filtered(options: tuple[ModelCatalogEntry, ...], req: RoutingPreviewRequest) -> tuple[ModelCatalogEntry, ...]:
    filtered = options
    if req.required_capability:
        filtered = tuple(model for model in filtered if req.required_capability in model.capability_tags)
    if req.cost_preference:
        filtered = tuple(model for model in filtered if model.cost_tier == req.cost_preference) or filtered
    if req.latency_preference:
        filtered = tuple(model for model in filtered if model.latency_tier == req.latency_preference) or filtered
    if req.task_profile:
        filtered = tuple(model for model in filtered if req.task_profile in model.task_families or req.task_profile in model.routing_roles) or filtered
    return filtered


def _fallbacks(cat: ModelCatalog, *, exclude: str | None, request: RoutingPreviewRequest) -> tuple[RouteFallback, ...]:
    allowed_modes = set()
    if request.allow_hosted_providers:
        allowed_modes.add("openai")
    if request.allow_local:
        allowed_modes.add("local")
    fallbacks = [
        RouteFallback(model.mode, model.model_id)
        for model in _metadata_filtered(cat.enabled(), request)
        if model.model_id != exclude and model.mode in allowed_modes
    ]
    return tuple(fallbacks[:3])


def _failed(reason: str, cat: ModelCatalog, req: RoutingPreviewRequest, reasons: list[str], warnings: list[str]) -> RoutingPreview:
    reasons.append(reason)
    return RoutingPreview(
        status="failed_closed",
        recommended_mode=None,
        recommended_model=None,
        fallbacks=_fallbacks(cat, exclude=None, request=req),
        reasons=tuple(reasons),
        warnings=tuple(warnings),
    )
