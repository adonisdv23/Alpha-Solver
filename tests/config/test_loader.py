from alpha.config.loader import load_config


def test_env_and_cli_layering(monkeypatch) -> None:
    monkeypatch.setenv("ALPHA_BRANCHING_FACTOR", "5")
    cfg = load_config(branching_factor=7)
    assert cfg["branching_factor"] == 7
    assert cfg["seed"] == 42


def test_determinism_flag(monkeypatch) -> None:
    monkeypatch.setenv("ALPHA_DETERMINISM", "1")
    cfg = load_config()
    assert cfg["ts"] == 0
    assert cfg["seed"] == 42
