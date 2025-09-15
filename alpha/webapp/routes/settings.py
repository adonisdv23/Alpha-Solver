"""Dashboard settings routes for managing provider API keys."""

from __future__ import annotations

import json
import os
from urllib.parse import parse_qs
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, Optional

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

__all__ = [
    "router",
    "FileSecretsBackend",
    "AuditLogger",
    "mask_secret",
]


def _resolve_path(env_var: str, default_name: str) -> Path:
    """Resolve a filesystem path for persistent storage.

    The location can be overridden through an environment variable. When no
    override is provided we fall back to a directory inside the user's home so
    that persisted data remains outside of version control.
    """

    env_value = os.getenv(env_var)
    if env_value:
        return Path(env_value).expanduser()
    return Path.home() / ".alpha_solver" / default_name


@dataclass(frozen=True)
class ProviderKeyDisplay:
    """View model for representing a stored provider key in the UI."""

    provider: str
    masked_key: str


class SecretsBackend:
    """Abstract interface for a secrets backend."""

    def list(self) -> Dict[str, str]:
        raise NotImplementedError

    def get(self, provider: str) -> Optional[str]:
        raise NotImplementedError

    def set(self, provider: str, key: str) -> None:
        raise NotImplementedError

    def delete(self, provider: str) -> None:
        raise NotImplementedError


class FileSecretsBackend(SecretsBackend):
    """Simple file-based secrets backend storing JSON data."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)

    def list(self) -> Dict[str, str]:
        return dict(self._read())

    def get(self, provider: str) -> Optional[str]:
        return self._read().get(provider)

    def set(self, provider: str, key: str) -> None:
        data = self._read()
        data[provider] = key
        self._write(data)

    def delete(self, provider: str) -> None:
        data = self._read()
        if provider in data:
            data.pop(provider)
            self._write(data)

    def _read(self) -> Dict[str, str]:
        if not self.path.exists():
            return {}
        with self.path.open("r", encoding="utf-8") as file:
            try:
                payload = json.load(file)
            except json.JSONDecodeError:
                payload = {}
        if not isinstance(payload, dict):
            return {}
        return {str(key): str(value) for key, value in payload.items()}

    def _write(self, data: Dict[str, str]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, sort_keys=True)


class AuditLogger:
    """File backed audit logger that stores masked change events."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)

    def log(self, action: str, provider: str, masked_key: str) -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        line = f"{timestamp} | {action.upper()} | {provider} | {masked_key}\n"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as file:
            file.write(line)


def mask_secret(raw_key: Optional[str]) -> str:
    """Return a masked representation of a secret value."""

    if not raw_key:
        return "****"
    if len(raw_key) <= 4:
        return "****"
    return f"****{raw_key[-4:]}"


class SettingsService:
    """Domain logic for manipulating provider API keys."""

    def __init__(self, backend: SecretsBackend, audit_logger: AuditLogger) -> None:
        self._backend = backend
        self._audit = audit_logger

    def list_masked(self) -> Iterable[ProviderKeyDisplay]:
        items = self._backend.list()
        for provider in sorted(items):
            yield ProviderKeyDisplay(provider=provider, masked_key=mask_secret(items[provider]))

    def set_key(self, provider: str, key: str) -> None:
        provider = provider.strip()
        key = key.strip()
        if not provider:
            raise ValueError("provider is required")
        if not key:
            raise ValueError("key is required")
        existing = self._backend.get(provider)
        self._backend.set(provider, key)
        action = "UPDATED" if existing is not None else "CREATED"
        self._audit.log(action, provider, mask_secret(key))

    def delete_key(self, provider: str) -> bool:
        provider = provider.strip()
        if not provider:
            raise ValueError("provider is required")
        existing = self._backend.get(provider)
        if existing is None:
            return False
        self._backend.delete(provider)
        self._audit.log("DELETED", provider, mask_secret(existing))
        return True


TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "templates" / "settings.html"
router = APIRouter()


def _service() -> SettingsService:
    backend_path = _resolve_path("ALPHA_DASHBOARD_SECRETS_PATH", "dashboard_api_keys.json")
    audit_path = _resolve_path("ALPHA_DASHBOARD_AUDIT_LOG", "dashboard_audit.log")
    backend = FileSecretsBackend(backend_path)
    audit_logger = AuditLogger(audit_path)
    return SettingsService(backend, audit_logger)


def _render_settings_template(providers: Iterable[ProviderKeyDisplay]) -> str:
    base = TEMPLATE_PATH.read_text(encoding="utf-8")
    rows: list[str] = []
    for item in providers:
        rows.append(
            """
        <tr>
          <td class="provider">{provider}</td>
          <td class="masked">{masked}</td>
          <td>
            <form method="post" action="/settings/keys" class="inline-form update-form">
              <input type="hidden" name="provider" value="{provider}" />
              <label>
                Update key
                <input type="text" name="key" placeholder="Enter new key" />
              </label>
              <button type="submit">Save</button>
            </form>
            <form method="post" action="/settings/keys/delete" class="inline-form delete-form">
              <input type="hidden" name="provider" value="{provider}" />
              <button type="submit">Delete</button>
            </form>
          </td>
        </tr>
        """.format(provider=item.provider, masked=item.masked_key)
        )

    if rows:
        table_html = """
    <table id="keys-table">
      <thead>
        <tr>
          <th scope="col">Provider</th>
          <th scope="col">Masked API key</th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody>
    {rows}
      </tbody>
    </table>
    """.format(rows="\n".join(row.strip("\n") for row in rows))
    else:
        table_html = '<p id="empty-state">No API keys configured.</p>'

    return base.replace("[[KEYS_TABLE]]", table_html)


@router.get("/settings", response_class=HTMLResponse)
async def settings_page() -> HTMLResponse:
    service = _service()
    providers = list(service.list_masked())
    html = _render_settings_template(providers)
    return HTMLResponse(content=html)


async def _extract_payload(request: Request) -> Dict[str, str]:
    content_type = request.headers.get("content-type", "").lower()
    if "application/json" in content_type:
        payload = await request.json()
        if isinstance(payload, dict):
            return {str(k): "" if v is None else str(v) for k, v in payload.items()}
        return {}

    body = await request.body()
    if not body:
        return {}
    parsed = parse_qs(body.decode())
    return {key: values[0] if values else "" for key, values in parsed.items()}


@router.post("/settings/keys")
async def create_or_update_key(request: Request) -> RedirectResponse:
    service = _service()
    payload = await _extract_payload(request)
    provider = payload.get("provider", "")
    key = payload.get("key", "")
    try:
        service.set_key(provider, key)
    except ValueError as exc:  # pragma: no cover - defensive branch
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc
    return RedirectResponse("/settings", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/settings/keys/delete")
async def delete_key(request: Request) -> RedirectResponse:
    service = _service()
    payload = await _extract_payload(request)
    provider = payload.get("provider", "")
    try:
        service.delete_key(provider)
    except ValueError as exc:  # pragma: no cover - defensive branch
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc
    return RedirectResponse("/settings", status_code=status.HTTP_303_SEE_OTHER)
