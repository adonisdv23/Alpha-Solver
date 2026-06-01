from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from alpha.providers import FakeProviderClient, ProviderCost, ProviderResult, ProviderUsage  # noqa: E402
from alpha.webapp.routes import auth, expert_preview  # noqa: E402


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
    auth.reset_state()

    app = FastAPI()
    auth.install_dashboard_security(app)
    app.include_router(auth.router)
    app.include_router(expert_preview.router)

    test_client = TestClient(app, base_url="https://testserver")
    try:
        yield test_client
    finally:
        test_client.close()
        os.environ.pop("MODEL_PROVIDER", None)


def _login(client: TestClient) -> str:
    response = client.post("/login", data={"password": "testing-secret"}, follow_redirects=False)
    assert response.status_code == 303
    csrf_token = client.cookies.get(auth.CSRF_COOKIE_NAME)
    assert csrf_token
    return csrf_token


def test_expert_preview_requires_authentication(client: TestClient) -> None:
    response = client.get("/dashboard/expert-preview", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_authenticated_user_can_access_preview_page(client: TestClient) -> None:
    _login(client)

    response = client.get("/dashboard/expert-preview")

    assert response.status_code == 200
    assert "Supervised preview only" in response.text
    assert expert_preview.DISCLAIMER in response.text
    assert "Plain provider output" in response.text
    assert "Alpha Solver expert preview" in response.text


def test_preview_submission_renders_plain_and_expert_outputs(client: TestClient) -> None:
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
            _provider_result("draft expert answer that clarify mode replaces", raw_secret=raw_secret),
        ]
    )
    client.app.state.provider_client_factory = lambda _model_set: fake

    response = client.post(
        "/dashboard/expert-preview",
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
    assert "I need a few details before I can answer this well." in html
    assert "Mode" in html
    assert "clarify" in html
    assert "Confidence" in html
    assert "0.35" in html
    assert "Complexity" in html
    assert "complex" in html
    assert "Call count" in html
    assert "Check timeline risk" in html
    assert "Budget is constrained" in html
    assert "Clarifying questions" in html
    assert "What is the main outcome you want from this request?" in html
    assert "Details" in html

    assert len(fake.requests) == 3
    assert fake.requests[0].metadata["route"] == "tot"
    assert fake.requests[1].metadata["route"] == "expert"
    assert fake.requests[2].metadata["route"] == "expert"
    assert len({request.model for request in fake.requests}) == 1

    assert raw_secret not in html
    assert "provider-hidden" not in html
    assert "raw_metadata" not in html
    assert "Authorization" not in html
    assert "Bearer" not in html
    assert "raw request" not in html.lower()
    assert "raw response" not in html.lower()


def test_preview_copy_keeps_claim_boundaries(client: TestClient) -> None:
    _login(client)

    response = client.get("/dashboard/expert-preview")

    assert response.status_code == 200
    body = response.text.lower()
    assert "better answer" not in body
    assert "benchmarked superiority" not in body
    assert "validated mvp" not in body
    assert "production-ready" not in body
    assert "runtime-ready" not in body
    assert "provider reasoning orchestration" not in body
    assert "autonomous reasoning system" not in body
    assert "live eval success" not in body
