"""Focused tests for the read-only Alpha Solver Operator Console shell.

These assert the console is:

* mounted on the real ``service.app:app`` behind the shared dashboard
  auth/CSRF middleware (fail-closed, session-protected);
* live-provider disabled by default with a disabled live-run button;
* free of any raw secret value in HTML or JSON;
* reachable without exercising any provider-call path.

They mirror the wiring/auth style of ``tests/ui/test_expert_preview_real_app.py``.
"""

from __future__ import annotations

import html
import sys
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from alpha.webapp.routes import auth, operator_console  # noqa: E402
from service.app import app, _mount_dashboard  # noqa: E402

PAGE_ROUTE = operator_console.ROUTE
STATUS_ROUTE = operator_console.STATUS_ROUTE

# A recognizable fake secret. It is placed in the environment and must never
# appear in any console response (HTML or JSON).
FAKE_SECRET = "sk-operator-console-should-never-render-0123456789"


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("ALPHA_DASHBOARD_PASSWORD", "testing-secret")
    monkeypatch.setenv("ALPHA_DASHBOARD_SECRET_KEY", "unit-test-secret")
    monkeypatch.setenv("MODEL_PROVIDER", "local")
    auth.reset_state()

    # https base_url: login sets Secure cookies the test client only resends
    # over https.
    test_client = TestClient(app, base_url="https://testserver")
    try:
        yield test_client
    finally:
        test_client.close()
        auth.reset_state()


def _login(client: TestClient) -> None:
    response = client.post(
        "/login", data={"password": "testing-secret"}, follow_redirects=False
    )
    assert response.status_code == 303
    assert client.cookies.get(auth.SESSION_COOKIE_NAME)


# ---------------------------------------------------------------------------
# Mounting and protection
# ---------------------------------------------------------------------------
def test_routes_registered_in_real_app() -> None:
    paths = {getattr(route, "path", None) for route in app.routes}
    assert PAGE_ROUTE in paths
    assert STATUS_ROUTE in paths


def test_mount_dashboard_adds_protected_console_routes() -> None:
    fresh = FastAPI()
    _mount_dashboard(fresh)

    paths = {getattr(route, "path", None) for route in fresh.routes}
    assert PAGE_ROUTE in paths
    assert STATUS_ROUTE in paths

    fresh_client = TestClient(fresh, base_url="https://testserver")
    try:
        response = fresh_client.get(PAGE_ROUTE, follow_redirects=False)
    finally:
        fresh_client.close()
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_unmounted_app_does_not_serve_console() -> None:
    """Without an explicit mount the console is not globally registered."""

    bare = FastAPI()
    bare_client = TestClient(bare, base_url="https://testserver")
    try:
        assert bare_client.get(PAGE_ROUTE).status_code == 404
        assert bare_client.get(STATUS_ROUTE).status_code == 404
    finally:
        bare_client.close()


