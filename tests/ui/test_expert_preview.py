from __future__ import annotations

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
    monkeypatch.setenv("ALPHA_LIVE_PREVIEW_ENABLED", "true")
    monkeypatch.setenv("ALPHA_LIVE_PREVIEW_MAX_REQUESTS", "20")
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


def _login(client: TestClient) -> str:
    response = client.post("/login", data={"password": "testing-secret"}, follow_redirects=False)
    assert response.status_code == 303
    csrf_token = client.cookies.get(auth.CSRF_COOKIE_NAME)
    assert csrf_token
    return csrf_token


def _assert_successful_preview_response(html: str, prompt: str) -> None:
    assert "plain same-provider answer" in html
    assert "Alpha Solver expert preview" in html
    assert f'<textarea id="prompt" name="prompt" required>{prompt}</textarea>' in html


def _assert_no_sensitive_preview_leak(html: str, *secrets: str) -> None:
    for secret in secrets:
        assert secret not in html
    assert "provider-hidden" not in html
    assert "raw_metadata" not in html
    assert "Authorization" not in html
    assert "Bearer" not in html
    assert "OPENAI_API_KEY" not in html
    assert "sk-" not in html
    assert "raw request" not in html.lower()
    assert "raw response" not in html.lower()
    assert "raw provider" not in html.lower()


def _install_successful_fake(client: TestClient) -> FakeProviderClient:
    fake = FakeProviderClient(
        [
            _provider_result("plain same-provider answer"),
            _provider_result(
                '{"considerations":["Check timeline risk"],'
                '"assumptions":["Budget is constrained"],"confidence":0.35}'
            ),
            _provider_result("draft expert answer that clarify mode replaces"),
        ]
    )
    client.app.state.provider_client_factory = lambda _model_set: fake
    return fake


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


