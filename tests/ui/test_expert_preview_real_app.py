"""Wiring/auth tests for the expert-preview page against the REAL application.

These complement ``tests/ui/test_expert_preview.py`` (which exercises the router
inside a throwaway fixture app). They assert that ``/dashboard/expert-preview`` is
actually mounted on ``service.app:app`` and protected by the shared dashboard
auth/CSRF middleware. ``test_route_registered_in_real_app`` is the regression test
that would have caught the route being absent from the runnable app.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from alpha.providers import (
    FakeProviderClient,
    ProviderCost,
    ProviderResult,
    ProviderUsage,
)  # noqa: E402
from alpha.webapp.routes import auth, expert_preview  # noqa: E402
from service.app import app, _dashboard_enabled, _mount_dashboard  # noqa: E402

ROUTE = "/dashboard/expert-preview"


def _provider_result(text: str, *, raw_secret: str | None = None) -> ProviderResult:
    return ProviderResult(
        provider="openai",
        model="gpt-test",
        text=text,
        finish_reason="stop",
        usage=ProviderUsage(input_tokens=1, output_tokens=1, total_tokens=2),
        cost=ProviderCost(estimated_usd=0.0, source="price_hint"),
        latency_ms=1,
        request_id="req-preview",
        raw_metadata={"raw": raw_secret or "hidden", "provider_request_id": "provider-hidden"},
    )


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("ALPHA_DASHBOARD_PASSWORD", "testing-secret")
    monkeypatch.setenv("ALPHA_DASHBOARD_SECRET_KEY", "unit-test-secret")
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    monkeypatch.setenv("ALPHA_LIVE_PREVIEW_ENABLED", "true")
    monkeypatch.setenv("ALPHA_LIVE_PREVIEW_MAX_REQUESTS", "20")
    app.state.live_preview_request_count = 0
    auth.reset_state()

    # ``base_url`` must be https: login sets Secure cookies, which the test client
    # only stores (and resends) over https.
    test_client = TestClient(app, base_url="https://testserver")
    try:
        yield test_client
    finally:
        test_client.close()
        auth.reset_state()


def _assert_loading_state_script(html: str) -> None:
    assert "let previewInFlight = false;" in html
    assert "submitButton.disabled = true;" in html
    assert "Running preview..." in html
    assert '"X-Alpha-CSRF": cookieValue("alpha_dashboard_csrf")' in html
    assert "document.body.innerHTML = nextDocument.body.innerHTML;" in html
    assert "initExpertPreviewForm();" in html


def _assert_long_response_layout(html: str) -> None:
    assert '.panes { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); align-items: start;' in html
    assert '.pane { min-width: 0; }' in html
    assert '.answer, pre { white-space: pre-wrap; overflow-wrap: anywhere; word-break: break-word; }' in html
    assert '.answer { display: block; margin: 0 0 1rem; max-height: none; overflow: visible;' in html


def _login(client: TestClient) -> str:
    response = client.post("/login", data={"password": "testing-secret"}, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == ROUTE
    csrf_token = client.cookies.get(auth.CSRF_COOKIE_NAME)
    assert csrf_token
    return csrf_token


def test_successful_login_redirects_to_expert_preview_and_sets_cookies(
    client: TestClient,
) -> None:
    response = client.post("/login", data={"password": "testing-secret"}, follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == ROUTE
    assert client.cookies.get(auth.SESSION_COOKIE_NAME)
    assert client.cookies.get(auth.CSRF_COOKIE_NAME)


def test_incorrect_password_returns_login_page(client: TestClient) -> None:
    response = client.post("/login", data={"password": "wrong"}, follow_redirects=False)

    assert response.status_code == 401
    assert "Invalid credentials" in response.text
    assert not client.cookies.get(auth.SESSION_COOKIE_NAME)


def test_requests_route_remains_unmounted_in_bundled_app(client: TestClient) -> None:
    _login(client)

    response = client.get("/requests")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_route_registered_in_real_app() -> None:
    """Regression test: the page must be mounted on the runnable app."""

    paths = {getattr(route, "path", None) for route in app.routes}
    assert ROUTE in paths


def test_logged_out_request_redirects_to_login(client: TestClient) -> None:
    response = client.get(ROUTE, follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_authenticated_request_renders_page(client: TestClient) -> None:
    _login(client)

    response = client.get(ROUTE)

    assert response.status_code == 200
    assert expert_preview.DISCLAIMER in response.text
    _assert_loading_state_script(response.text)
    _assert_long_response_layout(response.text)


def test_preview_post_uses_fake_provider_without_network(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    csrf_token = _login(client)
    raw_secret = "sk-preview-should-not-render"
    fake = FakeProviderClient(
        [
            _provider_result("plain same-provider answer", raw_secret=raw_secret),
            _provider_result(
                '{"considerations":["Check timeline risk"],'
                '"assumptions":["Budget is constrained"],"confidence":0.35}',
                raw_secret=raw_secret,
            ),
            _provider_result(
                "draft expert answer that clarify mode replaces", raw_secret=raw_secret
            ),
        ]
    )
    # Inject the fake on the shared app singleton via monkeypatch so it is restored
    # afterwards and never leaks into other tests that import the real app.
    monkeypatch.setattr(
        app.state, "provider_client_factory", lambda _model_set: fake, raising=False
    )

    response = client.post(
        ROUTE,
        data={
            "prompt": (
                "Review this uncertain security migration plan with budget and timeline "
                "risk, then decide the safest next step."
            )
        },
        headers={auth.CSRF_HEADER_NAME: csrf_token},
    )

    assert response.status_code == 200
    html = response.text
    assert "plain same-provider answer" in html
    # Three deterministic fake calls (plain tot pass + two expert passes) prove the
    # preview ran end-to-end with no live provider/network dependency.
    assert len(fake.requests) == 3
    # Provider secrets must never reach the rendered page.
    assert raw_secret not in html
    assert "provider-hidden" not in html


def test_preview_post_without_csrf_is_rejected(client: TestClient) -> None:
    _login(client)

    response = client.post(ROUTE, data={"prompt": "hello"}, follow_redirects=False)

    assert response.status_code == 403


def test_dashboard_disabled_when_password_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(auth.PASSWORD_ENV_VAR, raising=False)
    monkeypatch.setenv(auth.SECRET_ENV_VAR, "unit-test-secret")
    assert _dashboard_enabled() is False


def test_dashboard_disabled_when_password_is_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(auth.PASSWORD_ENV_VAR, auth.DEFAULT_DASHBOARD_PASSWORD)
    monkeypatch.setenv(auth.SECRET_ENV_VAR, "unit-test-secret")
    assert _dashboard_enabled() is False


def test_dashboard_disabled_when_secret_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(auth.PASSWORD_ENV_VAR, "a-strong-operator-secret")
    monkeypatch.delenv(auth.SECRET_ENV_VAR, raising=False)
    assert _dashboard_enabled() is False


def test_dashboard_disabled_when_secret_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(auth.PASSWORD_ENV_VAR, "a-strong-operator-secret")
    monkeypatch.setenv(auth.SECRET_ENV_VAR, "")
    assert _dashboard_enabled() is False


def test_dashboard_enabled_when_password_non_default_and_secret_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(auth.PASSWORD_ENV_VAR, "a-strong-operator-secret")
    monkeypatch.setenv(auth.SECRET_ENV_VAR, "unit-test-secret")
    assert _dashboard_enabled() is True


def test_mount_dashboard_adds_protected_routes() -> None:
    fresh = FastAPI()
    _mount_dashboard(fresh)

    paths = {getattr(route, "path", None) for route in fresh.routes}
    assert ROUTE in paths
    assert "/login" in paths

    fresh_client = TestClient(fresh, base_url="https://testserver")
    try:
        response = fresh_client.get(ROUTE, follow_redirects=False)
    finally:
        fresh_client.close()
    assert response.status_code == 303
    assert response.headers["location"] == "/login"
