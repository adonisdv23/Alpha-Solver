import pytest

from alpha.model_router import RoutingPreviewRequest, preview_route
from tools.operator_smoke_runner import MAX_PROMPT_CHARS


def test_router_selects_requested_enabled_openai_model_when_hosted_allowed():
    preview = preview_route(RoutingPreviewRequest(requested_mode="openai", requested_model="gpt-4.1-mini", allow_hosted_providers=True))

    assert preview.status == "preview_only"
    assert preview.recommended_mode == "openai"
    assert preview.recommended_model == "gpt-4.1-mini"
    assert "model_available_in_catalog" in preview.reasons
    assert "smoke_eligible" in preview.reasons


def test_router_selects_requested_enabled_local_model_when_local_allowed():
    preview = preview_route(RoutingPreviewRequest(requested_mode="local", requested_model="qwen2.5:3b", allow_local=True))

    assert preview.status == "preview_only"
    assert preview.recommended_mode == "local"
    assert preview.recommended_model == "qwen2.5:3b"


def test_router_rejects_hosted_model_when_hosted_not_allowed():
    preview = preview_route(RoutingPreviewRequest(requested_model="gpt-4.1-mini", allow_hosted_providers=False, allow_local=True))

    assert preview.status == "failed_closed"
    assert preview.recommended_model is None
    assert "hosted_provider_not_allowed" in preview.reasons


def test_router_rejects_local_model_when_local_not_allowed():
    preview = preview_route(RoutingPreviewRequest(requested_model="qwen2.5:3b", allow_hosted_providers=True, allow_local=False))

    assert preview.status == "failed_closed"
    assert preview.recommended_model is None
    assert "local_model_not_allowed" in preview.reasons


def test_router_returns_failed_closed_preview_for_unknown_model():
    preview = preview_route(RoutingPreviewRequest(requested_model="unknown-model"))

    assert preview.status == "failed_closed"
    assert preview.recommended_model is None
    assert "requested_model_not_in_catalog" in preview.reasons


def test_router_returns_failed_closed_preview_for_prompt_above_smoke_limit():
    preview = preview_route(RoutingPreviewRequest(prompt_length=MAX_PROMPT_CHARS + 1))

    assert preview.status == "failed_closed"
    assert "prompt_too_long_for_smoke_runner" in preview.reasons


def test_router_includes_reasons():
    preview = preview_route(RoutingPreviewRequest(requested_mode="openai", requested_model="gpt-4.1-mini"))

    assert preview.reasons
    assert "routing_preview_only" in preview.reasons
    assert "openai_requested_by_operator" in preview.reasons


def test_router_includes_preview_only_evidence_boundary_flags():
    preview = preview_route(RoutingPreviewRequest())

    assert preview.evidence_boundary == {
        "runs_provider": False,
        "runs_local_model": False,
        "quality_evidence": False,
        "readiness_evidence": False,
        "benchmark_evidence": False,
    }


def test_router_does_not_require_api_keys(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    preview = preview_route(RoutingPreviewRequest(requested_model="gpt-4.1-mini"))

    assert preview.status == "preview_only"
    assert preview.recommended_model == "gpt-4.1-mini"


def test_router_does_not_call_provider_clients(monkeypatch):
    import alpha.providers.openai as openai_provider

    def fail_if_called(*args, **kwargs):
        raise AssertionError("provider client must not be called by routing preview")

    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "execute", fail_if_called)

    preview = preview_route(RoutingPreviewRequest(requested_model="gpt-4.1-mini"))

    assert preview.status == "preview_only"


def test_router_does_not_call_ollama_or_local_runtime(monkeypatch):
    import alpha.local_llm.provider_adapter as provider_adapter

    def fail_if_called(*args, **kwargs):
        raise AssertionError("local runtime must not be called by routing preview")

    monkeypatch.setattr(provider_adapter, "run_configured_local_llm_runtime", fail_if_called)

    preview = preview_route(RoutingPreviewRequest(requested_model="qwen2.5:3b"))

    assert preview.status == "preview_only"


def test_preview_as_dict_is_structured():
    data = preview_route(RoutingPreviewRequest(requested_model="gpt-4.1-mini")).as_dict()

    assert data["status"] == "preview_only"
    assert data["recommended_mode"] == "openai"
    assert isinstance(data["fallbacks"], list)
    assert isinstance(data["reasons"], list)
    assert data["evidence_boundary"]["runs_provider"] is False