def test_openai_preview_submit_blocks_when_live_preview_flag_absent(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    csrf_token = _login(client)
    prompt = "Keep this blocked prompt visible."
    monkeypatch.delenv("ALPHA_LIVE_PREVIEW_ENABLED", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-guard-test-should-not-render")

    def fail_factory(_model_set: object) -> FakeProviderClient:
        raise AssertionError("provider factory must not be invoked when guard blocks")

    client.app.state.provider_client_factory = fail_factory

    response = client.post(
        "/dashboard/expert-preview",
        data={"prompt": prompt},
        headers={
            auth.CSRF_HEADER_NAME: csrf_token,
            "Authorization": "Bearer should-not-render",
        },
    )

    assert response.status_code == 403
    html = response.text
    assert "Live OpenAI preview testing is disabled." in html
    assert f'<textarea id="prompt" name="prompt" required>{prompt}</textarea>' in html
    _assert_no_sensitive_preview_leak(
        html,
        "sk-guard-test-should-not-render",
        "should-not-render",
    )


def test_openai_preview_submit_blocks_when_live_preview_flag_false(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    csrf_token = _login(client)
    prompt = "Keep this false-flag prompt visible."
    monkeypatch.setenv("ALPHA_LIVE_PREVIEW_ENABLED", "false")

    def fail_factory(_model_set: object) -> FakeProviderClient:
        raise AssertionError("provider factory must not be invoked when guard blocks")

    client.app.state.provider_client_factory = fail_factory

    response = client.post(
        "/dashboard/expert-preview",
        data={"prompt": prompt},
        headers={auth.CSRF_HEADER_NAME: csrf_token},
    )

    assert response.status_code == 403
    html = response.text
    assert "Live OpenAI preview testing is disabled." in html
    assert f'<textarea id="prompt" name="prompt" required>{prompt}</textarea>' in html
    assert "Plain provider output" in html
    assert "Alpha Solver expert preview" in html


def test_openai_preview_cap_blocks_after_configured_limit(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    csrf_token = _login(client)
    monkeypatch.setenv("ALPHA_LIVE_PREVIEW_ENABLED", "true")
    monkeypatch.setenv("ALPHA_LIVE_PREVIEW_MAX_REQUESTS", "1")
    fake = _install_successful_fake(client)
    first_prompt = "Define alpha in one sentence."
    second_prompt = "This second live preview should be blocked."

    first = client.post(
        "/dashboard/expert-preview",
        data={"prompt": first_prompt},
        headers={auth.CSRF_HEADER_NAME: csrf_token},
    )
    second = client.post(
        "/dashboard/expert-preview",
        data={"prompt": second_prompt},
        headers={auth.CSRF_HEADER_NAME: csrf_token},
    )

    assert first.status_code == 200
    _assert_successful_preview_response(first.text, first_prompt)
    assert len(fake.requests) == 2
    assert second.status_code == 403
    html = second.text
    assert "Live OpenAI preview request cap reached" in html
    assert f'<textarea id="prompt" name="prompt" required>{second_prompt}</textarea>' in html
    assert len(fake.requests) == 2
    _assert_no_sensitive_preview_leak(html)


def test_preview_submission_handles_unstructured_expert_preview_coherently(
    client: TestClient,
) -> None:
    csrf_token = _login(client)
    raw_secret = "sk-preview-should-not-render"
    raw_answer = "This long expert answer should be hidden when confidence is unavailable."
    fake = FakeProviderClient(
        [
            _provider_result("plain same-provider answer", raw_secret=raw_secret),
            _provider_result(
                "Here is a prose review with risks and assumptions, but no compact JSON, "
                "no section headings, and no numeric confidence value.",
                raw_secret=raw_secret,
            ),
            _provider_result(raw_answer, raw_secret=raw_secret),
        ]
    )
    client.app.state.provider_client_factory = lambda _model_set: fake

    response = client.post(
        "/dashboard/expert-preview",
        data={
            "prompt": (
                "Plan a security review and architecture migration where goals, timeline, "
                "owners, risk tolerance, and compliance constraints are uncertain."
            )
        },
        headers={auth.CSRF_HEADER_NAME: csrf_token},
    )

    assert response.status_code == 200
    html = response.text
    assert "plain same-provider answer" in html
    assert "I need a few details before I can answer this well." in html
    assert "clarify" in html
    assert "unavailable" in html
    assert "What is the main outcome you want from this request?" in html
    assert "preview_parse_status" in html
    assert "unstructured" in html
    assert raw_answer not in html

    assert len(fake.requests) == 3
    assert fake.requests[0].metadata["route"] == "tot"
    assert fake.requests[1].metadata["route"] == "expert"
    assert fake.requests[2].metadata["route"] == "expert"

    assert raw_secret not in html
    assert "provider-hidden" not in html
    assert "raw_metadata" not in html
    assert "Authorization" not in html
    assert "Bearer" not in html
    assert "raw request" not in html.lower()
    assert "raw response" not in html.lower()


def test_browser_like_multipart_submission_extracts_prompt_and_preserves_it(
    client: TestClient,
) -> None:
    csrf_token = _login(client)
    fake = _install_successful_fake(client)
    prompt = "Define alpha in one sentence."

    response = client.post(
        "/dashboard/expert-preview",
        files={"prompt": (None, prompt)},
        headers={auth.CSRF_HEADER_NAME: csrf_token},
    )

    assert response.status_code == 200
    _assert_successful_preview_response(response.text, prompt)
    assert len(fake.requests) == 2


def test_urlencoded_submission_extracts_prompt_and_preserves_it(client: TestClient) -> None:
    csrf_token = _login(client)
    fake = _install_successful_fake(client)
    prompt = "Summarize alpha briefly."

    response = client.post(
        "/dashboard/expert-preview",
        data={"prompt": prompt},
        headers={auth.CSRF_HEADER_NAME: csrf_token},
    )

    assert response.status_code == 200
    _assert_successful_preview_response(response.text, prompt)
    assert len(fake.requests) == 2


def test_local_provider_expert_preview_ignores_route_context(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    csrf_token = _login(client)
    monkeypatch.setenv("MODEL_PROVIDER", "local")
    client.app.state.provider_client_factory = lambda _model_set: (_ for _ in ()).throw(
        AssertionError("provider should not be used in local mode")
    )
    calls: list[str] = []

    def fake_solver(query: str) -> dict[str, str]:
        calls.append(query)
        label = "plain" if len(calls) == 1 else "expert"
        return {"final_answer": f"local {label}: {query}"}

    monkeypatch.setattr("service.app._tree_of_thought", fake_solver)
    prompt = "Define alpha in one sentence."

    response = client.post(
        "/dashboard/expert-preview",
        data={"prompt": prompt},
        headers={auth.CSRF_HEADER_NAME: csrf_token},
    )

    assert response.status_code == 200
    html = response.text
    assert "local plain: Define alpha in one sentence." in html
    assert "local expert: Define alpha in one sentence." in html
    assert f'<textarea id="prompt" name="prompt" required>{prompt}</textarea>' in html
    assert calls == [prompt, prompt]


def test_json_submission_still_extracts_prompt(client: TestClient) -> None:
    csrf_token = _login(client)
    fake = _install_successful_fake(client)
    prompt = "Explain alpha as JSON-compatible input."

    response = client.post(
        "/dashboard/expert-preview",
        json={"prompt": prompt},
        headers={auth.CSRF_HEADER_NAME: csrf_token},
    )

    assert response.status_code == 200
    _assert_successful_preview_response(response.text, prompt)
    assert len(fake.requests) == 2


def test_empty_prompt_returns_user_facing_error(client: TestClient) -> None:
    csrf_token = _login(client)

    response = client.post(
        "/dashboard/expert-preview",
        data={"prompt": "   "},
        headers={auth.CSRF_HEADER_NAME: csrf_token},
    )

    assert response.status_code == 400
    assert "Prompt is required." in response.text
    assert "Plain provider output" in response.text
    assert "Alpha Solver expert preview" in response.text


def test_preview_failure_preserves_prompt_in_textarea(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    csrf_token = _login(client)
    prompt = "Keep this prompt visible after a provider failure."

    async def fail_preview(*args: object, **kwargs: object) -> dict[str, object]:
        raise RuntimeError("forced preview failure")

    monkeypatch.setattr(expert_preview, "_solve_preview", fail_preview)

    response = client.post(
        "/dashboard/expert-preview",
        data={"prompt": prompt},
        headers={auth.CSRF_HEADER_NAME: csrf_token},
    )

    assert response.status_code == 502
    assert "Preview request failed." in response.text
    assert f'<textarea id="prompt" name="prompt" required>{prompt}</textarea>' in response.text


def test_second_browser_style_submit_after_error_keeps_csrf_behavior(client: TestClient) -> None:
    csrf_token = _login(client)
    error_response = client.post(
        "/dashboard/expert-preview",
        files={"prompt": (None, "")},
        headers={auth.CSRF_HEADER_NAME: csrf_token},
    )
    assert error_response.status_code == 400
    assert "Prompt is required." in error_response.text
    assert "document.write" not in error_response.text
    assert "initExpertPreviewForm" in error_response.text
    assert "X-Alpha-CSRF" in error_response.text

    fake = _install_successful_fake(client)
    prompt = "Define alpha in one sentence."
    response = client.post(
        "/dashboard/expert-preview",
        files={"prompt": (None, prompt)},
        headers={auth.CSRF_HEADER_NAME: csrf_token},
    )

    assert response.status_code == 200
    _assert_successful_preview_response(response.text, prompt)
    assert len(fake.requests) == 2


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
