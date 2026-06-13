from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from alpha.webapp.routes import settings


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    secrets_path = tmp_path / "dashboard-private" / "secrets.json"
    audit_path = tmp_path / "dashboard-private" / "audit.log"
    monkeypatch.setenv("ALPHA_DASHBOARD_SECRETS_PATH", str(secrets_path))
    monkeypatch.setenv("ALPHA_DASHBOARD_AUDIT_LOG", str(audit_path))

    app = FastAPI()
    app.include_router(settings.router)
    client = TestClient(app)
    try:
        yield client, secrets_path, audit_path
    finally:
        client.close()


def _post_key(client: TestClient, provider: str, key: str) -> None:
    response = client.post(
        "/settings/keys",
        data={"provider": provider, "key": key},
        follow_redirects=False,
    )
    assert response.status_code == 303


def _delete_key(client: TestClient, provider: str) -> None:
    response = client.post(
        "/settings/keys/delete",
        data={"provider": provider},
        follow_redirects=False,
    )
    assert response.status_code == 303


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _mode(path: Path) -> int:
    return path.stat().st_mode & 0o777


def test_create_key_persists_and_masks_display(client):
    client_app, secrets_path, audit_path = client

    _post_key(client_app, "openai", "sk-openai-12345678")

    stored = _read_json(secrets_path)
    assert stored == {"openai": "sk-openai-12345678"}

    page = client_app.get("/settings")
    assert page.status_code == 200
    assert "****5678" in page.text
    assert "sk-openai-12345678" not in page.text

    log_lines = audit_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(log_lines) == 1
    assert "CREATED" in log_lines[0]
    assert "****5678" in log_lines[0]


@pytest.mark.skipif(os.name != "posix", reason="POSIX file mode assertions are not portable")
def test_key_storage_uses_restrictive_file_and_directory_modes(client):
    client_app, secrets_path, audit_path = client

    _post_key(client_app, "openai", "sk-synthetic-permissions-1234")

    assert _mode(secrets_path.parent) == 0o700
    assert _mode(secrets_path) == 0o600
    assert _mode(audit_path.parent) == 0o700
    assert _mode(audit_path) == 0o600


@pytest.mark.skipif(os.name != "posix", reason="POSIX file mode assertions are not portable")
def test_existing_permissive_secret_file_is_tightened_on_write(tmp_path: Path):
    secrets_path = tmp_path / "nested" / "secrets.json"
    secrets_path.parent.mkdir(parents=True, mode=0o700)
    secrets_path.write_text('{"openai": "sk-synthetic-old-value"}', encoding="utf-8")
    os.chmod(secrets_path.parent, 0o700)
    os.chmod(secrets_path, 0o666)

    backend = settings.FileSecretsBackend(secrets_path)
    backend.set("openai", "sk-synthetic-new-value")

    assert _read_json(secrets_path) == {"openai": "sk-synthetic-new-value"}
    assert _mode(secrets_path.parent) == 0o700
    assert _mode(secrets_path) == 0o600


@pytest.mark.skipif(os.name != "posix", reason="POSIX file mode assertions are not portable")
def test_existing_private_parent_is_not_chmodded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    secrets_path = tmp_path / "operator-owned" / "secrets.json"
    secrets_path.parent.mkdir(parents=True, mode=0o700)
    os.chmod(secrets_path.parent, 0o700)
    chmod_calls: list[tuple[Path, int]] = []
    real_chmod = os.chmod

    def recording_chmod(path: str | os.PathLike[str], mode: int) -> None:
        chmod_calls.append((Path(path), mode))
        real_chmod(path, mode)

    monkeypatch.setattr(settings.os, "chmod", recording_chmod)

    backend = settings.FileSecretsBackend(secrets_path)
    backend.set("openai", "sk-synthetic-private-parent")

    assert (secrets_path.parent, 0o700) not in chmod_calls
    assert _mode(secrets_path.parent) == 0o700
    assert _mode(secrets_path) == 0o600


@pytest.mark.skipif(os.name != "posix", reason="POSIX file mode assertions are not portable")
def test_existing_unsafe_parent_fails_closed_without_chmod_or_secret_write(tmp_path: Path):
    secrets_path = tmp_path / "shared" / "secrets.json"
    audit_path = tmp_path / "shared-audit" / "audit.log"
    secrets_path.parent.mkdir(parents=True, mode=0o755)
    audit_path.parent.mkdir(parents=True, mode=0o750)
    os.chmod(secrets_path.parent, 0o755)
    os.chmod(audit_path.parent, 0o750)

    backend = settings.FileSecretsBackend(secrets_path)
    audit_logger = settings.AuditLogger(audit_path)

    with pytest.raises(PermissionError, match="non-private directory"):
        backend.set("openai", "sk-synthetic-unsafe-parent")
    with pytest.raises(PermissionError, match="non-private directory"):
        audit_logger.log("CREATED", "openai", "****rent")

    assert _mode(secrets_path.parent) == 0o755
    assert _mode(audit_path.parent) == 0o750
    assert not secrets_path.exists()
    assert not audit_path.exists()


def test_update_key_overwrites_value_and_audits(client):
    client_app, secrets_path, audit_path = client

    first = "sk-openai-11112222"
    updated = "sk-openai-33334444"
    _post_key(client_app, "openai", first)
    _post_key(client_app, "openai", updated)

    stored = _read_json(secrets_path)
    assert stored["openai"] == updated

    log_lines = audit_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(log_lines) == 2
    assert "CREATED" in log_lines[0]
    assert "UPDATED" in log_lines[1]
    assert updated not in log_lines[1]
    assert "****4444" in log_lines[1]


def test_delete_key_removes_key_and_logs(client):
    client_app, secrets_path, audit_path = client

    _post_key(client_app, "openai", "sk-openai-55556666")
    _delete_key(client_app, "openai")

    stored = _read_json(secrets_path)
    assert stored == {}

    log_lines = audit_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(log_lines) == 2
    assert "CREATED" in log_lines[0]
    assert "DELETED" in log_lines[1]
    assert "****6666" in log_lines[1]
    assert "sk-openai-55556666" not in " ".join(log_lines)


def test_masking_hides_short_keys(client):
    client_app, _, _ = client

    _post_key(client_app, "claude", "abcd")

    page = client_app.get("/settings")
    assert page.status_code == 200
    assert "****" in page.text
    assert "abcd" not in page.text


def test_audit_log_never_contains_plaintext_key(client):
    client_app, _, audit_path = client

    original = "sk-claude-ABCDE12345"
    updated = "sk-claude-ZYXW98765"

    _post_key(client_app, "claude", original)
    _post_key(client_app, "claude", updated)
    _delete_key(client_app, "claude")

    log_text = audit_path.read_text(encoding="utf-8")
    assert original not in log_text
    assert updated not in log_text
    assert log_text.count("CREATED") == 1
    assert log_text.count("UPDATED") == 1
    assert log_text.count("DELETED") == 1
    assert "****8765" in log_text
