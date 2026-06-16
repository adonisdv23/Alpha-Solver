from alpha.model_catalog import ModelCatalog


EXPECTED_LOCAL_MODELS = {"qwen2.5:3b", "gemma3:4b", "llama3.2:1b", "llama3.2:latest"}
EXPECTED_OPENAI_MODELS = {"gpt-4.1-mini", "gpt-4.1", "gpt-4o-mini"}


def test_catalog_loads_successfully():
    catalog = ModelCatalog.load()

    assert catalog.version
    assert catalog.models
    assert catalog.evidence_boundary == {
        "runs_provider": False,
        "runs_local_model": False,
        "quality_evidence": False,
        "readiness_evidence": False,
        "benchmark_evidence": False,
    }


def test_catalog_includes_expected_local_models():
    catalog = ModelCatalog.load()

    assert EXPECTED_LOCAL_MODELS <= {model.model_id for model in catalog.by_mode("local", enabled_only=False)}


def test_catalog_includes_expected_openai_models():
    catalog = ModelCatalog.load()

    assert EXPECTED_OPENAI_MODELS <= {model.model_id for model in catalog.by_mode("openai", enabled_only=False)}


def test_each_model_entry_has_required_no_quality_claim_metadata():
    catalog = ModelCatalog.load()

    for model in catalog.models:
        assert model.provider
        assert model.mode in {"local", "openai"}
        assert model.model_id
        assert isinstance(model.smoke_eligible, bool)
        assert model.quality_claim is False
        assert "not" in model.notes.lower()
