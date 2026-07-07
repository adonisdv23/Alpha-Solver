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
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from alpha.webapp import operator_console_artifacts as artifacts  # noqa: E402
from alpha.webapp.routes import auth, operator_console  # noqa: E402
from alpha.eval import operator_run_capture as capture_lib  # noqa: E402
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


# ---------------------------------------------------------------------------
# Local artifact status (AOC-B002-LOCAL-ARTIFACT-STATUS-001)
# ---------------------------------------------------------------------------
# Recognizable raw content that must never surface in HTML or JSON.
RAW_PROMPT = "RAW-PROMPT-must-not-render-zzz"
RAW_BASELINE = "RAW-BASELINE-must-not-render-zzz"
RAW_ROUTED = "RAW-ROUTED-must-not-render-zzz"
RAW_ROUTE_META = "RAW-ROUTE-META-must-not-render-zzz"


def _valid_capture() -> dict:
    """A structurally valid, export-ready capture with recognizable raw fields."""

    packet = {
        "packet_id": "ORC-TEST-001",
        "cases": [
            {"task_id": "t1", "prompt": RAW_PROMPT},
            {"task_id": "t2", "prompt": RAW_PROMPT},
        ],
    }
    capture = capture_lib.scaffold_capture(packet)
    capture["cases"][0].update(
        {
            "validation_status": "captured",
            "baseline_output": RAW_BASELINE,
            "routed_output": RAW_ROUTED,
            "route_metadata": {"route": RAW_ROUTE_META},
        }
    )
    capture["cases"][1].update(
        {
            "validation_status": "excluded",
            "baseline_output": "",
            "routed_output": "",
            "route_metadata": {},
            "exclusion_reason": "low headroom",
        }
    )
    return capture


def _write(tmp_path: Path, name: str, obj) -> None:
    (tmp_path / name).write_text(json.dumps(obj), encoding="utf-8")


