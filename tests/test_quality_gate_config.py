import importlib
import builtins

import pytest

from alpha.core.config import get_quality_gate, QualityGateConfig


def test_get_quality_gate_with_yaml():
    pytest.importorskip('yaml')
    cfg = get_quality_gate()
    assert isinstance(cfg, QualityGateConfig)
    assert cfg.min_accuracy == pytest.approx(0.85)
    assert cfg.max_p95_ms == 750
    assert cfg.max_p99_ms == 1200
    assert cfg.max_cost_per_call == pytest.approx(0.01)
    assert cfg.primary_metric == "em"


def test_get_quality_gate_without_yaml(monkeypatch):
    import alpha.core.config as cfg_module

    original_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == 'yaml':
            raise ModuleNotFoundError
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, '__import__', fake_import)
    cfg_module = importlib.reload(cfg_module)
    assert cfg_module.yaml is None
    cfg = cfg_module.get_quality_gate()
    assert isinstance(cfg, cfg_module.QualityGateConfig)
    assert cfg.min_accuracy == pytest.approx(0.85)
    assert cfg.max_p95_ms == 750
    assert cfg.max_p99_ms == 1200
    assert cfg.max_cost_per_call == pytest.approx(0.01)
    assert cfg.primary_metric == "em"
