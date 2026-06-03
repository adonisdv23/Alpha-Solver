import pytest

from service.models.modelset_registry import ModelSetRegistry, ModelSetError


def test_registry_loads_sets():
    reg = ModelSetRegistry()
    names = reg.names()
    assert "a3_live_capture" in names
    assert "default" in names and "cost_saver" in names
    # deterministic ordering
    assert names == sorted(names)
    # ensure data accessible and existing model sets are preserved
    default_ms = reg.get("default")
    assert default_ms.provider == "openai"
    assert default_ms.model == "gpt-5"
    assert default_ms.max_tokens == 2048
    assert default_ms.timeout_ms == 60000

    saver_ms = reg.get("cost_saver")
    assert saver_ms.provider == "openai"
    assert saver_ms.model == "gpt-5-mini"
    assert saver_ms.max_tokens == 1024
    assert saver_ms.timeout_ms == 45000

    a3_ms = reg.get("a3_live_capture")
    assert a3_ms.provider == "openai"
    assert a3_ms.model == "gpt-5-mini"
    assert a3_ms.max_tokens == 4096
    assert a3_ms.timeout_ms == 60000
    assert a3_ms.price_hint == saver_ms.price_hint


def test_invalid_schema_missing_model(tmp_path):
    cfg = tmp_path / "model_sets.yaml"
    cfg.write_text(
        """model_sets:
  bad:
    provider: openai
    max_tokens: 1
    timeout_ms: 1
"""
    )
    with pytest.raises(ModelSetError) as exc:
        ModelSetRegistry(cfg)
    assert "missing" in str(exc.value)


def test_invalid_provider(tmp_path):
    cfg = tmp_path / "model_sets.yaml"
    cfg.write_text(
        """model_sets:
  bad:
    provider: nope
    model: m
    max_tokens: 1
    timeout_ms: 1
"""
    )
    with pytest.raises(ModelSetError) as exc:
        ModelSetRegistry(cfg)
    assert "unknown provider" in str(exc.value)


def test_deterministic_order(tmp_path):
    cfg = tmp_path / "model_sets.yaml"
    cfg.write_text(
        """model_sets:
  zed:
    provider: openai
    model: z
    max_tokens: 1
    timeout_ms: 1
  alpha:
    provider: openai
    model: a
    max_tokens: 1
    timeout_ms: 1
"""
    )
    reg = ModelSetRegistry(cfg)
    assert reg.names() == ["alpha", "zed"]

