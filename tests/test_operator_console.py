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

import ast
import html
import importlib
import json
import os
import socket
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_ROOT = Path(__file__).resolve().parent
for import_root in (PROJECT_ROOT, TEST_ROOT):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from alpha.webapp import operator_console_artifacts as artifacts  # noqa: E402
from alpha.webapp import operator_console_receipts as receipts  # noqa: E402
from alpha.webapp.routes import auth, operator_console  # noqa: E402
from alpha.eval import operator_run_capture as capture_lib  # noqa: E402
from service.app import app, _mount_dashboard  # noqa: E402
from operator_console_safety import (  # noqa: E402
    OperatorConsoleSafetyViolation,
    operator_console_no_execution_guard,
    operator_console_no_get_write_guard,
)

PAGE_ROUTE = operator_console.ROUTE
STATUS_ROUTE = operator_console.STATUS_ROUTE
RECEIPTS_ROUTE = operator_console.RECEIPTS_ROUTE

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
    assert RECEIPTS_ROUTE in paths
    assert RECEIPTS_ROUTE in paths


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
        assert bare_client.post(RECEIPTS_ROUTE).status_code == 404
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
        "card-local-receipt-store",
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
        "local_receipts",
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


# ---------------------------------------------------------------------------
# Dry-Run Preview panel
# (AOC-B005-DRY-RUN-PREVIEW-001 /
# UI-ALPHA-OPERATOR-CONSOLE-DRY-RUN-PREVIEW-001). The panel is a display-only
# read of what a *future* dry-run would prepare or require, derived only from the
# existing local artifact status and provider-gate status. It executes nothing:
# no solve, no provider call, no /v1/solve, no CLI/subprocess, no artifact
# mutation, and no synthesized runtime output.
# ---------------------------------------------------------------------------
# Additional recognizable raw content that must never surface in HTML or JSON.
RAW_SYS_PROMPT = "RAW-SYSTEM-PROMPT-must-not-render-zzz"
RAW_PROVIDER_PAYLOAD = "RAW-PROVIDER-PAYLOAD-must-not-render-zzz"


def _dry_run(client: TestClient) -> dict:
    return client.get(STATUS_ROUTE).json()["dry_run_preview"]


def _dry_run_card_html(html_text: str) -> str:
    start = html_text.index('id="card-dry-run-preview"')
    end = html_text.index("</article>", start)
    return html_text[start:end]


def _scaffold_capture() -> dict:
    """A structurally valid (but not export-ready) capture with a raw prompt."""

    packet = {
        "packet_id": "ORC-TEST-001",
        "cases": [{"task_id": "t1", "prompt": RAW_PROMPT}],
    }
    return capture_lib.scaffold_capture(packet)


def _capture_with_sensitive_metadata() -> dict:
    """An export-ready capture whose route_metadata carries extra raw sentinels."""

    capture = _valid_capture()
    capture["cases"][0]["route_metadata"] = {
        "route": RAW_ROUTE_META,
        "system_prompt": RAW_SYS_PROMPT,
        "provider_payload": RAW_PROVIDER_PAYLOAD,
    }
    return capture


# 1. Status JSON includes the new dry-run preview section.
def test_dry_run_preview_section_in_status(client: TestClient) -> None:
    _login(client)
    payload = client.get(STATUS_ROUTE).json()
    assert "dry_run_preview" in payload
    dr = payload["dry_run_preview"]
    for field in (
        "preview_mode",
        "dry_run_execution",
        "would_use",
        "input_source_status",
        "evidence_packet_status",
        "preflight_status",
        "freshness_warnings",
        "provider_gate_summary",
        "preview_readiness",
        "preview_blockers",
        "boundary",
        "boundary_notes",
    ):
        assert field in dr, field
    assert dr["would_use"] == list(operator_console.DRY_RUN_WOULD_USE)
    assert set(dr["preflight_status"].keys()) == {"anchor", "lift"}


# 2. Dry-run preview mode is display-only.
def test_dry_run_preview_mode_display_only(client: TestClient) -> None:
    _login(client)
    assert _dry_run(client)["preview_mode"] == "display_only"


# 3. Dry-run execution is not enabled.
def test_dry_run_execution_not_enabled(client: TestClient) -> None:
    _login(client)
    assert _dry_run(client)["dry_run_execution"] == "not_enabled"


# 4. Live-run button remains disabled with the dry-run preview panel present.
def test_dry_run_live_run_button_remains_disabled(client: TestClient) -> None:
    _login(client)
    html_text = client.get(PAGE_ROUTE).text
    assert "Live run (disabled)" in html_text
    assert 'class="disabled-btn" disabled' in html_text
    assert (
        client.get(STATUS_ROUTE).json()["run_setup"]["live_run_button_enabled"]
        is False
    )


# 5. No POST/action route (or any non-GET route) is added for dry-run preview.
def test_dry_run_adds_no_execution_routes_beyond_receipt_post() -> None:
    console_routes = [
        route
        for route in app.routes
        if getattr(route, "path", "").startswith("/dashboard/operator-console")
    ]
    post_routes = []
    for route in console_routes:
        methods = getattr(route, "methods", set()) or set()
        if "POST" in methods:
            post_routes.append(getattr(route, "path", ""))
        assert "PUT" not in methods
        assert "DELETE" not in methods
        assert "PATCH" not in methods
    assert post_routes == [RECEIPTS_ROUTE]
    assert {getattr(route, "path", None) for route in console_routes} == {
        PAGE_ROUTE,
        STATUS_ROUTE,
        RECEIPTS_ROUTE,
    }


