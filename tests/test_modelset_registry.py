import pytest

from service.models.modelset_registry import ModelSetRegistry, ModelSetError


def test_registry_loads_sets():
    reg = ModelSetRegistry()
    names = reg.names()
    assert "default" in names and "cost_saver" in names
    # deterministic ordering
    assert names == sorted(names)
    # ensure data accessible
    ms = reg.get("default")
    assert ms.provider == "openai"
    assert ms.max_tokens == 2048


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

