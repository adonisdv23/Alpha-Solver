from alpha.model_router import RoutingPreviewRequest, preview_route
from tools.operator_smoke_runner import MAX_PROMPT_CHARS


def test_router_selects_requested_enabled_openai_model_when_hosted_allowed():
    preview = preview_route(RoutingPreviewRequest(requested_mode="openai", requested_model="gpt-4.1-mini", allow_hosted_providers=True))

    assert preview.status == "preview_only"
    assert preview.recommended_mode == "openai"
    assert preview.recommended_model == "gpt-4.1-mini"
    assert "model_available_in_catalog" in preview.reasons
    assert "smoke_eligible" in preview.reasons
    assert preview.provider_or_local_execution_authorized is False
    assert preview.selected_backend_type == "hosted"
    assert preview.no_call_evidence is True
    assert preview.operator_caveat == "Catalog inclusion is not model quality evidence."


def test_router_selects_requested_enabled_local_model_when_local_allowed():
    preview = preview_route(RoutingPreviewRequest(requested_mode="local", requested_model="qwen2.5:3b", allow_local=True))

    assert preview.status == "preview_only"
    assert preview.recommended_mode == "local"
    assert preview.recommended_model == "qwen2.5:3b"
    assert preview.selected_backend_type == "local"


def test_local_only_request_avoids_hosted_recommendations_unless_fallback_is_stated():
    preview = preview_route(RoutingPreviewRequest(local_only=True, allow_local=True, allow_hosted_providers=True))

    assert preview.status == "preview_only"
    assert preview.recommended_mode == "local"
    assert all(fallback.mode == "local" for fallback in preview.fallbacks)
    assert "local_only_request_suppresses_hosted_recommendations" in preview.warnings


def test_hosted_disabled_request_for_hosted_model_fails_closed_with_local_fallback():
    preview = preview_route(RoutingPreviewRequest(requested_model="gpt-4.1-mini", allow_hosted_providers=False, allow_local=True))

    assert preview.status == "failed_closed"
    assert preview.recommended_model is None
    assert "hosted_provider_not_allowed" in preview.reasons
    assert "local_fallback_available" in preview.warnings
    assert preview.fallbacks
    assert all(fallback.mode == "local" for fallback in preview.fallbacks)


def test_hosted_disabled_warning_only_announces_metadata_filtered_local_fallback():
    preview = preview_route(
        RoutingPreviewRequest(
            requested_model="gpt-4.1-mini",
            required_capability="json_capable",
            allow_hosted_providers=False,
            allow_local=True,
        )
    )

    assert preview.status == "failed_closed"
    assert "hosted_provider_not_allowed" in preview.reasons
    assert "local_fallback_available" not in preview.warnings
    assert "hosted_execution_disabled" in preview.warnings
    assert preview.fallbacks == ()


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


def test_router_returns_failed_closed_preview_for_prompt_above_smoke_limit_with_warning():
    preview = preview_route(RoutingPreviewRequest(prompt_length=MAX_PROMPT_CHARS + 1))

    assert preview.status == "failed_closed"
    assert "prompt_too_long_for_smoke_runner" in preview.reasons
    assert "prompt_length_exceeds_preview_smoke_boundary" in preview.warnings


def test_router_includes_metadata_reasons_without_validation_claims():
    preview = preview_route(RoutingPreviewRequest(requested_mode="openai", requested_model="gpt-4.1-mini", required_capability="json_capable"))

    assert preview.reasons
    assert "routing_preview_only" in preview.reasons
    assert "openai_requested_by_operator" in preview.reasons
    assert "required_capability_recorded_metadata_only" in preview.reasons
    assert "required_capability_matched_as_metadata_only" in preview.reasons
    assert preview.evidence_boundary["quality_evidence"] is False


def test_router_includes_preview_only_evidence_boundary_flags():
    preview = preview_route(RoutingPreviewRequest())

    assert preview.evidence_boundary == {
        "runs_provider": False,
        "runs_local_model": False,
        "quality_evidence": False,
        "readiness_evidence": False,
        "benchmark_evidence": False,
    }
    assert preview.provider_or_local_execution_authorized is False


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


