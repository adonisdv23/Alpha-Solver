"""Authentication and session management for the dashboard UI."""

from __future__ import annotations

import hmac
import os
import secrets
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Optional, Tuple
from urllib.parse import parse_qs

from fastapi import APIRouter, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

__all__ = [
    "router",
    "install_dashboard_security",
    "reset_state",
    "SESSION_COOKIE_NAME",
    "CSRF_COOKIE_NAME",
    "CSRF_HEADER_NAME",
]


# Constants governing cookie and session behaviour.
SESSION_COOKIE_NAME = "alpha_dashboard_session"
CSRF_COOKIE_NAME = "alpha_dashboard_csrf"
CSRF_HEADER_NAME = "x-alpha-csrf"

PASSWORD_ENV_VAR = "ALPHA_DASHBOARD_PASSWORD"
SECRET_ENV_VAR = "ALPHA_DASHBOARD_SECRET_KEY"

SESSION_TTL_SECONDS = 60 * 60  # one hour
LOCKOUT_THRESHOLD = 5
LOCKOUT_DURATION_SECONDS = 5 * 60  # five minutes

_PROTECTED_PREFIXES: Tuple[str, ...] = ("/requests", "/settings", "/run")
_CSRF_METHODS = {"POST", "PUT", "PATCH", "DELETE"}

_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
_LOGIN_TEMPLATE_PATH = _TEMPLATE_DIR / "login.html"


@dataclass
class SessionData:
    """Metadata describing an authenticated dashboard session."""

    session_id: str
    created_at: float
    expires_at: float
    csrf_token: str


@dataclass
class AttemptState:
    """Track failed login attempts for a particular client."""

    failures: int = 0
    locked_until: float = 0.0


router = APIRouter()


_SESSIONS: Dict[str, SessionData] = {}
_SESSIONS_LOCK = threading.Lock()

_ATTEMPTS: Dict[str, AttemptState] = {}
_ATTEMPTS_LOCK = threading.Lock()

_SECRET_KEY: Optional[str] = None


def reset_state() -> None:
    """Reset in-memory authentication state (used by tests)."""

    global _SECRET_KEY
    with _SESSIONS_LOCK:
        _SESSIONS.clear()
    with _ATTEMPTS_LOCK:
        _ATTEMPTS.clear()
    _SECRET_KEY = None


def _get_secret_key() -> str:
    """Return the secret key used to sign session cookies."""

    global _SECRET_KEY
    if _SECRET_KEY:
        return _SECRET_KEY
    env_value = os.getenv(SECRET_ENV_VAR)
    if env_value:
        _SECRET_KEY = env_value
    else:
        _SECRET_KEY = secrets.token_hex(32)
    return _SECRET_KEY


def _sign_session_id(session_id: str) -> str:
    secret = _get_secret_key().encode("utf-8")
    message = session_id.encode("utf-8")
    digest = hmac.new(secret, message, "sha256").hexdigest()
    return digest


def _serialize_session(session: SessionData) -> str:
    signature = _sign_session_id(session.session_id)
    return f"{session.session_id}.{signature}"


def _verify_serialized_session(value: str) -> Optional[str]:
    try:
        session_id, signature = value.split(".", 1)
    except ValueError:
        return None
    expected = _sign_session_id(session_id)
    if not hmac.compare_digest(signature, expected):
        return None
    return session_id


def _create_session() -> SessionData:
    now = time.monotonic()
    session_id = secrets.token_hex(32)
    csrf_token = secrets.token_hex(32)
    session = SessionData(
        session_id=session_id,
        created_at=now,
        expires_at=now + SESSION_TTL_SECONDS,
        csrf_token=csrf_token,
    )
    with _SESSIONS_LOCK:
        _SESSIONS[session_id] = session
    return session


def _delete_session(session_id: str) -> None:
    with _SESSIONS_LOCK:
        _SESSIONS.pop(session_id, None)


def _load_session(session_id: str) -> Optional[SessionData]:
    now = time.monotonic()
    with _SESSIONS_LOCK:
        session = _SESSIONS.get(session_id)
        if not session:
            return None
        if session.expires_at <= now:
            _SESSIONS.pop(session_id, None)
            return None
        return session


def _client_identifier(request: Request) -> str:
    host = getattr(request.client, "host", None)
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        host = forwarded.split(",")[0].strip()
    return host or "unknown-client"


def _is_locked(identifier: str) -> bool:
    now = time.monotonic()
    with _ATTEMPTS_LOCK:
        state = _ATTEMPTS.get(identifier)
        if not state:
            return False
        if state.locked_until and now < state.locked_until:
            return True
        if state.locked_until and now >= state.locked_until:
            _ATTEMPTS.pop(identifier, None)
        return False


def _record_failure(identifier: str) -> None:
    now = time.monotonic()
    with _ATTEMPTS_LOCK:
        state = _ATTEMPTS.setdefault(identifier, AttemptState())
        if state.locked_until and now < state.locked_until:
            return
        state.failures += 1
        if state.failures >= LOCKOUT_THRESHOLD:
            state.locked_until = now + LOCKOUT_DURATION_SECONDS
        else:
            state.locked_until = 0.0