def test_logged_out_page_redirects_to_login(client: TestClient) -> None:
    response = client.get(PAGE_ROUTE, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_logged_out_status_redirects_to_login(client: TestClient) -> None:
    response = client.get(STATUS_ROUTE, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


# ---------------------------------------------------------------------------
# Rendered shell content
# ---------------------------------------------------------------------------
def test_authenticated_page_renders_all_cards(client: TestClient) -> None:
    _login(client)
    response = client.get(PAGE_ROUTE)
    assert response.status_code == 200
    html = response.text

    for card_id in (
        "card-portable-contract",
        "card-run-setup",
        "card-route-trace",
        "card-provider-gate",
        "card-preflight-capture",
        "card-evidence-receipt",
    ):
        assert card_id in html

    assert "Alpha Solver Operator Console" in html


def test_authenticated_page_includes_boundary_text(client: TestClient) -> None:
    _login(client)
    html = client.get(PAGE_ROUTE).text

    assert operator_console.LOCAL_FIRST_TEXT in html
    assert operator_console.LIVE_DISABLED_TEXT in html
    assert operator_console.ARTIFACT_BOUNDARY_TEXT in html
    assert operator_console.NO_KEYS_TEXT in html


def test_live_run_button_is_disabled_in_page(client: TestClient) -> None:
    _login(client)
    html = client.get(PAGE_ROUTE).text
    assert "Live run (disabled)" in html
    assert "class=\"disabled-btn\" disabled" in html


def test_preflight_workflows_present_without_scoring_language(
    client: TestClient,
) -> None:
    _login(client)
    html = client.get(PAGE_ROUTE).text
    for workflow in (
        "anchor-preflight",
        "lift-preflight",
        "init-capture",
        "validate-capture",
        "export-evidence-packet",
    ):
        assert workflow in html
    # No scoring/ranking/winner language.
    for forbidden in ("winner", "ranking", "leaderboard", "score:"):
        assert forbidden not in html.lower()


def test_init_capture_command_includes_required_case_packet(
    client: TestClient,
) -> None:
    _login(client)
    expected_command = (
        "python scripts/operator_run_capture.py init "
        "--case-packet <case_packet.json> --out <capture.json>"
    )

    payload = client.get(STATUS_ROUTE).json()
    workflows = {
        workflow["id"]: workflow["command"]
        for workflow in payload["preflight_capture"]["workflows"]
    }

    assert workflows["init-capture"] == expected_command
    assert html.escape(expected_command) in client.get(PAGE_ROUTE).text


# ---------------------------------------------------------------------------
# Status JSON shape and provider gate
# ---------------------------------------------------------------------------
def test_status_json_shape(client: TestClient) -> None:
    _login(client)
    response = client.get(STATUS_ROUTE)
    assert response.status_code == 200
    payload = response.json()

    for section in (
        "console",
        "portable_contract",
        "run_setup",
        "route_trace",
        "provider_gate",
        "preflight_capture",
        "evidence_receipt",
    ):
        assert section in payload

    assert payload["console"]["mode"] == "local-first"
    assert payload["portable_contract"]["present"] is True
    assert payload["portable_contract"]["source_path"] == "alpha_solver_portable.py"


def test_status_live_provider_disabled_by_default(client: TestClient) -> None:
    _login(client)
    payload = client.get(STATUS_ROUTE).json()

    assert payload["console"]["live_provider_calls"] == "disabled"
    assert payload["provider_gate"]["live_provider_calls"] == "disabled"
    assert payload["provider_gate"]["console_calls_providers"] is False
    assert payload["run_setup"]["live_run_button_enabled"] is False

    live_modes = [
        mode
        for mode in payload["run_setup"]["run_modes"]
        if mode["id"] == "live-provider"
    ]
    assert live_modes and live_modes[0]["available"] is False


def test_status_key_status_is_categorical_only(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", FAKE_SECRET)
    _login(client)
    payload = client.get(STATUS_ROUTE).json()

    key_status = payload["provider_gate"]["key_status"]
    assert key_status["OPENAI_API_KEY"] == "present"
    for value in key_status.values():
        assert value in {"present", "missing", "unknown"}


# ---------------------------------------------------------------------------
# Secret non-leakage
# ---------------------------------------------------------------------------
def test_fake_secret_never_leaks_in_html(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", FAKE_SECRET)
    _login(client)
    html = client.get(PAGE_ROUTE).text
    assert FAKE_SECRET not in html
    # The key is still reported as present (categorical), just never by value.
    assert "OPENAI_API_KEY" in html


def test_fake_secret_never_leaks_in_json(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", FAKE_SECRET)
    _login(client)
    response = client.get(STATUS_ROUTE)
    assert FAKE_SECRET not in response.text


def test_build_console_status_never_embeds_secret_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", FAKE_SECRET)
    monkeypatch.setenv("ALPHA_DASHBOARD_SECRET_KEY", "another-fake-secret-value")
    status = operator_console.build_console_status()
    assert FAKE_SECRET not in repr(status)
    assert "another-fake-secret-value" not in repr(status)


# ---------------------------------------------------------------------------
# No provider-call path
# ---------------------------------------------------------------------------
def test_console_never_calls_provider_client(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Rendering the console must not construct or execute a provider client."""

    import alpha.providers.openai as openai_provider

    def _boom(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("provider client must not be used by operator console")

    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "__init__", _boom)
    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "execute", _boom)
    monkeypatch.setattr(
        app.state,
        "provider_client_factory",
        lambda *_a, **_k: _boom(),
        raising=False,
    )

    _login(client)
    assert client.get(PAGE_ROUTE).status_code == 200
    assert client.get(STATUS_ROUTE).status_code == 200


def test_console_module_does_not_import_provider_clients() -> None:
    """The module source must not reference provider client classes."""

    source = Path(operator_console.__file__).read_text(encoding="utf-8")
    for forbidden in ("ProviderClient", "OpenAIProviderClient", "httpx", "requests."):
        assert forbidden not in source