# 6. Missing capture produces safe preview blockers and still renders.
def test_dry_run_missing_capture_blockers_and_renders(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _use_root(monkeypatch, tmp_path)
    _login(client)
    dr = _dry_run(client)
    assert dr["input_source_status"] == "capture_missing"
    assert "missing_capture" in dr["preview_blockers"]
    assert "missing_evidence_packet" in dr["preview_blockers"]
    assert "missing_preflight_reports" in dr["preview_blockers"]
    assert dr["preview_readiness"] == "needs_artifacts"
    assert client.get(PAGE_ROUTE).status_code == 200


# 7. Invalid capture produces safe preview blockers and still renders.
def test_dry_run_invalid_capture_blockers_and_renders(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    (tmp_path / "capture.json").write_text("{ not valid json", encoding="utf-8")
    _use_root(monkeypatch, tmp_path)
    _login(client)
    dr = _dry_run(client)
    assert dr["input_source_status"] == "capture_invalid"
    assert "invalid_capture" in dr["preview_blockers"]
    assert dr["preview_readiness"] == "unavailable"
    assert client.get(PAGE_ROUTE).status_code == 200


# 8. Structurally valid capture -> local input status, no raw prompt/output.
def test_dry_run_structurally_valid_capture_no_raw(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _write(tmp_path, "capture.json", _scaffold_capture())
    _use_root(monkeypatch, tmp_path)
    _login(client)
    dr = _dry_run(client)
    assert dr["input_source_status"] == "capture_structurally_valid"

    html_text = client.get(PAGE_ROUTE).text
    body = client.get(STATUS_ROUTE).text
    for raw in (RAW_PROMPT, RAW_BASELINE, RAW_ROUTED, RAW_ROUTE_META):
        assert raw not in html_text
        assert raw not in body


# 9. Export-ready capture -> local input status, no raw prompt/output.
def test_dry_run_export_ready_capture_no_raw(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _write(tmp_path, "capture.json", _valid_capture())
    _use_root(monkeypatch, tmp_path)
    _login(client)
    dr = _dry_run(client)
    assert dr["input_source_status"] == "capture_export_ready"

    html_text = client.get(PAGE_ROUTE).text
    body = client.get(STATUS_ROUTE).text
    for raw in (RAW_PROMPT, RAW_BASELINE, RAW_ROUTED, RAW_ROUTE_META):
        assert raw not in html_text
        assert raw not in body


# 10. Missing evidence packet produces a safe preview blocker.
def test_dry_run_missing_evidence_packet_blocker(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _write(tmp_path, "capture.json", _valid_capture())
    _use_root(monkeypatch, tmp_path)
    _login(client)
    dr = _dry_run(client)
    assert dr["evidence_packet_status"] == "missing"
    assert "missing_evidence_packet" in dr["preview_blockers"]


# 11. Digest-valid evidence packet is self-integrity only, not readiness/quality.
def test_dry_run_digest_valid_is_self_integrity_only(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    capture = _valid_capture()
    _write(tmp_path, "capture.json", capture)
    _write(
        tmp_path, "evidence_packet.json", capture_lib.build_evidence_packet(capture)
    )
    # No preflight reports written, so the packet's valid digest alone must not
    # promote the preview to preview_ready.
    _use_root(monkeypatch, tmp_path)
    _login(client)
    dr = _dry_run(client)
    assert dr["evidence_packet_status"] == "digest_valid"
    assert dr["preview_readiness"] == "needs_artifacts"
    assert "missing_preflight_reports" in dr["preview_blockers"]
    # The boundary that a preview-ready state is not evidence appears in the UI.
    assert operator_console.DRY_RUN_NOT_EVIDENCE_TEXT in client.get(PAGE_ROUTE).text


# 12. Digest-invalid and digest-unverifiable states produce safe warnings/blockers.
def test_dry_run_digest_invalid_and_unverifiable_states(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    capture = _valid_capture()

    # digest_invalid: tamper the packet body after the digest was computed.
    invalid = capture_lib.build_evidence_packet(capture)
    invalid["packet_id"] = "tampered-after-digest"
    _write(tmp_path, "capture.json", capture)
    _write(tmp_path, "evidence_packet.json", invalid)
    _use_root(monkeypatch, tmp_path)
    _login(client)
    dr = _dry_run(client)
    assert dr["evidence_packet_status"] == "digest_invalid"
    assert "invalid_or_unverified_evidence_packet" in dr["preview_blockers"]
    assert "digest_invalid" in dr["freshness_warnings"]

    # digest_unverifiable: remove the recorded digest entirely.
    unverifiable = capture_lib.build_evidence_packet(capture)
    del unverifiable["content_digest"]
    _write(tmp_path, "evidence_packet.json", unverifiable)
    dr = _dry_run(client)
    assert dr["evidence_packet_status"] == "digest_unverifiable"
    assert "invalid_or_unverified_evidence_packet" in dr["preview_blockers"]
    assert "digest_unverifiable" in dr["freshness_warnings"]


# 13. Missing anchor/lift preflight reports produce a safe preview blocker.
def test_dry_run_missing_preflight_reports_blocker(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _write(tmp_path, "capture.json", _valid_capture())
    _use_root(monkeypatch, tmp_path)
    _login(client)
    dr = _dry_run(client)
    assert dr["preflight_status"] == {"anchor": "anchor_missing", "lift": "lift_missing"}
    assert "missing_preflight_reports" in dr["preview_blockers"]


# 14. Present anchor/lift reports are shown as local metadata only; a complete,
#     fresh, digest-valid set reaches preview_ready (metadata completeness only).
def test_dry_run_present_preflight_reports_metadata_only(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _write_all_four(tmp_path)
    _use_root(monkeypatch, tmp_path)
    _login(client)
    dr = _dry_run(client)
    assert dr["preflight_status"] == {"anchor": "anchor_present", "lift": "lift_present"}
    assert dr["preview_readiness"] == "preview_ready"
    assert "missing_preflight_reports" not in dr["preview_blockers"]
    # Even preview_ready never authorizes execution or leaks raw content.
    assert dr["dry_run_execution"] == "not_enabled"
    body = client.get(STATUS_ROUTE).text
    html_text = client.get(PAGE_ROUTE).text
    for raw in (RAW_PROMPT, RAW_BASELINE, RAW_ROUTED, RAW_ROUTE_META):
        assert raw not in body
        assert raw not in html_text


# 15. Stale evidence packet vs capture produces a safe freshness warning.
def test_dry_run_stale_evidence_packet_warning(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    capture = _valid_capture()
    _write(tmp_path, "capture.json", capture)
    _write(
        tmp_path, "evidence_packet.json", capture_lib.build_evidence_packet(capture)
    )
    _set_age(tmp_path / "capture.json", 10)
    _set_age(tmp_path / "evidence_packet.json", 3600)
    _use_root(monkeypatch, tmp_path)
    _login(client)
    dr = _dry_run(client)
    assert "evidence_packet_older_than_capture" in dr["freshness_warnings"]
    assert "stale_derived_artifacts" in dr["preview_blockers"]


# 16. Stale anchor preflight vs capture produces a safe freshness warning.
def test_dry_run_stale_anchor_preflight_warning(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _write(tmp_path, "capture.json", _valid_capture())
    _write(tmp_path, "anchor_preflight_report.json", _anchor_report())
    _set_age(tmp_path / "capture.json", 10)
    _set_age(tmp_path / "anchor_preflight_report.json", 3600)
    _use_root(monkeypatch, tmp_path)
    _login(client)
    dr = _dry_run(client)
    assert "anchor_preflight_older_than_capture" in dr["freshness_warnings"]
    assert "stale_derived_artifacts" in dr["preview_blockers"]


# 17. Stale lift preflight vs capture produces a safe freshness warning.
def test_dry_run_stale_lift_preflight_warning(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _write(tmp_path, "capture.json", _valid_capture())
    _write(tmp_path, "lift_preflight_report.json", _lift_report())
    _set_age(tmp_path / "capture.json", 10)
    _set_age(tmp_path / "lift_preflight_report.json", 3600)
    _use_root(monkeypatch, tmp_path)
    _login(client)
    dr = _dry_run(client)
    assert "lift_preflight_older_than_capture" in dr["freshness_warnings"]
    assert "stale_derived_artifacts" in dr["preview_blockers"]


# 18. Provider gate summary is included but live execution remains blocked.
def test_dry_run_provider_gate_summary_blocked(client: TestClient) -> None:
    _login(client)
    dr = _dry_run(client)
    summary = dr["provider_gate_summary"]
    for field in (
        "live_execution_gate",
        "provider_key_status",
        "cap_completeness",
        "live_execution_blockers",
    ):
        assert field in summary
    assert summary["live_execution_gate"] == "blocked"
    assert "provider_live_execution_blocked" in dr["preview_blockers"]
    assert "display_only_lane" in dr["preview_blockers"]


# 19. Complete provider/cap configuration does not enable dry-run execution.
def test_dry_run_complete_config_does_not_enable_execution(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _clear_gate_env(monkeypatch)
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", FAKE_SECRET)
    for env in (
        "ALPHA_PROVIDER_MAX_COST_USD",
        "ALPHA_PROVIDER_MAX_INPUT_TOKENS",
        "ALPHA_PROVIDER_MAX_OUTPUT_TOKENS",
        "ALPHA_PROVIDER_MAX_REQUESTS",
    ):
        monkeypatch.setenv(env, "5")
    _login(client)
    dr = _dry_run(client)
    assert dr["dry_run_execution"] == "not_enabled"
    summary = dr["provider_gate_summary"]
    assert summary["cap_completeness"] == "configured"
    assert summary["provider_key_status"] == "present"
    assert summary["live_execution_gate"] == "blocked"
    assert "provider_live_execution_blocked" in dr["preview_blockers"]
    assert "display_only_lane" in dr["preview_blockers"]


# 20. Fake API keys never appear in HTML, JSON, or reprs with the panel present.
def test_dry_run_fake_secret_never_leaks(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", FAKE_SECRET)
    _write_all_four(tmp_path)
    _use_root(monkeypatch, tmp_path)
    _login(client)
    assert FAKE_SECRET not in client.get(PAGE_ROUTE).text
    assert FAKE_SECRET not in client.get(STATUS_ROUTE).text
    assert FAKE_SECRET not in repr(operator_console.build_console_status())


# 21. Raw prompt/baseline/routed/route-metadata/system-prompt/provider-payload
#     sentinels never appear in HTML or JSON.
def test_dry_run_raw_sentinels_never_leak(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    capture = _capture_with_sensitive_metadata()
    _write(tmp_path, "capture.json", capture)
    _write(
        tmp_path, "evidence_packet.json", capture_lib.build_evidence_packet(capture)
    )
    _write(tmp_path, "anchor_preflight_report.json", _anchor_report())
    _write(tmp_path, "lift_preflight_report.json", _lift_report())
    _use_root(monkeypatch, tmp_path)
    _login(client)
    html_text = client.get(PAGE_ROUTE).text
    body = client.get(STATUS_ROUTE).text
    for raw in (
        RAW_PROMPT,
        RAW_BASELINE,
        RAW_ROUTED,
        RAW_ROUTE_META,
        RAW_SYS_PROMPT,
        RAW_PROVIDER_PAYLOAD,
    ):
        assert raw not in html_text
        assert raw not in body


# 22. Provider client constructors patched to raise still allow both routes.
def test_dry_run_provider_client_patched_raise_routes_ok(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    import alpha.providers.openai as openai_provider

    def _boom(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("provider client must not be used by operator console")

    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "__init__", _boom)
    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "execute", _boom)
    _write_all_four(tmp_path)
    _use_root(monkeypatch, tmp_path)
    _login(client)
    assert client.get(PAGE_ROUTE).status_code == 200
    assert client.get(STATUS_ROUTE).status_code == 200


# 23. Source-scan: no provider client / httpx / requests / subprocess / socket /
#     browser / MCP / CLI / solve imports are introduced in the route module.
def test_dry_run_console_route_has_no_execution_or_solve_imports() -> None:
    source = Path(operator_console.__file__).read_text(encoding="utf-8")
    import_lines = [
        line
        for line in source.splitlines()
        if line.strip().startswith(("import ", "from "))
    ]
    joined = "\n".join(import_lines).lower()
    for token in (
        "solve",
        "provider",
        "mcp",
        "httpx",
        "requests",
        "subprocess",
        "socket",
        "urllib",
        "playwright",
        "selenium",
        "webdriver",
        "webbrowser",
        "pexpect",
        "openai",
        "anthropic",
    ):
        assert token not in joined, token


# 24. UI text contains the dry-run preview boundary text.
def test_dry_run_boundary_text_in_ui(client: TestClient) -> None:
    _login(client)
    html_text = client.get(PAGE_ROUTE).text
    for text in operator_console.DRY_RUN_BOUNDARY_TEXTS:
        assert text in html_text
    assert operator_console.DRY_RUN_BOUNDARY_NOTE in html_text


# 25. UI does not contain misleading dry-run execution/claim language.
def test_dry_run_no_misleading_execution_language(client: TestClient) -> None:
    _login(client)
    card = _dry_run_card_html(client.get(PAGE_ROUTE).text).lower()
    for forbidden in (
        "run now",
        "execute now",
        "submit to provider",
        "generate answer",
        "solve now",
        "start solve",
        "production ready",
        "ready for production",
        "estimated spend",
        "estimated cost",
        "winner",
        "leaderboard",
        "outperforms",
        "model comparison",
    ):
        assert forbidden not in card, forbidden


# 26/27. Existing provider gate, artifact status, and freshness surfaces persist
#        alongside the dry-run preview panel.
def test_dry_run_preview_coexists_with_existing_sections(client: TestClient) -> None:
    _login(client)
    payload = client.get(STATUS_ROUTE).json()
    for section in (
        "console",
        "portable_contract",
        "run_setup",
        "route_trace",
        "provider_gate",
        "dry_run_preview",
        "preflight_capture",
        "evidence_receipt",
        "local_artifacts",
    ):
        assert section in payload
    assert payload["provider_gate"]["live_execution_gate"] == "blocked"
    local = payload["local_artifacts"]
    assert "freshness" in local
    assert "status_generated_at_utc" in local
    html_text = client.get(PAGE_ROUTE).text
    for card_id in ("card-provider-gate", "card-dry-run-preview", "card-evidence-receipt"):
        assert card_id in html_text

# ---------------------------------------------------------------------------
# Local Receipt Store
# (AOC-B006-LOCAL-RECEIPT-STORE-001 /
# UI-ALPHA-OPERATOR-CONSOLE-LOCAL-RECEIPT-STORE-001). Receipts are safe local
# audit snapshots only: one protected POST creates one JSON receipt under the
# safe artifact root and stores only whitelisted status summaries.
# ---------------------------------------------------------------------------
RAW_SYSTEM_PROMPT = "RAW-SYSTEM-PROMPT-must-not-render-zzz"
RAW_PROVIDER_PAYLOAD = "RAW-PROVIDER-PAYLOAD-must-not-render-zzz"
RAW_ENV_SENTINEL = "RAW-ENV-SENTINEL-must-not-render-zzz"
PARTIAL_KEY = FAKE_SECRET[:12]


def _csrf_headers(client: TestClient) -> dict[str, str]:
    token = client.cookies.get(auth.CSRF_COOKIE_NAME)
    assert token
    return {auth.CSRF_HEADER_NAME: token}


def _repo_receipt_root(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    repo_root = Path(artifacts.__file__).resolve().parents[2]
    rel = Path("local") / f"receipt-tests-{tmp_path.name}"
    root = repo_root / rel
    if root.exists():
        for path in sorted(root.rglob("*"), reverse=True):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                path.rmdir()
        root.rmdir()
    root.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv(artifacts.ARTIFACT_ROOT_ENV, rel.as_posix())
    return root / "receipts"


def _receipt_files(root: Path) -> list[Path]:
    return sorted(root.glob("*.json")) if root.exists() else []


def _post_receipt(client: TestClient, **kwargs: object):
    return client.post(
        RECEIPTS_ROUTE,
        headers=_csrf_headers(client),
        follow_redirects=False,
        **kwargs,
    )


def test_receipt_status_section_empty_and_safe_label(client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    _repo_receipt_root(monkeypatch, tmp_path)
    _login(client)
    store = client.get(STATUS_ROUTE).json()["local_receipts"]
    assert store["enabled"] is True
    assert store["create_receipt_endpoint"] == RECEIPTS_ROUTE
    assert store["count"] == 0
    assert "missing_dir" in store["states"] or "empty" in store["states"]
    assert store["receipt_root"].startswith("local/")
    assert store["receipt_root"].endswith("/receipts")
    assert not Path(store["receipt_root"]).is_absolute()


def test_receipt_page_empty_renders_normally(client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    _repo_receipt_root(monkeypatch, tmp_path)
    _login(client)
    html_text = client.get(PAGE_ROUTE).text
    assert "Local Receipt Store" in html_text
    assert "Save local receipt snapshot" in html_text
    assert "No local receipts saved yet." in html_text


def test_receipt_post_route_is_protected() -> None:
    paths = {
        (getattr(route, "path", None), tuple(sorted(getattr(route, "methods", set()) or set())))
        for route in app.routes
    }
    assert (RECEIPTS_ROUTE, ("POST",)) in paths


def test_unauthenticated_receipt_post_matches_protected_behavior(client: TestClient) -> None:
    response = client.post(RECEIPTS_ROUTE, follow_redirects=False)
    assert response.status_code == 401
    assert response.json()["detail"] == "not authenticated"


def test_authenticated_receipt_post_requires_csrf(client: TestClient) -> None:
    _login(client)
    response = client.post(RECEIPTS_ROUTE, follow_redirects=False)
    assert response.status_code == 403
    assert response.json()["detail"] == "missing CSRF token"


def test_receipt_post_creates_one_file_with_schema_and_digest(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = _repo_receipt_root(monkeypatch, tmp_path)
    _login(client)
    response = _post_receipt(client)
    assert response.status_code == 303
    assert response.headers["location"] == PAGE_ROUTE
    files = _receipt_files(root)
    assert len(files) == 1
    receipt = json.loads(files[0].read_text(encoding="utf-8"))
    assert receipt["schema_version"] == receipts.RECEIPT_SCHEMA_VERSION
    assert receipt["content_digest"].startswith("sha256:")
    body = {key: value for key, value in receipt.items() if key != "content_digest"}
    assert receipts.digest_receipt_body(body) == receipt["content_digest"]
    assert receipt["receipt_id"] in files[0].name
    assert files[0].suffix == ".json"
    assert "/" not in receipt["receipt_id"] and "\\" not in receipt["receipt_id"]
    assert len(receipt["receipt_id"]) <= 40


def test_receipt_post_ignores_user_path_and_body(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = _repo_receipt_root(monkeypatch, tmp_path)
    _login(client)
    response = _post_receipt(
        client,
        params={"path": "/tmp/evil", "receipt_id": "../evil"},
        json={"filename": "evil.json", "receipt_id": "evil", "snapshot": {"raw": RAW_PROMPT}},
    )
    assert response.status_code == 303
    files = _receipt_files(root)
    assert len(files) == 1
    text = files[0].read_text(encoding="utf-8")
    assert "evil" not in files[0].name
    assert "/tmp/evil" not in text
    assert RAW_PROMPT not in text


def test_receipt_outside_root_override_rejected_for_write(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    outside = tmp_path / "outside"
    monkeypatch.setenv(artifacts.ARTIFACT_ROOT_ENV, str(outside))
    _login(client)
    response = _post_receipt(client)
    assert response.status_code == 303
    assert not outside.exists()
    assert receipts.receipt_root() == artifacts.DEFAULT_ARTIFACT_ROOT / "receipts"


def test_receipt_inside_root_override_writes_under_safe_root(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = _repo_receipt_root(monkeypatch, tmp_path)
    _login(client)
    assert _post_receipt(client).status_code == 303
    files = _receipt_files(root)
    assert len(files) == 1
    assert files[0].resolve().is_relative_to(root.resolve())


def test_receipt_snapshot_safe_whitelist_no_raw_or_runtime_output(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = _repo_receipt_root(monkeypatch, tmp_path)
    capture_root = root.parent
    _write_all_four(capture_root)
    monkeypatch.setenv("OPENAI_API_KEY", FAKE_SECRET)
    monkeypatch.setenv("RAW_ENV_TEST_SENTINEL", RAW_ENV_SENTINEL)
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    _login(client)
    assert _post_receipt(client).status_code == 303
    receipt_text = _receipt_files(root)[0].read_text(encoding="utf-8")
    receipt = json.loads(receipt_text)
    snapshot = receipt["snapshot"]
    gate = snapshot["provider_gate"]
    assert gate["key_status"]["OPENAI_API_KEY"] == "present"
    assert gate["provider_key_status"] == "present"
    assert snapshot["dry_run_preview"]["dry_run_execution"] == "not_enabled"
    assert snapshot["route_trace"]["route"] == "not run yet"
    assert snapshot["route_trace"]["confidence"] == "not run yet"
    assert snapshot["route_trace"]["safe_out_state"] == "not run yet"
    assert snapshot["local_artifacts"]["capture"]["route_metadata_present_count"] == 1
    assert snapshot["local_artifacts"]["evidence_packet"]["content_digest"].startswith("sha256:")
    forbidden = (
        RAW_PROMPT,
        RAW_BASELINE,
        RAW_ROUTED,
        RAW_ROUTE_META,
        RAW_SYSTEM_PROMPT,
        RAW_PROVIDER_PAYLOAD,
        FAKE_SECRET,
        PARTIAL_KEY,
        RAW_ENV_SENTINEL,
        "generated answer",
    )
    for token in forbidden:
        assert token not in receipt_text


def test_receipt_save_does_not_leak_raw_in_status_or_html(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = _repo_receipt_root(monkeypatch, tmp_path)
    _write_all_four(root.parent)
    monkeypatch.setenv("OPENAI_API_KEY", FAKE_SECRET)
    _login(client)
    assert _post_receipt(client).status_code == 303
    html_text = client.get(PAGE_ROUTE).text
    status_text = client.get(STATUS_ROUTE).text
    for token in (RAW_PROMPT, RAW_BASELINE, RAW_ROUTED, RAW_ROUTE_META, RAW_PROVIDER_PAYLOAD, FAKE_SECRET):
        assert token not in html_text
        assert token not in status_text


def test_recent_receipt_summary_in_status_and_page_without_full_body(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = _repo_receipt_root(monkeypatch, tmp_path)
    _login(client)
    assert _post_receipt(client).status_code == 303
    receipt = json.loads(_receipt_files(root)[0].read_text(encoding="utf-8"))
    status = client.get(STATUS_ROUTE).json()
    recent = status["local_receipts"]["recent"]
    assert status["local_receipts"]["count"] == 1
    assert recent[0]["receipt_id"] == receipt["receipt_id"]
    assert "snapshot" not in recent[0]
    html_text = client.get(PAGE_ROUTE).text
    assert receipt["receipt_id"] in html_text
    assert receipt["content_digest"] in html_text
    assert RAW_PROMPT not in html_text
    assert RAW_BASELINE not in html_text


def test_corrupt_receipt_fails_safe(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = _repo_receipt_root(monkeypatch, tmp_path)
    root.mkdir(parents=True)
    (root / "corrupt.json").write_text("{not json", encoding="utf-8")
    _login(client)
    assert client.get(STATUS_ROUTE).status_code == 200
    assert client.get(PAGE_ROUTE).status_code == 200
    store = client.get(STATUS_ROUTE).json()["local_receipts"]
    assert "invalid_entries" in store["states"]
    assert store["recent"][0]["state"] == "invalid"


def test_multiple_receipts_newest_first_with_limit(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _repo_receipt_root(monkeypatch, tmp_path)
    _login(client)
    for _ in range(7):
        assert _post_receipt(client).status_code == 303
    recent = client.get(STATUS_ROUTE).json()["local_receipts"]["recent"]
    assert len(recent) == 5
    created = [item["created_at_utc"] for item in recent]
    assert created == sorted(created, reverse=True)


def test_receipt_creation_does_not_mutate_existing_operator_artifacts(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = _repo_receipt_root(monkeypatch, tmp_path)
    artifact_root = root.parent
    _write_all_four(artifact_root)
    names = [
        "capture.json",
        "evidence_packet.json",
        "anchor_preflight_report.json",
        "lift_preflight_report.json",
    ]
    before = {name: (artifact_root / name).read_bytes() for name in names}
    _login(client)
    assert _post_receipt(client).status_code == 303
    after = {name: (artifact_root / name).read_bytes() for name in names}
    assert after == before


def test_provider_client_patched_raise_receipts_ok(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    import alpha.providers.openai as openai_provider

    def _boom(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("provider client must not be used by receipts")

    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "__init__", _boom)
    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "execute", _boom)
    _repo_receipt_root(monkeypatch, tmp_path)
    _login(client)
    assert client.get(PAGE_ROUTE).status_code == 200
    assert client.get(STATUS_ROUTE).status_code == 200
    assert _post_receipt(client).status_code == 303


def test_no_execution_imports_in_receipt_sources() -> None:
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
        "from alpha.providers",
        "import alpha.providers",
        "internal_solve",
    )
    for module in (operator_console, receipts):
        source = Path(module.__file__).read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in source, f"{token!r} found in {module.__file__}"


def test_receipt_ui_boundary_text_and_no_misleading_receipt_language(client: TestClient) -> None:
    _login(client)
    html_text = client.get(PAGE_ROUTE).text
    for text in receipts.RECEIPT_BOUNDARY_TEXTS:
        assert text in html_text
    receipt_card = html_text.split('id="card-local-receipt-store"', 1)[1].split('id="card-evidence-receipt"', 1)[0]
    for forbidden in (
        "Run receipt",
        "Execute",
        "Solve",
        "Submit to provider",
        "Generate answer",
        "Validate",
        "Benchmark",
        "production ready",
        "winner",
        "estimated spend",
    ):
        assert forbidden not in receipt_card

# ---------------------------------------------------------------------------
# ChatGPT Copy/Paste Capture panel (manual-only guidance)
# ---------------------------------------------------------------------------

def _chatgpt_capture_status(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict:
    _use_root(monkeypatch, tmp_path)
    return operator_console.build_console_status()["chatgpt_copy_paste_capture"]


def _pending_capture() -> dict:
    packet = {"packet_id": "ORC-PENDING-001", "cases": [{"task_id": "t1", "prompt": RAW_PROMPT}]}
    return capture_lib.scaffold_capture(packet)


def _all_excluded_capture() -> dict:
    capture = _pending_capture()
    capture["cases"][0]["validation_status"] = "excluded"
    capture["cases"][0]["exclusion_reason"] = "manual exclusion"
    return capture


def test_chatgpt_copy_paste_status_defaults_manual_only(client: TestClient) -> None:
    _login(client)
    payload = client.get(STATUS_ROUTE).json()
    section = payload["chatgpt_copy_paste_capture"]
    assert section["mode"] == "manual_only"
    assert section["automation"] == "disabled"
    assert section["browser_automation"] == "disabled"
    assert section["provider_calls"] == "disabled"
    assert section["live_execution"] == "disabled"
    assert section["console_writes_capture"] is False
    assert section["console_stores_pasted_outputs"] is False


def test_chatgpt_missing_capture_stage_and_steps(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    section = _chatgpt_capture_status(tmp_path, monkeypatch)
    assert section["current_capture_stage"] == "no_capture"
    assert section["next_manual_steps"] == [
        "author_case_packet",
        "run_anchor_preflight_from_terminal",
        "scaffold_capture_from_terminal",
    ]


def test_chatgpt_invalid_capture_stage_and_steps(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "capture.json").write_text("{ nope", encoding="utf-8")
    section = _chatgpt_capture_status(tmp_path, monkeypatch)
    assert section["current_capture_stage"] == "capture_invalid"
    assert "validate_capture_from_terminal" in section["next_manual_steps"]


def test_chatgpt_pending_capture_stage_from_safe_counts(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _write(tmp_path, "capture.json", _pending_capture())
    section = _chatgpt_capture_status(tmp_path, monkeypatch)
    assert section["current_capture_stage"] == "capture_scaffolded"
    assert "paste_outputs_into_capture_file" in section["next_manual_steps"]


def test_chatgpt_in_progress_capture_stage_from_safe_counts(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    packet = {
        "packet_id": "ORC-INPROGRESS-001",
        "cases": [
            {"task_id": "t1", "prompt": RAW_PROMPT},
            {"task_id": "t2", "prompt": RAW_PROMPT},
        ],
    }
    capture = capture_lib.scaffold_capture(packet)
    capture["cases"][1]["validation_status"] = "excluded"
    capture["cases"][1]["exclusion_reason"] = "manual exclusion"
    _write(tmp_path, "capture.json", capture)
    section = _chatgpt_capture_status(tmp_path, monkeypatch)
    assert section["current_capture_stage"] == "capture_in_progress"
    assert "finish_pending_capture_slots" in section["next_manual_steps"]


def test_chatgpt_all_excluded_capture_stage_and_steps_safe(
    client: TestClient, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _write(tmp_path, "capture.json", _all_excluded_capture())
    _use_root(monkeypatch, tmp_path)
    _login(client)
    payload = client.get(STATUS_ROUTE).json()
    section = payload["chatgpt_copy_paste_capture"]
    assert section["current_capture_stage"] == "capture_all_excluded"
    assert "finish_pending_capture_slots" not in section["next_manual_steps"]
    assert "add_at_least_one_captured_case" in section["next_manual_steps"]
    assert "revise_case_packet_or_capture_file" in section["next_manual_steps"]

    html_text = client.get(PAGE_ROUTE).text
    body = json.dumps(section)
    for raw in (
        RAW_PROMPT,
        RAW_BASELINE,
        RAW_ROUTED,
        RAW_ROUTE_META,
        RAW_SYSTEM_PROMPT,
        RAW_PROVIDER_PAYLOAD,
        FAKE_SECRET,
    ):
        assert raw not in body
        assert raw not in html_text


def test_chatgpt_export_ready_and_evidence_packet_stages(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    capture = _valid_capture()
    _write(tmp_path, "capture.json", capture)
    section = _chatgpt_capture_status(tmp_path, monkeypatch)
    assert section["current_capture_stage"] == "capture_export_ready"

    _write(tmp_path, "evidence_packet.json", capture_lib.build_evidence_packet(capture))
    section = _chatgpt_capture_status(tmp_path, monkeypatch)
    assert section["current_capture_stage"] == "evidence_packet_available"
    assert section["next_manual_steps"] == ["save_local_receipt_snapshot"]


def test_chatgpt_stage_derived_only_from_safe_summary(monkeypatch: pytest.MonkeyPatch) -> None:
    local = {
        "capture": {"state": "structurally_valid", "counts": {"captured": 0, "excluded": 0, "pending": 2}},
        "evidence_packet": {"state": "missing"},
    }
    assert operator_console._chatgpt_capture_stage(local) == "capture_scaffolded"
    local["capture"] = {"state": "structurally_valid", "counts": {"captured": 1, "excluded": 0, "pending": 1}}
    assert operator_console._chatgpt_capture_stage(local) == "capture_in_progress"
    local["capture"] = {"state": "structurally_valid", "counts": {"captured": 0, "excluded": 2, "pending": 0}}
    assert operator_console._chatgpt_capture_stage(local) == "capture_all_excluded"
    local["evidence_packet"] = {"state": "digest_valid"}
    assert operator_console._chatgpt_capture_stage(local) == "evidence_packet_available"


def test_chatgpt_checklist_template_and_commands_are_safe(client: TestClient) -> None:
    _login(client)
    payload = client.get(STATUS_ROUTE).json()
    section = payload["chatgpt_copy_paste_capture"]
    assert "copy_paste_checklist" in section
    assert "collect_plain_chatgpt_output_manually" in section["copy_paste_checklist"]
    template = section["capture_slot_template"]
    assert template["task_id"] == "<task_id>"
    assert "<paste plain ChatGPT output into local capture file>" in template.values()
    assert all("python scripts/operator_run_capture.py" in c["command"] for c in section["terminal_commands"])
    assert client.get(PAGE_ROUTE).status_code == 200
    html_text = client.get(PAGE_ROUTE).text
    assert html.escape("<task_id>") in html_text
    assert "Terminal command snippets (text only; not executed)" in html_text
    body = json.dumps(section)
    for raw in (RAW_PROMPT, RAW_BASELINE, RAW_ROUTED, RAW_ROUTE_META, RAW_SYSTEM_PROMPT, RAW_PROVIDER_PAYLOAD, FAKE_SECRET):
        assert raw not in body
        assert raw not in html_text


def test_chatgpt_ui_boundary_route_metadata_and_buttons(client: TestClient) -> None:
    _login(client)
    html_text = client.get(PAGE_ROUTE).text
    assert "card-chatgpt-copy-paste-capture" in html_text
    for text in operator_console.CHATGPT_CAPTURE_BOUNDARY_TEXTS:
        assert text in html_text
    for label in operator_console.CHATGPT_CAPTURE_ROUTE_METADATA_GUIDANCE:
        assert label in html_text
    assert "no_scoring" in html_text
    assert "no_rank_ordering" in html_text
    assert "no_selected_output" in html_text
    assert "no_quality_judgment" in html_text
    assert "no_readiness_or_benchmark_claim" in html_text
    assert "Live run (disabled)" in html_text
    button_text = " ".join(__import__("re").findall(r"<button[^>]*>(.*?)</button>", html_text, flags=__import__("re").S))
    for forbidden in ("Run", "Execute", "Solve", "Submit to provider", "Generate", "Validate", "Benchmark", "Start", "Automate"):
        if forbidden == "Run":
            assert "Live run (disabled)" in button_text
        else:
            assert forbidden not in button_text


def test_chatgpt_no_new_post_route_and_receipt_route_unchanged() -> None:
    post_paths = {getattr(route, "path", None) for route in app.routes if "POST" in getattr(route, "methods", set())}
    assert RECEIPTS_ROUTE in post_paths
    assert not any("copy" in str(path).lower() or "paste" in str(path).lower() for path in post_paths)


def test_chatgpt_provider_client_patched_raise_routes_ok(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    import alpha.providers.openai as openai_provider

    def _boom(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("provider client must not be used by operator console")

    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "__init__", _boom)
    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "execute", _boom)
    _login(client)
    assert client.get(PAGE_ROUTE).status_code == 200
    assert client.get(STATUS_ROUTE).status_code == 200


def test_chatgpt_source_scan_no_execution_imports() -> None:
    source = Path(operator_console.__file__).read_text(encoding="utf-8")
    import_lines = [line for line in source.splitlines() if line.strip().startswith(("import ", "from "))]
    joined = "\n".join(import_lines).lower()
    for token in ("chatgpt", "provider", "mcp", "httpx", "requests", "subprocess", "socket", "urllib", "playwright", "selenium", "webdriver", "webbrowser", "pexpect", "solve"):
        assert token not in joined, token

# ---------------------------------------------------------------------------
# PROCESS-HARDENING-NO-PROVIDER-CALL-TEST-HELPER-001
# ---------------------------------------------------------------------------
def test_operator_console_safety_helper_negative_controls(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Canaries prove the reusable guard fails on forbidden actions."""

    with operator_console_no_execution_guard(monkeypatch):
        with pytest.raises(OperatorConsoleSafetyViolation):
            sock = socket.socket()
            try:
                sock.connect(("203.0.113.10", 443))
            finally:
                sock.close()
        with pytest.raises(OperatorConsoleSafetyViolation):
            subprocess.run(["python", "-c", "print('must-not-run')"], check=False)
        with pytest.raises(OperatorConsoleSafetyViolation):
            os.system("echo must-not-run")
        with pytest.raises(OperatorConsoleSafetyViolation):
            os.popen("echo must-not-run")
        with pytest.raises(OperatorConsoleSafetyViolation):
            os.spawnv(os.P_WAIT, "/bin/echo", ["echo", "must-not-run"])

    with operator_console_no_get_write_guard(monkeypatch):
        with pytest.raises(OperatorConsoleSafetyViolation):
            (tmp_path / "unauthorized.txt").write_text("must-not-write", encoding="utf-8")
        with pytest.raises(OperatorConsoleSafetyViolation):
            open(tmp_path / "unauthorized-open.txt", "w", encoding="utf-8")
        with pytest.raises(OperatorConsoleSafetyViolation):
            (tmp_path / "unauthorized-path-open.txt").open("x", encoding="utf-8")


def test_operator_console_provider_and_model_canaries_raise(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Canaries prove provider/model guard patch points are effective."""

    import alpha.providers.openai as openai_provider

    def _boom(*_args: object, **_kwargs: object) -> None:
        raise OperatorConsoleSafetyViolation("blocked provider/model invocation")

    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "__init__", _boom)
    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "execute", _boom)
    monkeypatch.setattr(app.state, "provider_client_factory", _boom, raising=False)

    with pytest.raises(OperatorConsoleSafetyViolation):
        app.state.provider_client_factory()
    with pytest.raises(OperatorConsoleSafetyViolation):
        openai_provider.OpenAIProviderClient()


def test_operator_console_v1_solve_canary_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """Canary proves a mocked /v1/solve invocation is observable by guard tests."""

    import service.app as service_app

    async def _boom(*_args: object, **_kwargs: object) -> None:
        raise OperatorConsoleSafetyViolation("blocked /v1/solve invocation")

    route = next(route for route in app.routes if getattr(route, "path", None) == "/v1/solve")
    monkeypatch.setattr(service_app, "solve", _boom)
    monkeypatch.setattr(route, "endpoint", _boom)
    monkeypatch.setattr(route.dependant, "call", _boom)
    with pytest.raises(OperatorConsoleSafetyViolation):
        import anyio

        anyio.run(service_app.solve, object(), object())
    with pytest.raises(OperatorConsoleSafetyViolation):
        import anyio

        anyio.run(route.endpoint, object(), object())
    with pytest.raises(OperatorConsoleSafetyViolation):
        import anyio

        anyio.run(route.dependant.call, object(), object())


def test_operator_console_render_status_under_reusable_safety_guard(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """GET render/status paths stay inside no-execution and no-write guards."""

    import alpha.providers.openai as openai_provider
    import service.app as service_app

    def _blocked(*_args: object, **_kwargs: object) -> None:
        raise OperatorConsoleSafetyViolation("blocked execution boundary")

    async def _blocked_solve(*_args: object, **_kwargs: object) -> None:
        raise OperatorConsoleSafetyViolation("blocked /v1/solve boundary")

    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "__init__", _blocked)
    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "execute", _blocked)
    monkeypatch.setattr(app.state, "provider_client_factory", _blocked, raising=False)
    solve_route = next(route for route in app.routes if getattr(route, "path", None) == "/v1/solve")
    monkeypatch.setattr(service_app, "solve", _blocked_solve)
    monkeypatch.setattr(solve_route, "endpoint", _blocked_solve)
    monkeypatch.setattr(solve_route.dependant, "call", _blocked_solve)

    _login(client)
    with operator_console_no_execution_guard(monkeypatch), operator_console_no_get_write_guard(monkeypatch):
        page = client.get(PAGE_ROUTE)
        status = client.get(STATUS_ROUTE)

    assert page.status_code == 200
    assert status.status_code == 200
    payload = status.json()
    assert payload["provider_gate"]["console_calls_providers"] is False
    assert payload["run_setup"]["live_run_button_enabled"] is False
    assert payload["provider_gate"]["live_provider_calls"] == "disabled"
    assert payload["dry_run_preview"]["dry_run_execution"] == "not_enabled"
    assert payload["chatgpt_copy_paste_capture"]["console_stores_pasted_outputs"] is False


def test_operator_console_import_tree_under_safety_guard(monkeypatch: pytest.MonkeyPatch) -> None:
    """Import/reload of console modules must not start providers, network, solve, or subprocesses."""

    import alpha.providers.openai as openai_provider
    import service.app as service_app

    def _blocked(*_args: object, **_kwargs: object) -> None:
        raise OperatorConsoleSafetyViolation("blocked import-time execution boundary")

    async def _blocked_solve(*_args: object, **_kwargs: object) -> None:
        raise OperatorConsoleSafetyViolation("blocked import-time /v1/solve boundary")

    monkeypatch.setattr(openai_provider.OpenAIProviderClient, "__init__", _blocked)
    monkeypatch.setattr(app.state, "provider_client_factory", _blocked, raising=False)
    solve_route = next(route for route in app.routes if getattr(route, "path", None) == "/v1/solve")
    monkeypatch.setattr(service_app, "solve", _blocked_solve)
    monkeypatch.setattr(solve_route, "endpoint", _blocked_solve)
    monkeypatch.setattr(solve_route.dependant, "call", _blocked_solve)

    with operator_console_no_execution_guard(monkeypatch), operator_console_no_get_write_guard(monkeypatch):
        importlib.reload(artifacts)
        importlib.reload(receipts)
        importlib.reload(operator_console)


def test_operator_console_write_chokepoint_source_allowlist() -> None:
    """Operator Console writes remain limited to the authorized receipt helper."""

    modules = (artifacts, operator_console, receipts)
    allowed_write_calls = {
        (Path(receipts.__file__).resolve(), "mkdir"),
        (Path(receipts.__file__).resolve(), "open"),
        (Path(receipts.__file__).resolve(), "write_text"),
    }
    violations: list[str] = []
    for module in modules:
        module_path = Path(module.__file__).resolve()
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = ""
                if isinstance(node.func, ast.Attribute):
                    name = node.func.attr
                elif isinstance(node.func, ast.Name):
                    name = node.func.id
                if name == "open":
                    if isinstance(node.func, ast.Attribute):
                        mode_arg = node.args[0] if node.args else None
                    else:
                        mode_arg = node.args[1] if len(node.args) > 1 else None
                    mode_keyword = next((kw.value for kw in node.keywords if kw.arg == "mode"), None)
                    mode_node = mode_keyword or mode_arg
                    mode = mode_node.value if isinstance(mode_node, ast.Constant) else "r"
                    if any(flag in str(mode) for flag in ("w", "a", "x", "+")):
                        if (module_path, name) not in allowed_write_calls:
                            violations.append(f"{module_path}:{node.lineno}: open({mode!r})")
                if name in {"write_text", "write_bytes", "mkdir", "dump"}:
                    if (module_path, name) not in allowed_write_calls:
                        violations.append(f"{module_path}:{node.lineno}: {name}")

    assert violations == []


def test_operator_console_no_user_supplied_write_path_parameters() -> None:
    """Receipt creation remains pathless from the request surface."""

    route = next(route for route in app.routes if getattr(route, "path", None) == RECEIPTS_ROUTE)
    dependant_names = [param.name for param in getattr(route, "dependant").body_params]
    dependant_names += [param.name for param in getattr(route, "dependant").query_params]
    assert dependant_names == []

# ---------------------------------------------------------------------------
# UI-ALPHA-OPERATOR-CONSOLE-MANUAL-NEXT-STEP-GUIDE-001
# ---------------------------------------------------------------------------
def _manual_next_step_card_html(html_text: str) -> str:
    start = html_text.index('id="card-manual-next-step-guide"')
    end = html_text.index("</article>", start)
    return html_text[start:end]


def test_manual_next_step_guide_status_payload(client: TestClient) -> None:
    _login(client)
    payload = client.get(STATUS_ROUTE).json()
    assert "manual_next_step_guide" in payload
    guide = payload["manual_next_step_guide"]
    assert guide["title"] == "Manual Next Step Guide"
    assert guide["mode"] == "display_only"
    assert guide["execution"] == "non_executing"
    assert guide["sections"] == [
        "Available for review",
        "Manual-only steps",
        "Blocked in this console",
    ]
    assert {item["section"] for item in guide["items"]} == set(guide["sections"])
    assert "Provider calls blocked." in guide["boundary_notes"]


def test_manual_next_step_guide_card_copy_and_sections(client: TestClient) -> None:
    _login(client)
    card = _manual_next_step_card_html(client.get(PAGE_ROUTE).text)
    for required in (
        "Manual Next Step Guide",
        "Available for review",
        "Manual-only steps",
        "Blocked in this console",
        "display-only",
        "Provider calls blocked",
        "Local Receipt Store only",
    ):
        assert required in card
    assert "manual-only" in card.lower()
    assert "does not run providers" in card
    assert "does not call /v1/solve" in card
    assert "does not accept prompt input or store pasted model output" in card


def test_manual_next_step_guide_has_no_action_controls(client: TestClient) -> None:
    _login(client)
    card = _manual_next_step_card_html(client.get(PAGE_ROUTE).text)
    assert "<button" not in card
    assert "<form" not in card
    assert "<textarea" not in card
    assert "method=\"post\"" not in card.lower()
    control_fragments = (
        "run selected",
        "dispatch",
        "submit",
        "send",
        "process",
        "retry",
        "schedule",
        "approve",
    )
    lowered = card.lower()
    for word in control_fragments:
        assert f">{word}<" not in lowered, word
        assert f'aria-label="{word}"' not in lowered, word
        assert f'value="{word}"' not in lowered, word


def test_manual_next_step_guide_no_new_post_route_and_receipt_only() -> None:
    post_paths = {
        getattr(route, "path", None)
        for route in app.routes
        if "POST" in getattr(route, "methods", set())
        and str(getattr(route, "path", "")).startswith("/dashboard/operator-console")
    }
    assert post_paths == {RECEIPTS_ROUTE}


def test_manual_next_step_guide_no_raw_or_secret_leak(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", FAKE_SECRET)
    capture = _capture_with_sensitive_metadata()
    _write(tmp_path, "capture.json", capture)
    _write(tmp_path, "evidence_packet.json", capture_lib.build_evidence_packet(capture))
    _use_root(monkeypatch, tmp_path)
    _login(client)
    status_text = client.get(STATUS_ROUTE).text
    card = _manual_next_step_card_html(client.get(PAGE_ROUTE).text)
    for raw in (
        RAW_PROMPT,
        RAW_BASELINE,
        RAW_ROUTED,
        RAW_ROUTE_META,
        RAW_SYS_PROMPT,
        RAW_PROVIDER_PAYLOAD,
        FAKE_SECRET,
        "sk-",
    ):
        assert raw not in status_text
        assert raw not in card


def test_manual_next_step_guide_preserves_existing_boundaries(client: TestClient) -> None:
    _login(client)
    payload = client.get(STATUS_ROUTE).json()
    assert payload["provider_gate"]["live_execution_gate"] == "blocked"
    assert payload["provider_gate"]["live_provider_calls"] == "disabled"
    assert payload["dry_run_preview"]["preview_mode"] == "display_only"
    assert payload["dry_run_preview"]["dry_run_execution"] == "not_enabled"
    assert payload["chatgpt_copy_paste_capture"]["mode"] == "manual_only"
    assert payload["chatgpt_copy_paste_capture"]["console_stores_pasted_outputs"] is False
    assert payload["run_setup"]["live_run_button_enabled"] is False
    assert payload["route_trace"]["note"] == "No solve has run from this console; fields are placeholders."


def test_manual_next_step_guide_forbidden_claim_language_absent(client: TestClient) -> None:
    _login(client)
    card = _manual_next_step_card_html(client.get(PAGE_ROUTE).text).lower()
    for forbidden in (
        "safe action queue",
        "action queue",
        "task queue",
        "job queue",
        "worker",
        "run selected",
        "schedule",
        "retry",
        "priority",
        "winner",
        "score",
        "rank",
        "production-ready",
        "benchmark passed",
        "validated output",
        "readiness",
        "superiority",
    ):
        assert forbidden not in card, forbidden


def test_manual_next_step_guide_under_reusable_safety_guard(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _login(client)
    with operator_console_no_execution_guard(monkeypatch), operator_console_no_get_write_guard(monkeypatch):
        page = client.get(PAGE_ROUTE)
        status = client.get(STATUS_ROUTE)
    assert page.status_code == 200
    assert status.status_code == 200
    assert "Manual Next Step Guide" in page.text
    assert "manual_next_step_guide" in status.json()