def test_route_preview_surfaces_cost_latency_context_privacy_and_capability_reasons():
    preview = preview_route(
        RoutingPreviewRequest(
            requested_model="gpt-4.1-mini",
            required_capability="json_capable",
            required_context_tier="high",
            privacy_preference="hosted_provider_boundary",
        )
    )

    assert preview.status == "preview_only"
    assert "cost_tier_reason:medium" in preview.reasons
    assert "latency_tier_reason:medium" in preview.reasons
    assert "context_tier_reason:high" in preview.reasons
    assert "privacy_tier_reason:hosted_provider_boundary" in preview.reasons
    assert "capability_tag_match:json_capable" in preview.reasons
    assert "catalog_inclusion_not_quality_evidence" in preview.reasons


def test_fallback_candidates_are_fallback_eligible_and_tag_compatible():
    preview = preview_route(RoutingPreviewRequest(required_capability="local_runtime", allow_local=True, allow_hosted_providers=True))

    assert preview.fallbacks
    assert all(fallback.fallback_eligible for fallback in preview.fallbacks)
    assert all(fallback.mode == "local" for fallback in preview.fallbacks)


def test_required_context_tier_is_hard_filter_and_can_route_to_hosted():
    preview = preview_route(RoutingPreviewRequest(required_context_tier="high"))

    assert preview.status == "preview_only"
    assert preview.selected_context_tier == "high"
    assert preview.selected_context_tier != "low"
    assert preview.recommended_mode == "openai"


def test_privacy_preference_is_hard_filter_and_hosted_alias_excludes_local():
    preview = preview_route(RoutingPreviewRequest(privacy_preference="hosted"))

    assert preview.status == "preview_only"
    assert preview.recommended_mode == "openai"
    assert preview.selected_backend_type == "hosted"
    assert preview.selected_privacy_tier.startswith("hosted")


def test_unsatisfied_hard_metadata_filter_fails_closed():
    preview = preview_route(RoutingPreviewRequest(required_context_tier="ultra"))

    assert preview.status == "failed_closed"
    assert preview.recommended_model is None
    assert "no_eligible_model" in preview.reasons


def test_requested_model_must_satisfy_hard_metadata_filters():
    preview = preview_route(RoutingPreviewRequest(requested_model="qwen2.5:3b", required_context_tier="high"))

    assert preview.status == "failed_closed"
    assert preview.recommended_model is None
    assert "requested_model_missing_required_context_tier" in preview.reasons


def test_metadata_preferences_keep_routing_deterministic():
    req = RoutingPreviewRequest(cost_preference="low", latency_preference="medium", task_profile="general")

    previews = [preview_route(req).as_dict() for _ in range(3)]

    assert previews[0] == previews[1] == previews[2]
    assert previews[0]["recommended_mode"] == "local"


def test_required_capability_filters_recommendations_metadata_only():
    preview = preview_route(RoutingPreviewRequest(required_capability="vision_capable", allow_local=True, allow_hosted_providers=True))

    assert preview.status == "preview_only"
    assert preview.recommended_model == "gpt-4o-mini"
    assert preview.provider_or_local_execution_authorized is False


def test_requested_model_missing_required_capability_fails_closed():
    preview = preview_route(RoutingPreviewRequest(requested_model="qwen2.5:3b", required_capability="vision_capable"))

    assert preview.status == "failed_closed"
    assert "required_capability_recorded_metadata_only" in preview.reasons
    assert "required_capability_matched_as_metadata_only" not in preview.reasons
    assert "requested_model_missing_required_capability" in preview.reasons


def test_prior_smoke_only_evidence_boundaries_are_preserved():
    preview = preview_route(RoutingPreviewRequest(requested_model="qwen2.5:3b"))

    assert preview.status == "preview_only"
    assert preview.evidence_boundary == {
        "runs_provider": False,
        "runs_local_model": False,
        "quality_evidence": False,
        "readiness_evidence": False,
        "benchmark_evidence": False,
    }


def test_preview_as_dict_is_structured():
    data = preview_route(RoutingPreviewRequest(requested_model="gpt-4.1-mini")).as_dict()

    assert data["status"] == "preview_only"
    assert data["recommended_mode"] == "openai"
    assert isinstance(data["fallbacks"], list)
    assert isinstance(data["reasons"], list)
    assert data["evidence_boundary"]["runs_provider"] is False
    assert data["provider_or_local_execution_authorized"] is False
    assert data["selected_backend_type"] == "hosted"
    assert data["selected_smoke_eligible"] is True
    assert data["no_call_evidence"] is True
