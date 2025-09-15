import os
import subprocess
import sys

import pytest
from _pytest.monkeypatch import MonkeyPatch
import yaml

from service.auth.jwt_utils import AuthKeyStore
from service.config.loader import load_config
from service.config.validators import validate


@pytest.fixture(scope="session", autouse=True)
def _hires_auth_reload():
    mp = MonkeyPatch()
    orig_reload = AuthKeyStore.reload

    def reload(self, force: bool = False) -> None:  # type: ignore[override]
        try:
            mtime = self.path.stat().st_mtime_ns
        except FileNotFoundError:
            self._keys = {}
            self._mtime = 0
            return
        if force or mtime != getattr(self, "_mtime", 0):
            with self.path.open() as f:
                data = yaml.safe_load(f) or {}
            keys = {}
            for kid, value in data.items():
                if isinstance(value, dict):
                    pem = value.get("public_key") or value.get("key") or ""
                else:
                    pem = value or ""
                keys[kid] = pem
            self._keys = keys
            self._mtime = mtime

    mp.setattr(AuthKeyStore, "reload", reload)
    yield
    mp.setattr(AuthKeyStore, "reload", orig_reload)


def test_load_and_validate_default():
    env = {"MODEL_PROVIDER": "openai", "OPENAI_API_KEY": "sk"}
    cfg = load_config(env=env)
    assert cfg["models"]["provider"] == "openai"
    validate(cfg)


def test_env_override():
    env = {
        "MODEL_PROVIDER": "dummy",
        "OPENAI_API_KEY": "x",
        "SERVER_HOST": "127.0.0.1",
    }
    cfg = load_config(env=env)
    assert cfg["models"]["provider"] == "dummy"
    assert cfg["server"]["host"] == "127.0.0.1"


def test_validate_bad_provider():
    cfg = load_config(env={"MODEL_PROVIDER": "bad", "OPENAI_API_KEY": "x"})
    with pytest.raises(ValueError, match="models.provider"):
        validate(cfg)


def test_validate_negative_threshold():
    env = {"MODEL_PROVIDER": "openai", "OPENAI_API_KEY": "x"}
    cfg = load_config(env=env)
    cfg["gates"]["low_conf_threshold"] = -0.1
    with pytest.raises(ValueError, match="gates.low_conf_threshold"):
        validate(cfg)


def _run_check_env(extra_env):
    env = os.environ.copy()
    env.update(extra_env)
    return subprocess.run(
        [sys.executable, "scripts/check_env.py"], env=env, capture_output=True, text=True
    )


def test_check_env_success():
    result = _run_check_env({"MODEL_PROVIDER": "openai", "OPENAI_API_KEY": "sk"})
    assert result.returncode == 0
    assert "Environment looks good" in result.stdout


def test_check_env_missing_var():
    result = _run_check_env({"MODEL_PROVIDER": "openai"})
    assert result.returncode != 0
    assert "OPENAI_API_KEY" in result.stdout


def test_redaction(caplog):
    with caplog.at_level("DEBUG"):
        load_config(env={"MODEL_PROVIDER": "openai", "OPENAI_API_KEY": "secret"})
    assert "secret" not in caplog.text
