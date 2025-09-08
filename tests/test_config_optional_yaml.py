import pytest


def test_get_quality_gate_without_yaml(monkeypatch):
    import alpha.core.config as cfg
    monkeypatch.setattr(cfg, "yaml", None)
    cfg_val = cfg.get_quality_gate()
    assert cfg_val.min_accuracy == 0.85


def test_get_quality_gate_with_yaml():
    pytest.importorskip("yaml")
    import alpha.core.config as cfg
    cfg_val = cfg.get_quality_gate()
    assert cfg_val.min_accuracy == 0.85