def _record_success(identifier: str) -> None:
    with _ATTEMPTS_LOCK:
        _ATTEMPTS.pop(identifier, None)


def _render_login_template(error_message: str = "") -> str:
    base = _LOGIN_TEMPLATE_PATH.read_text(encoding="utf-8")
    if error_message:
        error_block = f"<p class=\"error\" role=\"alert\">{error_message}</p>"
    else:
        error_block = ""
    return base.replace("[[ERROR_MESSAGE]]", error_block)


async def _extract_login_payload(request: Request) -> Dict[str, str]:
    content_type = request.headers.get("content-type", "").lower()
    if "application/json" in content_type:
        payload = await request.json()
        if isinstance(payload, dict):
            return {str(key): "" if value is None else str(value) for key, value in payload.items()}
        return {}

    body = await request.body()
    if not body:
        return {}
    parsed = parse_qs(body.decode())
    return {key: values[0] if values else "" for key, values in parsed.items()}


def _expected_password() -> str:
    password = os.getenv(PASSWORD_ENV_VAR)
    if password is None:
        return "alpha-dashboard"
    return password


def _build_lockout_response() -> HTMLResponse:
    html = _render_login_template("Too many failed attempts. Try again later.")
    return HTMLResponse(content=html, status_code=status.HTTP_429_TOO_MANY_REQUESTS)


@router.get("/login", response_class=HTMLResponse)
async def login_form() -> HTMLResponse:
    return HTMLResponse(content=_render_login_template())


@router.post("/login")
async def login(request: Request) -> Response:
    identifier = _client_identifier(request)
    if _is_locked(identifier):
        return _build_lockout_response()

    payload = await _extract_login_payload(request)
    supplied_password = str(payload.get("password", ""))
    if secrets.compare_digest(supplied_password, _expected_password()):
        _record_success(identifier)
        session = _create_session()
        response = RedirectResponse("/requests", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(
            CSRF_COOKIE_NAME,
            session.csrf_token,
            secure=True,
            httponly=False,
            samesite="strict",
            max_age=SESSION_TTL_SECONDS,
        )
        response.set_cookie(
            SESSION_COOKIE_NAME,
            _serialize_session(session),
            secure=True,
            httponly=True,
            samesite="strict",
            max_age=SESSION_TTL_SECONDS,
        )
        return response

    _record_failure(identifier)
    html = _render_login_template("Invalid credentials")
    return HTMLResponse(content=html, status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/logout")
async def logout(request: Request) -> Response:
    cookie = request.cookies.get(SESSION_COOKIE_NAME)
    if cookie:
        session_id = _verify_serialized_session(cookie)
        if session_id:
            _delete_session(session_id)
    response = RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(SESSION_COOKIE_NAME)
    response.delete_cookie(CSRF_COOKIE_NAME)
    return response


def _is_protected_path(path: str, protected: Iterable[str]) -> bool:
    for prefix in protected:
        if path == prefix or path.startswith(prefix + "/"):
            return True
    return False


def _require_session(request: Request) -> SessionData:
    cookie = request.cookies.get(SESSION_COOKIE_NAME)
    if not cookie:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "not authenticated")
    session_id = _verify_serialized_session(cookie)
    if not session_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid session")
    session = _load_session(session_id)
    if not session:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "session expired")
    request.state.alpha_dashboard_session = session
    return session


def _enforce_csrf(request: Request, session: SessionData) -> None:
    header_token = request.headers.get(CSRF_HEADER_NAME)
    if not header_token:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "missing CSRF token")
    if not secrets.compare_digest(header_token, session.csrf_token):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "invalid CSRF token")


def install_dashboard_security(
    app: FastAPI, protected_prefixes: Iterable[str] | None = None
) -> None:
    """Install middleware enforcing authentication and CSRF checks."""

    prefixes: Tuple[str, ...]
    if protected_prefixes is None:
        prefixes = _PROTECTED_PREFIXES
    else:
        prefixes = tuple(sorted(set(protected_prefixes)))

    if getattr(app.state, "alpha_dashboard_security_installed", False):
        app.state.alpha_dashboard_protected = prefixes
        return

    app.state.alpha_dashboard_security_installed = True
    app.state.alpha_dashboard_protected = prefixes

    @app.middleware("http")
    async def _dashboard_security(request: Request, call_next):  # type: ignore[override]
        path = request.url.path
        protected = getattr(app.state, "alpha_dashboard_protected", prefixes)
        requires_guard = _is_protected_path(path, protected)
        is_login = path.startswith("/login")
        is_logout = path.startswith("/logout")

        if requires_guard:
            try:
                session = _require_session(request)
            except HTTPException as exc:
                if request.method.upper() == "GET":
                    return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
                return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)

            if request.method.upper() in _CSRF_METHODS:
                try:
                    _enforce_csrf(request, session)
                except HTTPException as exc:
                    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)

        elif not (is_login or is_logout):
            request.state.alpha_dashboard_session = None  # type: ignore[attr-defined]

        response = await call_next(request)
        return response
