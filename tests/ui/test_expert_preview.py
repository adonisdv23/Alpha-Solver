from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import anyio
import pytest
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from alpha.providers import (
    FakeProviderClient,
    emit_provider_accounting,
    ProviderCost,
    ProviderResult,
    ProviderUsage,
)  # noqa: E402
from alpha.webapp.routes import auth, expert_preview  # noqa: E402


def _provider_result(
    text: str,
    *,
    raw_secret: str | None = None,
    usage: ProviderUsage | None = None,
    cost: ProviderCost | None = None,
    latency_ms: int = 1,
) -> ProviderResult:
    return ProviderResult(
        provider="openai",
        model="gpt-test",
        text=text,
        finish_reason="stop",
        usage=usage or ProviderUsage(input_tokens=1, output_tokens=1, total_tokens=2),
        cost=cost or ProviderCost(estimated_usd=0.0, source="price_hint"),
        latency_ms=latency_ms,
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


def _assert_metrics_panel_rendered(html: str) -> None:
    assert "Request metrics" in html
    assert "Total preview latency" in html
    assert "Provider" in html
    assert "Mode" in html
    assert "Calls" in html
    assert "Input tokens" in html
    assert "Output tokens" in html
    assert "Total tokens" in html
    assert "Estimated API cost" in html
    assert "Cost source" in html
    assert "Provider latency" in html


def _assert_loading_state_script(html: str) -> None:
    assert "let previewInFlight = false;" in html
    assert "if (previewInFlight)" in html
    assert "submitButton.disabled = true;" in html
    assert "Running preview..." in html
    assert 'form.setAttribute("aria-busy", "true");' in html
    assert '"X-Alpha-CSRF": cookieValue("alpha_dashboard_csrf")' in html
    assert "document.body.innerHTML = nextDocument.body.innerHTML;" in html
    assert "initExpertPreviewForm();" in html


def _assert_long_response_layout(html: str) -> None:
    assert '.panes { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); align-items: start;' in html
    assert '.pane { min-width: 0; }' in html
    assert '.answer, pre { white-space: pre-wrap; overflow-wrap: anywhere; word-break: break-word; }' in html
    assert '.answer { display: block; margin: 0 0 1rem; max-height: none; overflow: visible;' in html
    assert 'class="answer response-text" aria-label="Primary response"' in html


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


def _assert_no_shared_accounting_sink(app: FastAPI) -> None:
    assert not callable(getattr(app.state, "provider_accounting_sink", None))


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
    _assert_loading_state_script(response.text)


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
            _provider_result(
                "draft expert answer that clarify mode replaces", raw_secret=raw_secret
            ),
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
    _assert_metrics_panel_rendered(html)
    assert "gpt-test" in html
    assert "openai" in html
    assert "expert" in html
    assert "$0.000000 estimated" in html
    assert "price_hint" in html

    assert len(fake.requests) == 3
    assert fake.requests[0].metadata["route"] == "tot"
    assert fake.requests[1].metadata["route"] == "expert"
    assert fake.requests[2].metadata["route"] == "expert"
    assert len({request.model for request in fake.requests}) == 1
    _assert_no_shared_accounting_sink(client.app)

    assert raw_secret not in html
    assert "provider-hidden" not in html
    assert "raw_metadata" not in html
    assert "Authorization" not in html
    assert "Bearer" not in html
    assert "raw request" not in html.lower()
    assert "raw response" not in html.lower()


def test_preview_submission_preserves_requested_operator_plan_structure(
    client: TestClient,
) -> None:
    csrf_token = _login(client)
    prompt = (
        "Create a two-hour operator test plan for /dashboard/expert-preview "
        "that separates setup, prompt runs, evidence capture, and rollback."
    )
    expert_answer = (
        "# Two-hour operator test plan\n\n"
        "## Setup (0:00-0:20)\n"
        "- Confirm local-provider baseline and dashboard login.\n\n"
        "## Prompt runs (0:20-1:15)\n"
        "- Run the controlled prompts and compare panes.\n\n"
        "## Evidence capture (1:15-1:45)\n"
        "- Record sanitized summaries only.\n\n"
        "## Rollback (1:45-2:00)\n"
        "- Return MODEL_PROVIDER=local and document status.\n\n"
        "Assumptions: supervised operator test only; no MVP validation claim."
    )
    fake = FakeProviderClient(
        [
            _provider_result("plain same-provider answer"),
            _provider_result(
                '{"considerations":["Preserve the requested plan first"],'
                '"assumptions":["Operator preview only"],"confidence":0.82}'
            ),
            _provider_result(expert_answer),
        ]
    )
    client.app.state.provider_client_factory = lambda _model_set: fake

    response = client.post(
        "/dashboard/expert-preview",
        data={"prompt": prompt},
        headers={auth.CSRF_HEADER_NAME: csrf_token},
    )

    assert response.status_code == 200
    html = response.text
    assert "Two-hour operator test plan" in html
    for section in ("Setup", "Prompt runs", "Evidence capture", "Rollback"):
        assert section in html
    for time_box in ("0:00-0:20", "0:20-1:15", "1:15-1:45", "1:45-2:00"):
        assert time_box in html
    assert "Preserve the requested plan first" in html
    assert "Operator preview only" in html
    assert len(fake.requests) == 3
    answer_prompt = fake.requests[2].prompt
    assert "Preserve the user's requested output format first" in answer_prompt
    assert "do not let them replace the requested deliverable" in answer_prompt


def test_preview_submission_answerable_operator_plan_is_not_clarify_only(
    client: TestClient,
) -> None:
    csrf_token = _login(client)
    prompt = (
        "Create a two-hour operator test plan for /dashboard/expert-preview "
        "that separates setup, prompt runs, evidence capture, and rollback."
    )
    expert_answer = (
        "# Two-hour operator test plan\n\n"
        "Assumptions: supervised preview only; no MVP validation claim.\n\n"
        "## Setup\n"
        "- Confirm dashboard auth and local-provider rollback path.\n\n"
        "## Prompt runs\n"
        "- Execute controlled prompts and compare primary answers.\n\n"
        "## Evidence capture\n"
        "- Save sanitized observations, screenshots, and request IDs.\n\n"
        "## Rollback\n"
        "- Restore local mode and record status."
    )
    fake = FakeProviderClient(
        [
            _provider_result("plain same-provider answer"),
            _provider_result(
                '{"considerations":["The prompt already names the deliverable and route"],'
                '"assumptions":["Operator has approved preview access"],"confidence":0.50}'
            ),
            _provider_result(expert_answer),
        ]
    )
    client.app.state.provider_client_factory = lambda _model_set: fake

    response = client.post(
        "/dashboard/expert-preview",
        data={"prompt": prompt},
        headers={auth.CSRF_HEADER_NAME: csrf_token},
    )

    assert response.status_code == 200
    html = response.text
    assert "I need a few details before I can answer this well." not in html
    assert "Two-hour operator test plan" in html
    for section in ("Setup", "Prompt runs", "Evidence capture", "Rollback"):
        assert section in html
    assert "Assumptions" in html
    assert "The prompt already names the deliverable and route" in html
    assert "Operator has approved preview access" in html
    assert "Mode" in html
    assert "answer_with_assumptions" in html
    assert len(fake.requests) == 3


def test_preview_submission_renders_operator_plan_when_expert_step_two_is_empty(
    client: TestClient,
) -> None:
    csrf_token = _login(client)
    prompt = (
        "Create a two-hour operator test plan for /dashboard/expert-preview "
        "that separates setup, prompt runs, evidence capture, and rollback."
    )
    fake = FakeProviderClient(
        [
            _provider_result("plain same-provider answer"),
            _provider_result(
                '{"considerations":["Keep the requested deliverable primary"],'
                '"assumptions":["Run is a supervised operator preview"],"confidence":0.50}'
            ),
            _provider_result(""),
        ]
    )
    client.app.state.provider_client_factory = lambda _model_set: fake

    response = client.post(
        "/dashboard/expert-preview",
        data={"prompt": prompt},
        headers={auth.CSRF_HEADER_NAME: csrf_token},
    )

    assert response.status_code == 200
    html = response.text
    assert "answer_with_assumptions" in html
    assert "Two-hour operator test plan" in html
    for section in ("Setup", "Prompt runs", "Evidence capture", "Rollback"):
        assert section in html
    assert "Keep the requested deliverable primary" in html
    assert "Run is a supervised operator preview" in html
    assert "I need a few details before I can answer this well." not in html
    assert len(fake.requests) == 3


def test_expert_preview_answer_uses_final_answer_when_answer_alias_is_blank() -> None:
    html = expert_preview._render_expert_payload(
        {
            "answer": "",
            "final_answer": "Two-hour operator test plan fallback",
            "mode": "answer_with_assumptions",
            "considerations": ["Keep deliverable primary"],
            "assumptions": ["Supervised preview only"],
            "meta": {"route": "expert", "complexity": "complex", "call_count": 2},
        }
    )

    assert "Two-hour operator test plan fallback" in html
    assert "Keep deliverable primary" in html
    assert "Supervised preview only" in html

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


def test_metrics_panel_renders_usage_cost_and_safe_unknowns(client: TestClient) -> None:
    csrf_token = _login(client)
    fake = FakeProviderClient(
        [
            _provider_result(
                "plain same-provider answer",
                usage=ProviderUsage(input_tokens=11, output_tokens=7, total_tokens=18),
                cost=ProviderCost(estimated_usd=0.000123, source="price_hint"),
                latency_ms=45,
            ),
            _provider_result(
                '{"considerations":["Check timeline risk"],"assumptions":[],"confidence":0.8}',
                usage=ProviderUsage(input_tokens=13, output_tokens=5, total_tokens=18),
                cost=ProviderCost(estimated_usd=0.0002, source="price_hint"),
                latency_ms=55,
            ),
            _provider_result(
                "expert answer",
                usage=ProviderUsage(input_tokens=17, output_tokens=19, total_tokens=36),
                cost=ProviderCost(estimated_usd=0.0003, source="price_hint"),
                latency_ms=65,
            ),
        ]
    )
    client.app.state.provider_client_factory = lambda _model_set: fake

    response = client.post(
        "/dashboard/expert-preview",
        data={"prompt": "Plan a security migration with budget, timeline, compliance, owner, rollout, and risk tradeoffs across multiple teams."},
        headers={auth.CSRF_HEADER_NAME: csrf_token},
    )

    assert response.status_code == 200
    html = response.text
    _assert_metrics_panel_rendered(html)
    assert "11" in html
    assert "7" in html
    assert "18" in html
    assert "30" in html
    assert "24" in html
    assert "54" in html
    assert "$0.000123 estimated" in html
    assert "$0.000500 estimated" in html


def test_preview_metrics_do_not_leave_shared_app_state_accounting_sink(
    client: TestClient,
) -> None:
    csrf_token = _login(client)
    fake = _install_successful_fake(client)

    response = client.post(
        "/dashboard/expert-preview",
        data={"prompt": "Review this migration plan with budget and timeline risk."},
        headers={auth.CSRF_HEADER_NAME: csrf_token},
    )

    assert response.status_code == 200
    _assert_metrics_panel_rendered(response.text)
    assert len(fake.requests) >= 2
    _assert_no_shared_accounting_sink(client.app)


def test_overlapping_preview_solves_keep_accounting_records_request_scoped(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_solve(req: object, request: object) -> JSONResponse:
        query = getattr(req, "query")
        context = getattr(req, "context") or {}
        if query == "alpha":
            await anyio.sleep(0.01)
            emit_provider_accounting(
                {
                    "event": "provider.cost.recorded",
                    "provider": "openai",
                    "model": "gpt-alpha",
                    "route": context.get("route", "tot"),
                    "input_tokens": 101,
                    "output_tokens": 11,
                    "total_tokens": 112,
                    "estimated_cost_usd": 0.00101,
                    "cost_source": "price_hint",
                }
            )
            await anyio.sleep(0.02)
        else:
            emit_provider_accounting(
                {
                    "event": "provider.cost.recorded",
                    "provider": "openai",
                    "model": "gpt-beta",
                    "route": context.get("route", "tot"),
                    "input_tokens": 202,
                    "output_tokens": 22,
                    "total_tokens": 224,
                    "estimated_cost_usd": 0.00202,
                    "cost_source": "price_hint",
                }
            )
            await anyio.sleep(0.02)
        return JSONResponse(
            {
                "final_answer": f"answer {query}",
                "meta": {"route": context.get("route", "tot")},
            }
        )

    monkeypatch.setattr("service.app.solve", fake_solve)

    async def run_pair() -> tuple[dict[str, object], dict[str, object], SimpleNamespace]:
        app = SimpleNamespace(state=SimpleNamespace())
        request = SimpleNamespace(app=app)
        results: dict[str, dict[str, object]] = {}

        async def run_one(prompt: str) -> None:
            results[prompt] = await expert_preview._solve_preview(request, prompt, expert=False)

        async with anyio.create_task_group() as task_group:
            task_group.start_soon(run_one, "alpha")
            task_group.start_soon(run_one, "beta")
        return results["alpha"], results["beta"], app

    alpha_result, beta_result, app = anyio.run(run_pair)

    alpha_meta = alpha_result["meta"]
    beta_meta = beta_result["meta"]
    assert alpha_meta["model"] == "gpt-alpha"
    assert alpha_meta["usage"]["input_tokens"] == 101
    assert alpha_meta["cost"]["estimated_usd"] == pytest.approx(0.00101)
    assert beta_meta["model"] == "gpt-beta"
    assert beta_meta["usage"]["input_tokens"] == 202
    assert beta_meta["cost"]["estimated_usd"] == pytest.approx(0.00202)
    assert not hasattr(app.state, "provider_accounting_sink")


def test_metrics_panel_uses_unknowns_without_usage_or_cost_metadata(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    csrf_token = _login(client)

    async def fake_solve_preview(*args: object, expert: bool) -> dict[str, object]:
        if expert:
            return {
                "final_answer": "expert answer",
                "confidence": 0.4,
                "considerations": [],
                "assumptions": [],
                "mode": "clarify",
                "meta": {"route": "expert"},
            }
        return {"final_answer": "plain answer", "meta": {"route": "tot"}}

    monkeypatch.setattr(expert_preview, "_solve_preview", fake_solve_preview)

    response = client.post(
        "/dashboard/expert-preview",
        data={"prompt": "Render unknown metrics safely."},
        headers={auth.CSRF_HEADER_NAME: csrf_token},
    )

    assert response.status_code == 200
    html = response.text
    _assert_metrics_panel_rendered(html)
    assert "unknown" in html
    assert "not estimated" in html


def test_metrics_panel_does_not_render_sensitive_request_or_provider_values(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    csrf_token = _login(client)
    raw_secret = "sk-metrics-secret-should-not-render"
    account_id = "acct_provider_should_not_render"
    raw_payload = "raw-provider-payload-should-not-render"
    raw_body = "raw-request-body-should-not-render"
    session_value = client.cookies.get(auth.SESSION_COOKIE_NAME)
    fake = FakeProviderClient(
        [
            _provider_result("plain same-provider answer", raw_secret=raw_secret),
            _provider_result(
                '{"considerations":["Check timeline risk"],"assumptions":[],"confidence":0.8}',
                raw_secret=raw_secret,
            ),
            _provider_result("expert answer", raw_secret=raw_secret),
        ]
    )
    client.app.state.provider_client_factory = lambda _model_set: fake
    monkeypatch.setenv("OPENAI_API_KEY", raw_secret)

    response = client.post(
        "/dashboard/expert-preview",
        data={"prompt": "Confirm metrics redaction boundaries."},
        headers={
            auth.CSRF_HEADER_NAME: csrf_token,
            "Authorization": "Bearer metrics-bearer-should-not-render",
            "X-Raw-Request": raw_body,
            "X-Provider-Account": account_id,
            "X-Raw-Provider-Payload": raw_payload,
        },
    )

    assert response.status_code == 200
    html = response.text
    _assert_metrics_panel_rendered(html)
    _assert_no_sensitive_preview_leak(
        html,
        raw_secret,
        account_id,
        raw_payload,
        raw_body,
        csrf_token,
        session_value or "",
        "metrics-bearer-should-not-render",
    )



def test_long_plain_and_expert_responses_use_expanding_wrapping_answer_boxes(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    csrf_token = _login(client)
    long_plain = "Plain provider output " + ("wraps cleanly with a very long segment " * 80)
    long_expert = "Alpha Solver expert preview output " + ("expands vertically for operator review " * 80)

    async def fake_solve_preview(*args: object, expert: bool) -> dict[str, object]:
        if expert:
            return {
                "final_answer": long_expert,
                "confidence": 0.62,
                "considerations": ["Review long output layout"],
                "meta": {"route": "expert", "call_count": 1},
            }
        return {"final_answer": long_plain, "meta": {"route": "tot", "call_count": 1}}

    monkeypatch.setattr(expert_preview, "_solve_preview", fake_solve_preview)

    response = client.post(
        "/dashboard/expert-preview",
        data={"prompt": "Render long responses without clipping."},
        headers={auth.CSRF_HEADER_NAME: csrf_token},
    )

    assert response.status_code == 200
    html = response.text
    assert long_plain in html
    assert long_expert in html
    assert html.count('class="answer response-text" aria-label="Primary response"') == 2
    _assert_long_response_layout(html)


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
    _assert_loading_state_script(error_response.text)

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