def _use_root(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(artifacts, "resolve_artifact_root", lambda: tmp_path)


def test_no_local_artifacts_status_and_render(client: TestClient) -> None:
    _login(client)
    payload = client.get(STATUS_ROUTE).json()
    local = payload["local_artifacts"]

    assert local["detected"] is False
    assert local["no_artifacts_message"] == artifacts.NO_ARTIFACTS_TEXT
    for section in ("capture", "evidence_packet", "anchor_preflight", "lift_preflight"):
        assert local[section]["state"] == "missing"

    html_text = client.get(PAGE_ROUTE).text
    assert artifacts.NO_ARTIFACTS_TEXT in html_text


def test_artifact_boundary_texts_present(client: TestClient) -> None:
    _login(client)
    html_text = client.get(PAGE_ROUTE).text
    payload_text = json.dumps(client.get(STATUS_ROUTE).json())
    for text in artifacts.BOUNDARY_TEXTS:
        assert text in html_text
        assert text in payload_text


def test_valid_capture_summary(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _write(tmp_path, "capture.json", _valid_capture())
    _use_root(monkeypatch, tmp_path)
    _login(client)

    payload = client.get(STATUS_ROUTE).json()
    cap = payload["local_artifacts"]["capture"]
    assert cap["state"] in {"structurally_valid", "export_ready"}
    assert cap["schema_version"] == capture_lib.CAPTURE_SCHEMA_VERSION
    assert cap["packet_id"] == "ORC-TEST-001"
    assert cap["counts"] == {
        "total": 2,
        "captured": 1,
        "excluded": 1,
        "pending": 0,
    }
    assert cap["route_metadata_present_count"] == 1

    html_text = client.get(PAGE_ROUTE).text
    body = json.dumps(payload)
    for raw in (RAW_PROMPT, RAW_BASELINE, RAW_ROUTED, RAW_ROUTE_META):
        assert raw not in html_text
        assert raw not in body


def test_invalid_json_capture_fails_safe(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    (tmp_path / "capture.json").write_text("{ not valid json", encoding="utf-8")
    _use_root(monkeypatch, tmp_path)
    _login(client)

    response = client.get(STATUS_ROUTE)
    assert response.status_code == 200
    assert response.json()["local_artifacts"]["capture"]["state"] == "invalid_json"
    assert client.get(PAGE_ROUTE).status_code == 200


def test_invalid_structure_capture_fails_safe(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _write(tmp_path, "capture.json", {"schema_version": "wrong", "cases": "nope"})
    _use_root(monkeypatch, tmp_path)
    _login(client)

    response = client.get(STATUS_ROUTE)
    assert response.status_code == 200
    assert (
        response.json()["local_artifacts"]["capture"]["state"] == "invalid_structure"
    )
    assert client.get(PAGE_ROUTE).status_code == 200


def test_valid_evidence_packet_digest_valid(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    packet = capture_lib.build_evidence_packet(_valid_capture())
    _write(tmp_path, "evidence_packet.json", packet)
    _use_root(monkeypatch, tmp_path)
    _login(client)

    payload = client.get(STATUS_ROUTE).json()
    pkt = payload["local_artifacts"]["evidence_packet"]
    assert pkt["state"] == "digest_valid"
    assert pkt["packet_id"] == "ORC-TEST-001"
    assert pkt["schema_version"] == capture_lib.PACKET_SCHEMA_VERSION
    assert pkt["content_digest"].startswith("sha256:")
    assert pkt["counts"]["total"] == 2

    # digest (a hash, not raw content) is shown; raw case content is not.
    html_text = client.get(PAGE_ROUTE).text
    assert pkt["content_digest"] in html_text
    for raw in (RAW_PROMPT, RAW_BASELINE, RAW_ROUTED, RAW_ROUTE_META):
        assert raw not in html_text
        assert raw not in json.dumps(payload)


def test_bad_evidence_packet_digest_fails_safe(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    packet = capture_lib.build_evidence_packet(_valid_capture())
    packet["packet_id"] = "tampered-after-digest"  # digest no longer matches body
    _write(tmp_path, "evidence_packet.json", packet)
    _use_root(monkeypatch, tmp_path)
    _login(client)

    response = client.get(STATUS_ROUTE)
    assert response.status_code == 200
    assert (
        response.json()["local_artifacts"]["evidence_packet"]["state"]
        == "digest_invalid"
    )


def test_evidence_packet_missing_digest_unverifiable(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    packet = capture_lib.build_evidence_packet(_valid_capture())
    del packet["content_digest"]
    _write(tmp_path, "evidence_packet.json", packet)
    _use_root(monkeypatch, tmp_path)
    _login(client)

    payload = client.get(STATUS_ROUTE).json()
    assert (
        payload["local_artifacts"]["evidence_packet"]["state"] == "digest_unverifiable"
    )


def test_preflight_report_summaries(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    anchor_report = {
        "schema_version": capture_lib.ANCHOR_PREFLIGHT_REPORT_SCHEMA_VERSION,
        "packet_id": "ORC-TEST-001",
        "boundary": "structural only",
        "summary": {
            "counts": {
                "anchor_bearing": 1,
                "anchor_free": 0,
                "invalid_case": 1,
                "total": 2,
            },
            "needs_attention": ["t2"],
        },
        # A raw prompt buried in case detail must never surface.
        "cases": [{"task_id": "t1", "state": "anchor_bearing", "prompt": RAW_PROMPT}],
    }
    lift_report = {
        "schema_version": capture_lib.LIFT_PREFLIGHT_REPORT_SCHEMA_VERSION,
        "packet_id": "ORC-TEST-001",
        "boundary": "structural only",
        "summary": {
            "counts": {"structural_pass": 1, "total": 1},
            "needs_attention": [],
        },
        "cases": [{"task_id": "t1", "state": "structural_pass", "routed": RAW_ROUTED}],
    }
    _write(tmp_path, "anchor_preflight_report.json", anchor_report)
    _write(tmp_path, "lift_preflight_report.json", lift_report)
    _use_root(monkeypatch, tmp_path)
    _login(client)

    payload = client.get(STATUS_ROUTE).json()
    anchor = payload["local_artifacts"]["anchor_preflight"]
    lift = payload["local_artifacts"]["lift_preflight"]

    assert anchor["state"] == "present"
    assert anchor["needs_attention_count"] == 1
    assert anchor["state_counts"]["invalid_case"] == 1
    assert lift["state"] == "present"
    assert lift["needs_attention_count"] == 0

    # Preflight presence is not a quality/readiness signal, and raw case detail
    # never surfaces.
    html_text = client.get(PAGE_ROUTE).text
    body = json.dumps(payload)
    for raw in (RAW_PROMPT, RAW_ROUTED):
        assert raw not in html_text
        assert raw not in body


def test_path_override_outside_root_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(artifacts.ARTIFACT_ROOT_ENV, "/etc")
    assert artifacts.resolve_artifact_root() == artifacts.DEFAULT_ARTIFACT_ROOT


def test_path_override_traversal_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(artifacts.ARTIFACT_ROOT_ENV, "../../../../../etc")
    assert artifacts.resolve_artifact_root() == artifacts.DEFAULT_ARTIFACT_ROOT


def test_path_override_inside_repo_honored(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(artifacts.ARTIFACT_ROOT_ENV, "local/oc_test_subdir")
    resolved = artifacts.resolve_artifact_root()
    repo_root = Path(artifacts.__file__).resolve().parents[2]
    assert resolved == (repo_root / "local" / "oc_test_subdir").resolve()
    assert str(resolved).startswith(str(repo_root.resolve()))


def test_no_secret_leak_with_artifacts_present(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", FAKE_SECRET)
    capture = _valid_capture()
    _write(tmp_path, "capture.json", capture)
    _write(tmp_path, "evidence_packet.json", capture_lib.build_evidence_packet(capture))
    _use_root(monkeypatch, tmp_path)
    _login(client)

    assert FAKE_SECRET not in client.get(PAGE_ROUTE).text
    assert FAKE_SECRET not in client.get(STATUS_ROUTE).text


def test_no_provider_call_with_artifacts_present(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    import alpha.providers.openai as openai_provider

    def _boom(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("provider client must not be used by operator console")

    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "__init__", _boom)
    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "execute", _boom)
    _write(tmp_path, "capture.json", _valid_capture())
    _use_root(monkeypatch, tmp_path)
    _login(client)

    assert client.get(PAGE_ROUTE).status_code == 200
    assert client.get(STATUS_ROUTE).status_code == 200


def test_artifacts_module_does_not_import_provider_clients() -> None:
    source = Path(artifacts.__file__).read_text(encoding="utf-8")
    for forbidden in ("ProviderClient", "OpenAIProviderClient", "httpx", "requests."):
        assert forbidden not in source


# Recognizable raw text smuggled into a content_digest field must never render.
RAW_DIGEST_LEAK = "RAW-DIGEST-LEAK-must-not-render-zzz"


def test_malformed_content_digest_never_leaks_raw_content(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A corrupted content_digest carrying raw text is withheld and fails safe."""

    packet = capture_lib.build_evidence_packet(_valid_capture())
    # Corrupt the digest to smuggle raw prompt/output-like text.
    packet["content_digest"] = "sha256:" + RAW_DIGEST_LEAK + " " + RAW_PROMPT
    _write(tmp_path, "evidence_packet.json", packet)
    _use_root(monkeypatch, tmp_path)
    _login(client)

    payload = client.get(STATUS_ROUTE).json()
    pkt = payload["local_artifacts"]["evidence_packet"]

    # Malformed digest -> safe non-leaking state, value not returned.
    assert pkt["state"] == "invalid_structure"
    assert pkt.get("content_digest") is None

    html_text = client.get(PAGE_ROUTE).text
    body = json.dumps(payload)
    for raw in (RAW_DIGEST_LEAK, RAW_PROMPT, RAW_BASELINE, RAW_ROUTED):
        assert raw not in html_text
        assert raw not in body


def test_wellformed_digest_value_is_still_exposed(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A valid sha256:<64 hex> digest is still surfaced (regression guard)."""

    packet = capture_lib.build_evidence_packet(_valid_capture())
    _write(tmp_path, "evidence_packet.json", packet)
    _use_root(monkeypatch, tmp_path)
    _login(client)

    pkt = client.get(STATUS_ROUTE).json()["local_artifacts"]["evidence_packet"]
    assert pkt["state"] == "digest_valid"
    assert pkt["content_digest"] == packet["content_digest"]
    assert pkt["content_digest"] in client.get(PAGE_ROUTE).text


def test_invalid_utf8_artifact_fails_safe(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Undecodable artifact bytes report invalid_json and never 500."""

    (tmp_path / "capture.json").write_bytes(b"\xff\xfe\x00\x80 not utf-8 \xff")
    _use_root(monkeypatch, tmp_path)
    _login(client)

    response = client.get(STATUS_ROUTE)
    assert response.status_code == 200
    assert response.json()["local_artifacts"]["capture"]["state"] == "invalid_json"
    assert client.get(PAGE_ROUTE).status_code == 200


# ---------------------------------------------------------------------------
# Artifact freshness and sequence coherence
# (AOC-B003-ARTIFACT-FRESHNESS-001 / UI-ALPHA-OPERATOR-CONSOLE-ARTIFACT-
# FRESHNESS-001). Timestamps are injected and mtimes are controlled so the
# freshness labels and ordering states are deterministic.
# ---------------------------------------------------------------------------
FIXED_NOW = datetime(2026, 7, 7, 12, 0, 0, tzinfo=timezone.utc)
FIXED_NOW_TS = FIXED_NOW.timestamp()


def _set_age(path: Path, seconds_old: float) -> None:
    """Set a file's mtime to ``FIXED_NOW`` minus ``seconds_old``."""

    ts = FIXED_NOW_TS - seconds_old
    os.utime(path, (ts, ts))


def _status(tmp_path: Path, now: datetime = FIXED_NOW) -> dict:
    return artifacts.build_artifact_status(root=tmp_path, now=now)


def _anchor_report(packet_id: str = "ORC-TEST-001") -> dict:
    return {
        "schema_version": capture_lib.ANCHOR_PREFLIGHT_REPORT_SCHEMA_VERSION,
        "packet_id": packet_id,
        "boundary": "structural only",
        "summary": {
            "counts": {
                "anchor_bearing": 1,
                "anchor_free": 0,
                "invalid_case": 1,
                "total": 2,
            },
            "needs_attention": ["t2"],
        },
        "cases": [{"task_id": "t1", "state": "anchor_bearing", "prompt": RAW_PROMPT}],
    }


def _lift_report(packet_id: str = "ORC-TEST-001") -> dict:
    return {
        "schema_version": capture_lib.LIFT_PREFLIGHT_REPORT_SCHEMA_VERSION,
        "packet_id": packet_id,
        "boundary": "structural only",
        "summary": {
            "counts": {"structural_pass": 1, "total": 1},
            "needs_attention": [],
        },
        "cases": [{"task_id": "t1", "state": "structural_pass", "routed": RAW_ROUTED}],
    }


def _write_all_four(tmp_path: Path) -> None:
    capture = _valid_capture()
    _write(tmp_path, "capture.json", capture)
    _write(
        tmp_path,
        "evidence_packet.json",
        capture_lib.build_evidence_packet(capture),
    )
    _write(tmp_path, "anchor_preflight_report.json", _anchor_report())
    _write(tmp_path, "lift_preflight_report.json", _lift_report())


# 1. Status JSON includes status_generated_at_utc.
def test_status_json_includes_status_generated_at_utc(client: TestClient) -> None:
    _login(client)
    local = client.get(STATUS_ROUTE).json()["local_artifacts"]
    generated = local["status_generated_at_utc"]
    assert isinstance(generated, str) and generated
    parsed = datetime.fromisoformat(generated)
    assert parsed.tzinfo is not None


# 2. Each of the four fixed summaries includes safe metadata when present.
def test_freshness_metadata_present_for_all_four_files(tmp_path: Path) -> None:
    _write_all_four(tmp_path)
    names = {
        "capture": "capture.json",
        "evidence_packet": "evidence_packet.json",
        "anchor_preflight": "anchor_preflight_report.json",
        "lift_preflight": "lift_preflight_report.json",
    }
    for filename in names.values():
        _set_age(tmp_path / filename, 10)

    files = _status(tmp_path)["freshness"]["files"]
    for key, filename in names.items():
        meta = files[key]
        assert meta["path_label"] == filename
        assert meta["exists"] is True
        assert meta["metadata_state"] == "present"
        assert isinstance(meta["age_seconds"], int) and meta["age_seconds"] >= 0
        assert meta["modified_at_utc"] is not None
        assert meta["age_label"] == "just_updated"


# 3. Missing files still return safe missing states and render normally.
def test_freshness_missing_files_safe_and_render(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _use_root(monkeypatch, tmp_path)
    _login(client)

    freshness = client.get(STATUS_ROUTE).json()["local_artifacts"]["freshness"]
    for key in ("capture", "evidence_packet", "anchor_preflight", "lift_preflight"):
        meta = freshness["files"][key]
        assert meta["exists"] is False
        assert meta["metadata_state"] == "missing"
        assert meta["age_label"] == "missing"
        assert meta["modified_at_utc"] is None
        assert meta["age_seconds"] is None
    for key in (
        "evidence_packet_vs_capture",
        "anchor_preflight_vs_capture",
        "lift_preflight_vs_capture",
    ):
        assert freshness["sequence_coherence"][key]["state"] == "not_comparable"

    assert client.get(PAGE_ROUTE).status_code == 200


# 4. Invalid JSON still fails safe and does not 500 (freshness still present).
def test_freshness_invalid_json_fails_safe(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    (tmp_path / "capture.json").write_text("{ not valid json", encoding="utf-8")
    _use_root(monkeypatch, tmp_path)
    _login(client)

    response = client.get(STATUS_ROUTE)
    assert response.status_code == 200
    local = response.json()["local_artifacts"]
    assert local["capture"]["state"] == "invalid_json"
    # The file exists on disk, so filesystem metadata is still surfaced.
    assert local["freshness"]["files"]["capture"]["metadata_state"] == "present"
    assert client.get(PAGE_ROUTE).status_code == 200


# 5. Invalid UTF-8 still fails safe and does not 500 (freshness still present).
def test_freshness_invalid_utf8_fails_safe(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    (tmp_path / "capture.json").write_bytes(b"\xff\xfe\x00 not utf-8 \xff")
    _use_root(monkeypatch, tmp_path)
    _login(client)

    response = client.get(STATUS_ROUTE)
    assert response.status_code == 200
    local = response.json()["local_artifacts"]
    assert local["capture"]["state"] == "invalid_json"
    assert local["freshness"]["files"]["capture"]["metadata_state"] == "present"
    assert client.get(PAGE_ROUTE).status_code == 200


# 6. File mtimes are surfaced only as safe metadata (ISO string + int age).
def test_file_mtime_surfaced_only_as_safe_metadata(tmp_path: Path) -> None:
    _write(tmp_path, "capture.json", _valid_capture())
    _set_age(tmp_path / "capture.json", 42)

    status = _status(tmp_path)
    meta = status["freshness"]["files"]["capture"]
    assert meta["age_seconds"] == 42
    assert meta["path_label"] == "capture.json"
    parsed = datetime.fromisoformat(meta["modified_at_utc"])
    expected = FIXED_NOW - timedelta(seconds=42)
    assert abs((parsed - expected).total_seconds()) < 1

    body = json.dumps(status)
    # No absolute path and no raw epoch float leak into the payload.
    assert str(tmp_path) not in body
    assert repr(FIXED_NOW_TS - 42) not in body


# 7. Freshness labels are deterministic under injected time / controlled mtimes.
def test_freshness_labels_are_deterministic(tmp_path: Path) -> None:
    path = tmp_path / "capture.json"
    _write(tmp_path, "capture.json", _valid_capture())

    cases = {
        0: "just_updated",
        300: "just_updated",
        301: "recent",
        3600: "recent",
        86_400: "recent",
        86_401: "older",
    }
    for seconds_old, expected in cases.items():
        _set_age(path, seconds_old)
        label = _status(tmp_path)["freshness"]["files"]["capture"]["age_label"]
        assert label == expected, (seconds_old, label)

    # The pure helper is deterministic for edge/metadata states too.
    assert artifacts.age_label(None, "missing") == "missing"
    assert artifacts.age_label(None, "unavailable") == "unknown"
    assert artifacts.age_label(0, "present") == "just_updated"


# 8. evidence_packet.json older than capture.json -> older_than_capture.
def test_evidence_packet_older_than_capture(tmp_path: Path) -> None:
    capture = _valid_capture()
    _write(tmp_path, "capture.json", capture)
    _write(
        tmp_path, "evidence_packet.json", capture_lib.build_evidence_packet(capture)
    )
    _set_age(tmp_path / "capture.json", 10)
    _set_age(tmp_path / "evidence_packet.json", 3600)

    seq = _status(tmp_path)["freshness"]["sequence_coherence"]
    assert seq["evidence_packet_vs_capture"]["state"] == "older_than_capture"


# 9. anchor_preflight_report.json older than capture.json -> older_than_capture.
def test_anchor_preflight_older_than_capture(tmp_path: Path) -> None:
    _write(tmp_path, "capture.json", _valid_capture())
    _write(tmp_path, "anchor_preflight_report.json", _anchor_report())
    _set_age(tmp_path / "capture.json", 10)
    _set_age(tmp_path / "anchor_preflight_report.json", 3600)

    seq = _status(tmp_path)["freshness"]["sequence_coherence"]
    assert seq["anchor_preflight_vs_capture"]["state"] == "older_than_capture"


# 10. lift_preflight_report.json older than capture.json -> older_than_capture.
def test_lift_preflight_older_than_capture(tmp_path: Path) -> None:
    _write(tmp_path, "capture.json", _valid_capture())
    _write(tmp_path, "lift_preflight_report.json", _lift_report())
    _set_age(tmp_path / "capture.json", 10)
    _set_age(tmp_path / "lift_preflight_report.json", 3600)

    seq = _status(tmp_path)["freshness"]["sequence_coherence"]
    assert seq["lift_preflight_vs_capture"]["state"] == "older_than_capture"


# 11. Derived same-age-or-newer than capture -> same_or_newer_than_capture.
def test_derived_same_or_newer_than_capture(tmp_path: Path) -> None:
    _write_all_four(tmp_path)
    _set_age(tmp_path / "capture.json", 100)
    for filename in (
        "evidence_packet.json",
        "anchor_preflight_report.json",
        "lift_preflight_report.json",
    ):
        _set_age(tmp_path / filename, 10)

    seq = _status(tmp_path)["freshness"]["sequence_coherence"]
    assert seq["evidence_packet_vs_capture"]["state"] == "same_or_newer_than_capture"
    assert seq["anchor_preflight_vs_capture"]["state"] == "same_or_newer_than_capture"
    assert seq["lift_preflight_vs_capture"]["state"] == "same_or_newer_than_capture"


# 12. Packet id mismatch is reported without raw artifact display.
def test_packet_id_mismatch_reported_without_raw(tmp_path: Path) -> None:
    _write(tmp_path, "capture.json", _valid_capture())  # packet_id ORC-TEST-001
    other = _valid_capture()
    other["packet_id"] = "ORC-OTHER-999"
    _write(
        tmp_path, "evidence_packet.json", capture_lib.build_evidence_packet(other)
    )
    _set_age(tmp_path / "capture.json", 10)
    _set_age(tmp_path / "evidence_packet.json", 10)

    status = _status(tmp_path)
    seq = status["freshness"]["sequence_coherence"]["evidence_packet_vs_capture"]
    assert "packet_id_mismatch" in seq["flags"]

    body = json.dumps(status)
    for raw in (RAW_PROMPT, RAW_BASELINE, RAW_ROUTED, RAW_ROUTE_META):
        assert raw not in body


# 13. Digest valid but older than capture still reports a stale sequence state.
def test_digest_valid_but_older_than_capture_still_flags_stale(
    tmp_path: Path,
) -> None:
    capture = _valid_capture()
    _write(tmp_path, "capture.json", capture)
    _write(
        tmp_path, "evidence_packet.json", capture_lib.build_evidence_packet(capture)
    )
    _set_age(tmp_path / "capture.json", 10)
    _set_age(tmp_path / "evidence_packet.json", 3600)

    status = _status(tmp_path)
    # Packet self-integrity is intact...
    assert status["evidence_packet"]["state"] == "digest_valid"
    # ...yet the packet file appears older than capture on disk.
    seq = status["freshness"]["sequence_coherence"]["evidence_packet_vs_capture"]
    assert seq["state"] == "older_than_capture"


# 14. Digest invalid / unverifiable are not hidden by freshness metadata.
def test_digest_invalid_not_hidden_by_freshness(tmp_path: Path) -> None:
    capture = _valid_capture()
    _write(tmp_path, "capture.json", capture)
    packet = capture_lib.build_evidence_packet(capture)
    packet["packet_id"] = "tampered-after-digest"  # digest no longer matches body
    _write(tmp_path, "evidence_packet.json", packet)
    _set_age(tmp_path / "capture.json", 10)
    _set_age(tmp_path / "evidence_packet.json", 10)

    status = _status(tmp_path)
    assert status["evidence_packet"]["state"] == "digest_invalid"
    seq = status["freshness"]["sequence_coherence"]["evidence_packet_vs_capture"]
    assert "digest_invalid" in seq["flags"]


def test_digest_unverifiable_not_hidden_by_freshness(tmp_path: Path) -> None:
    capture = _valid_capture()
    _write(tmp_path, "capture.json", capture)
    packet = capture_lib.build_evidence_packet(capture)
    del packet["content_digest"]
    _write(tmp_path, "evidence_packet.json", packet)
    _set_age(tmp_path / "capture.json", 10)
    _set_age(tmp_path / "evidence_packet.json", 10)

    status = _status(tmp_path)
    assert status["evidence_packet"]["state"] == "digest_unverifiable"
    seq = status["freshness"]["sequence_coherence"]["evidence_packet_vs_capture"]
    assert "digest_unverifiable" in seq["flags"]


# 15. Fake API keys never appear in HTML or JSON when freshness is rendered.
def test_fake_secret_never_leaks_with_freshness(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", FAKE_SECRET)
    capture = _valid_capture()
    _write(tmp_path, "capture.json", capture)
    _write(
        tmp_path, "evidence_packet.json", capture_lib.build_evidence_packet(capture)
    )
    _set_age(tmp_path / "capture.json", 10)
    _set_age(tmp_path / "evidence_packet.json", 20)
    _use_root(monkeypatch, tmp_path)
    _login(client)

    assert FAKE_SECRET not in client.get(PAGE_ROUTE).text
    assert FAKE_SECRET not in client.get(STATUS_ROUTE).text


# 16. Raw prompt / baseline / routed / route-metadata never appear with freshness.
def test_raw_content_never_leaks_with_freshness(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _write_all_four(tmp_path)
    for filename in (
        "capture.json",
        "evidence_packet.json",
        "anchor_preflight_report.json",
        "lift_preflight_report.json",
    ):
        _set_age(tmp_path / filename, 30)
    _use_root(monkeypatch, tmp_path)
    _login(client)

    html_text = client.get(PAGE_ROUTE).text
    body = client.get(STATUS_ROUTE).text
    for raw in (RAW_PROMPT, RAW_BASELINE, RAW_ROUTED, RAW_ROUTE_META):
        assert raw not in html_text
        assert raw not in body


# 17. Provider client constructors patched to raise still allow both routes.
def test_provider_client_patched_raise_routes_ok_with_freshness(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    import alpha.providers.openai as openai_provider

    def _boom(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("provider client must not be used by operator console")

    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "__init__", _boom)
    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "execute", _boom)

    capture = _valid_capture()
    _write(tmp_path, "capture.json", capture)
    _write(
        tmp_path, "evidence_packet.json", capture_lib.build_evidence_packet(capture)
    )
    _set_age(tmp_path / "capture.json", 10)
    _set_age(tmp_path / "evidence_packet.json", 20)
    _use_root(monkeypatch, tmp_path)
    _login(client)

    assert client.get(PAGE_ROUTE).status_code == 200
    assert client.get(STATUS_ROUTE).status_code == 200


# 18. Source-scan: no provider/network/subprocess/browser/CLI execution imports.
def test_no_execution_imports_in_console_sources() -> None:
    forbidden = (
        "ProviderClient",
        "OpenAIProviderClient",
        "httpx",
        "requests.",
        "import subprocess",
        "subprocess.",
        "import socket",
        "urllib",
        "playwright",
        "selenium",
        "webdriver",
        "webbrowser",
        "pexpect",
    )
    for module in (artifacts, operator_console):
        source = Path(module.__file__).read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in source, f"{token!r} found in {module.__file__}"


# 19. Outside-root override remains rejected.
def test_freshness_outside_root_override_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(artifacts.ARTIFACT_ROOT_ENV, "/etc")
    assert artifacts.resolve_artifact_root() == artifacts.DEFAULT_ARTIFACT_ROOT


# 20. Inside-repo override remains honored.
def test_freshness_inside_root_override_honored(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(artifacts.ARTIFACT_ROOT_ENV, "local/oc_freshness_subdir")
    resolved = artifacts.resolve_artifact_root()
    repo_root = Path(artifacts.__file__).resolve().parents[2]
    assert resolved == (repo_root / "local" / "oc_freshness_subdir").resolve()


# 21. No path is taken from request data (query params, headers).
def test_no_path_taken_from_request_data(client: TestClient) -> None:
    _login(client)
    response = client.get(
        STATUS_ROUTE + "?root=/etc&artifact_root=/etc&path=/etc/passwd",
        headers={"X-Artifact-Root": "/etc"},
    )
    assert response.status_code == 200
    local = response.json()["local_artifacts"]
    # The fixed default root is used regardless of request-supplied paths.
    assert local["artifact_root"] == "local/operator_console"
    assert "/etc" not in json.dumps(local)


# ---------------------------------------------------------------------------
# Provider, model, and cost gate panel
# (AOC-B004-PROVIDER-COST-GATE-PANEL-001 /
# UI-ALPHA-OPERATOR-CONSOLE-PROVIDER-COST-GATE-PANEL-001). The gate is a
# display-only view of configuration and safety-gate state: no credential
# validation, no provider call, no billing truth, no authorization of live
# execution.
# ---------------------------------------------------------------------------
# Every environment variable the gate inspects. Cleared so tests start from a
# known "nothing configured" baseline unless a test sets a value explicitly.
_GATE_ENVS = (
    "ALPHA_PROVIDER_EMERGENCY_STOP",
    "ALPHA_LIVE_PREVIEW_ENABLED",
    "ALPHA_PROVIDER_MAX_COST_USD",
    "ALPHA_PROVIDER_MAX_INPUT_TOKENS",
    "ALPHA_PROVIDER_MAX_OUTPUT_TOKENS",
    "ALPHA_PROVIDER_MAX_REQUESTS",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GOOGLE_API_KEY",
    "GEMINI_API_KEY",
)


def _clear_gate_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for env in _GATE_ENVS:
        monkeypatch.delenv(env, raising=False)


def _gate(client: TestClient) -> dict:
    return client.get(STATUS_ROUTE).json()["provider_gate"]


# 1. Status JSON includes the expanded provider_gate fields.
def test_provider_gate_includes_expanded_fields(client: TestClient) -> None:
    _login(client)
    gate = _gate(client)
    for field in (
        "configured_provider",
        "provider_mode_label",
        "live_provider_calls",
        "console_calls_providers",
        "emergency_stop",
        "live_preview_surface",
        "key_status",
        "required_provider_keys",
        "provider_key_status",
        "cap_status",
        "cap_completeness",
        "cost_cap_status",
        "token_request_cap_status",
        "live_execution_gate",
        "live_execution_blockers",
        "gate_boundary",
    ):
        assert field in gate, field
    assert set(gate["cap_status"].keys()) == {
        "max_cost_usd",
        "max_input_tokens",
        "max_output_tokens",
        "max_requests",
    }


# 2. Default provider gate remains blocked and display-only.
def test_provider_gate_default_blocked_and_display_only(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _clear_gate_env(monkeypatch)
    _login(client)
    gate = _gate(client)
    assert gate["live_execution_gate"] == "blocked"
    assert "display_only_lane" in gate["live_execution_blockers"]
    assert "live_provider_calls_disabled" in gate["live_execution_blockers"]
    assert "display-only" in gate["gate_boundary"]


# 3. Live provider calls remain disabled.
def test_provider_gate_live_calls_disabled(client: TestClient) -> None:
    _login(client)
    gate = _gate(client)
    assert gate["live_provider_calls"] == "disabled"
    assert gate["console_calls_providers"] is False


# 4. Live-run button remains disabled (with the expanded gate panel present).
def test_live_run_button_still_disabled_with_gate_panel(client: TestClient) -> None:
    _login(client)
    html_text = client.get(PAGE_ROUTE).text
    assert "Live run (disabled)" in html_text
    assert 'class="disabled-btn" disabled' in html_text
    assert client.get(STATUS_ROUTE).json()["run_setup"][
        "live_run_button_enabled"
    ] is False


# 5. Emergency stop engaged appears as a blocker.
def test_emergency_stop_appears_as_blocker(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _clear_gate_env(monkeypatch)
    monkeypatch.setenv("ALPHA_PROVIDER_EMERGENCY_STOP", "1")
    _login(client)
    gate = _gate(client)
    assert gate["emergency_stop"] == "engaged"
    assert "emergency_stop_engaged" in gate["live_execution_blockers"]


# 6. Missing provider key for the configured provider appears as a safe blocker
#    without displaying any value.
def test_missing_provider_key_blocker(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _clear_gate_env(monkeypatch)
    # Configured provider requires a key that is absent.
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    _login(client)
    gate = _gate(client)
    assert gate["provider_key_status"] == "missing"
    assert "missing_provider_key" in gate["live_execution_blockers"]
    assert gate["key_status"]["OPENAI_API_KEY"] == "missing"


# 7. Present provider key for the configured provider reports present only,
#    never a raw or partial value.
def test_present_provider_key_categorical_only(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _clear_gate_env(monkeypatch)
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", FAKE_SECRET)
    _login(client)
    status_text = client.get(STATUS_ROUTE).text
    gate = _gate(client)
    assert gate["key_status"]["OPENAI_API_KEY"] == "present"
    assert gate["provider_key_status"] == "present"
    assert "missing_provider_key" not in gate["live_execution_blockers"]
    assert FAKE_SECRET not in status_text
    # Not even a partial (prefix or suffix) of the key value is surfaced.
    assert FAKE_SECRET[:20] not in status_text
    assert FAKE_SECRET[-20:] not in status_text


# 8. Missing cost cap appears as a safe blocker.
def test_missing_cost_cap_blocker(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _clear_gate_env(monkeypatch)
    _login(client)
    gate = _gate(client)
    assert gate["cost_cap_status"] == "missing"
    assert "missing_cost_cap" in gate["live_execution_blockers"]


# 9. Partial cap configuration reports partial or equivalent safe state.
def test_partial_cap_configuration_reports_partial(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _clear_gate_env(monkeypatch)
    monkeypatch.setenv("ALPHA_PROVIDER_MAX_INPUT_TOKENS", "1000")
    _login(client)
    gate = _gate(client)
    assert gate["cap_completeness"] == "partially_configured"
    assert gate["token_request_cap_status"] == "partial"
    assert gate["cap_status"]["max_input_tokens"] == "present"
    assert gate["cap_status"]["max_output_tokens"] == "missing"
    assert "missing_token_or_request_cap" in gate["live_execution_blockers"]


# 10. Complete cap configuration reports configured or equivalent safe state.
def test_complete_cap_configuration_reports_configured(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _clear_gate_env(monkeypatch)
    for env in (
        "ALPHA_PROVIDER_MAX_COST_USD",
        "ALPHA_PROVIDER_MAX_INPUT_TOKENS",
        "ALPHA_PROVIDER_MAX_OUTPUT_TOKENS",
        "ALPHA_PROVIDER_MAX_REQUESTS",
    ):
        monkeypatch.setenv(env, "5")
    _login(client)
    gate = _gate(client)
    assert gate["cap_completeness"] == "configured"
    assert gate["cost_cap_status"] == "present"
    assert gate["token_request_cap_status"] == "present"
    assert "missing_cost_cap" not in gate["live_execution_blockers"]
    assert "missing_token_or_request_cap" not in gate["live_execution_blockers"]
    # Complete caps do not authorize live execution; the gate stays blocked.
    assert gate["live_execution_gate"] == "blocked"


# 11. Live-preview surface enabled does not by itself permit live execution.
def test_live_preview_enabled_does_not_permit_execution(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _clear_gate_env(monkeypatch)
    monkeypatch.setenv("ALPHA_LIVE_PREVIEW_ENABLED", "1")
    _login(client)
    gate = _gate(client)
    assert gate["live_preview_surface"] == "enabled"
    assert "live_preview_surface_disabled" not in gate["live_execution_blockers"]
    assert gate["live_execution_gate"] == "blocked"
    assert "live_provider_calls_disabled" in gate["live_execution_blockers"]
    assert "display_only_lane" in gate["live_execution_blockers"]


# 12. Provider gate never validates credentials.
def test_provider_gate_never_validates_credentials(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _clear_gate_env(monkeypatch)
    monkeypatch.setenv("OPENAI_API_KEY", FAKE_SECRET)
    _login(client)
    gate = _gate(client)
    # Key status is categorical presence only, never a validity verdict.
    assert set(gate["key_status"].values()) <= {"present", "missing"}
    # The gate explicitly states no credential validation is performed.
    assert "credential validation" in gate["gate_boundary"]
    assert (
        operator_console.GATE_NO_CREDENTIAL_VALIDATION_TEXT
        in client.get(PAGE_ROUTE).text
    )


# 13. Provider gate never calls provider clients.
def test_provider_gate_never_calls_provider_clients(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    import alpha.providers.openai as openai_provider

    def _boom(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("provider client must not be used by operator console")

    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "__init__", _boom)
    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "execute", _boom)
    monkeypatch.setenv("OPENAI_API_KEY", FAKE_SECRET)
    _login(client)
    assert client.get(STATUS_ROUTE).status_code == 200
    assert operator_console.build_console_status()["provider_gate"][
        "console_calls_providers"
    ] is False


# 14. Provider client constructors patched to raise still allow both routes.
def test_provider_client_patched_raise_both_routes_ok_with_gate(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    import alpha.providers.openai as openai_provider

    def _boom(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("provider client must not be used by operator console")

    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "__init__", _boom)
    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "execute", _boom)
    monkeypatch.setenv("OPENAI_API_KEY", FAKE_SECRET)
    _login(client)
    assert client.get(PAGE_ROUTE).status_code == 200
    assert client.get(STATUS_ROUTE).status_code == 200


# 15. Fake API keys never appear in HTML, JSON, or reprs.
def test_fake_key_never_appears_in_gate_html_json_repr(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", FAKE_SECRET)
    monkeypatch.setenv("ANTHROPIC_API_KEY", FAKE_SECRET)
    _login(client)
    assert FAKE_SECRET not in client.get(PAGE_ROUTE).text
    assert FAKE_SECRET not in client.get(STATUS_ROUTE).text
    assert FAKE_SECRET not in repr(operator_console.build_console_status())


# 16. Status JSON contains no raw environment values for inspected env vars.
def test_no_raw_env_values_in_status_json(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    sentinels = {
        "ALPHA_PROVIDER_MAX_COST_USD": "CAP-COST-SENTINEL-123",
        "ALPHA_PROVIDER_MAX_INPUT_TOKENS": "CAP-IN-SENTINEL-123",
        "ALPHA_PROVIDER_MAX_OUTPUT_TOKENS": "CAP-OUT-SENTINEL-123",
        "ALPHA_PROVIDER_MAX_REQUESTS": "CAP-REQ-SENTINEL-123",
        "ALPHA_PROVIDER_EMERGENCY_STOP": "STOP-SENTINEL-123",
        "ALPHA_LIVE_PREVIEW_ENABLED": "PREVIEW-SENTINEL-123",
        "OPENAI_API_KEY": FAKE_SECRET,
    }
    for env, value in sentinels.items():
        monkeypatch.setenv(env, value)
    _login(client)
    body = client.get(STATUS_ROUTE).text
    for value in sentinels.values():
        assert value not in body


# 17. Rendered HTML contains the provider/cost gate boundary text.
def test_gate_boundary_text_in_html(client: TestClient) -> None:
    _login(client)
    html_text = client.get(PAGE_ROUTE).text
    for text in operator_console.GATE_BOUNDARY_TEXTS:
        assert text in html_text


# 18. Source-scan: no execution imports in the console route module.
def test_route_module_has_no_execution_imports() -> None:
    source = Path(operator_console.__file__).read_text(encoding="utf-8")
    forbidden = (
        "ProviderClient",
        "OpenAIProviderClient",
        "httpx",
        "requests.",
        "import subprocess",
        "subprocess.",
        "import socket",
        "urllib",
        "playwright",
        "selenium",
        "webdriver",
        "webbrowser",
        "pexpect",
    )
    for token in forbidden:
        assert token not in source, f"{token!r} found in {operator_console.__file__}"


# 19. No scoring/ranking/winner/billing/model-comparison claim language in the UI.
def test_gate_ui_has_no_scoring_or_billing_claim_language(client: TestClient) -> None:
    _login(client)
    html_text = client.get(PAGE_ROUTE).text.lower()
    for forbidden in (
        "winner",
        "ranking",
        "leaderboard",
        "score:",
        "outperforms",
        "production ready",
        "ready for production",
        "exact spend",
        "estimated cost",
        "estimated spend",
        "model comparison",
    ):
        assert forbidden not in html_text


# 20. Existing artifact status / freshness surfaces persist alongside the gate.
def test_artifact_surfaces_persist_with_gate_panel(client: TestClient) -> None:
    _login(client)
    payload = client.get(STATUS_ROUTE).json()
    assert "provider_gate" in payload
    assert payload["provider_gate"]["live_execution_gate"] == "blocked"
    local = payload["local_artifacts"]
    assert "freshness" in local
    assert "status_generated_at_utc" in local
    for section in ("capture", "evidence_packet", "anchor_preflight", "lift_preflight"):
        assert section in local


# ---------------------------------------------------------------------------
# Provider-specific required-key gating (Codex P2 regression).
# The missing_provider_key blocker must be derived from the *configured
# provider's* required key, not from any known key. Mirrors the categorical
# provider-key mapping in scripts/check_env.py without reading or validating a
# key value.
# ---------------------------------------------------------------------------
def _gate_for_provider(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    provider: str,
    present_keys: tuple = (),
) -> dict:
    _clear_gate_env(monkeypatch)
    monkeypatch.setenv("MODEL_PROVIDER", provider)
    for env in present_keys:
        monkeypatch.setenv(env, FAKE_SECRET)
    _login(client)
    return _gate(client)


# 1. anthropic + only OPENAI_API_KEY present still blocks with missing_provider_key.
def test_anthropic_with_only_openai_key_still_missing_provider_key(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    gate = _gate_for_provider(
        client, monkeypatch, "anthropic", present_keys=("OPENAI_API_KEY",)
    )
    assert gate["configured_provider"] == "anthropic"
    assert gate["required_provider_keys"] == ["ANTHROPIC_API_KEY"]
    assert gate["provider_key_status"] == "missing"
    assert "missing_provider_key" in gate["live_execution_blockers"]
    assert gate["live_execution_gate"] == "blocked"


# 2. anthropic + ANTHROPIC_API_KEY present removes missing_provider_key.
def test_anthropic_with_anthropic_key_removes_missing_provider_key(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    gate = _gate_for_provider(
        client, monkeypatch, "anthropic", present_keys=("ANTHROPIC_API_KEY",)
    )
    assert gate["provider_key_status"] == "present"
    assert "missing_provider_key" not in gate["live_execution_blockers"]
    assert gate["live_execution_gate"] == "blocked"


# 3. openai + OPENAI_API_KEY present removes missing_provider_key.
def test_openai_with_openai_key_removes_missing_provider_key(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    gate = _gate_for_provider(
        client, monkeypatch, "openai", present_keys=("OPENAI_API_KEY",)
    )
    assert gate["required_provider_keys"] == ["OPENAI_API_KEY"]
    assert gate["provider_key_status"] == "present"
    assert "missing_provider_key" not in gate["live_execution_blockers"]


# 4. google + GOOGLE_API_KEY present removes missing_provider_key.
def test_google_with_google_key_removes_missing_provider_key(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    gate = _gate_for_provider(
        client, monkeypatch, "google", present_keys=("GOOGLE_API_KEY",)
    )
    assert gate["required_provider_keys"] == ["GOOGLE_API_KEY"]
    assert gate["provider_key_status"] == "present"
    assert "missing_provider_key" not in gate["live_execution_blockers"]


# 5. gemini + GOOGLE_API_KEY present removes missing_provider_key.
def test_gemini_with_google_key_removes_missing_provider_key(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    gate = _gate_for_provider(
        client, monkeypatch, "gemini", present_keys=("GOOGLE_API_KEY",)
    )
    assert gate["required_provider_keys"] == ["GOOGLE_API_KEY"]
    assert gate["provider_key_status"] == "present"
    assert "missing_provider_key" not in gate["live_execution_blockers"]


# 6. local requires no provider key.
def test_local_provider_requires_no_key(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    gate = _gate_for_provider(client, monkeypatch, "local")
    assert gate["required_provider_keys"] == []
    assert gate["provider_key_status"] == "not_required"
    assert "missing_provider_key" not in gate["live_execution_blockers"]
    assert gate["live_execution_gate"] == "blocked"


# 7. none requires no provider key.
def test_none_provider_requires_no_key(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    gate = _gate_for_provider(client, monkeypatch, "none")
    assert gate["required_provider_keys"] == []
    assert gate["provider_key_status"] == "not_required"
    assert "missing_provider_key" not in gate["live_execution_blockers"]
    assert gate["live_execution_gate"] == "blocked"


# 8. local_llm is not satisfied by any hosted-provider key; stays blocked.
def test_local_llm_not_satisfied_by_hosted_keys(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    gate = _gate_for_provider(
        client,
        monkeypatch,
        "local_llm",
        present_keys=(
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "GOOGLE_API_KEY",
            "GEMINI_API_KEY",
        ),
    )
    assert gate["provider_key_status"] == "not_evaluated"
    # Hosted-provider keys do not satisfy local_llm.
    assert "missing_provider_key" not in gate["live_execution_blockers"]
    assert "local_llm_configuration_not_evaluated" in gate["live_execution_blockers"]
    assert gate["live_execution_gate"] == "blocked"


# 9. Raw key values never appear in HTML, JSON, or reprs under provider gating.
def test_provider_gating_never_leaks_key_values(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _clear_gate_env(monkeypatch)
    monkeypatch.setenv("MODEL_PROVIDER", "google")
    monkeypatch.setenv("GOOGLE_API_KEY", FAKE_SECRET)
    monkeypatch.setenv("OPENAI_API_KEY", FAKE_SECRET)
    _login(client)
    assert FAKE_SECRET not in client.get(PAGE_ROUTE).text
    assert FAKE_SECRET not in client.get(STATUS_ROUTE).text
    assert FAKE_SECRET not in repr(operator_console.build_console_status())


# 10. Provider clients patched to raise still allow both routes with gating.
def test_provider_gating_does_not_call_provider_clients(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    import alpha.providers.openai as openai_provider

    def _boom(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("provider client must not be used by operator console")

    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "__init__", _boom)
    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "execute", _boom)
    _clear_gate_env(monkeypatch)
    monkeypatch.setenv("MODEL_PROVIDER", "anthropic")
    _login(client)
    assert client.get(PAGE_ROUTE).status_code == 200
    assert client.get(STATUS_ROUTE).status_code == 200
