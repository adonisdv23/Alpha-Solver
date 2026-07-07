"""Read-only Alpha Solver Operator Console shell.

This module renders a protected, local-first operator cockpit made of status
cards. It exposes contract/status information for the operator and clearly
marks every not-yet-wired surface. It intentionally does **not** enable live
API execution:

* No provider client is imported, instantiated, or called here.
* No network, model, MCP, tool, or browser call is made.
* Status is assembled only from configuration and environment *presence*.

Secret handling: key status is boolean/categorical only. Raw environment values
(API keys, secrets) are never returned by the JSON endpoint and never rendered
in HTML. Only ``present`` / ``missing`` / ``unknown`` categories are surfaced.

The console is mounted behind the shared dashboard auth/CSRF middleware (see
``alpha/webapp/routes/auth.py``) under the protected ``/dashboard`` prefix, so
it is fail-closed: it is only reachable when the dashboard is enabled with a
non-default password and an explicit signing secret, and only for an
authenticated session.
"""

from __future__ import annotations

import html
import os
from pathlib import Path
from typing import Any, Dict, List, Mapping, Tuple

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from alpha.webapp import operator_console_artifacts as artifacts
from alpha.webapp import operator_console_receipts as receipts

router = APIRouter()

ROUTE = "/dashboard/operator-console"
STATUS_ROUTE = "/dashboard/operator-console/status"
RECEIPTS_ROUTE = receipts.CREATE_RECEIPT_ENDPOINT

# ---------------------------------------------------------------------------
# Boundary text. These strings are asserted by tests and must appear verbatim
# in the rendered console so an operator immediately understands the mode and
# the honesty/evidence boundaries.
# ---------------------------------------------------------------------------
LOCAL_FIRST_TEXT = "Local-first operator console"
LIVE_DISABLED_TEXT = "Live provider calls are disabled in this MVP"
ARTIFACT_BOUNDARY_TEXT = (
    "Preflight and capture outputs are structural support artifacts, not "
    "answer-quality, benchmark, readiness, or superiority evidence"
)
NO_KEYS_TEXT = "No API keys are displayed"
CLAIM_BOUNDARY_TEXT = (
    "No benchmark, readiness, production, provider-validation, or "
    "superiority evidence is presented here"
)

# ---------------------------------------------------------------------------
# Provider and cost gate boundary text. The provider/cost gate panel is a
# display-only view of configuration and safety-gate state. These strings are
# asserted by tests and rendered verbatim so an operator sees that gate status
# is visibility only: no credential validation, no provider call, no billing
# truth, and no authorization of live execution.
# ---------------------------------------------------------------------------
GATE_CONFIG_VISIBILITY_TEXT = (
    "Provider and cost gate status is configuration visibility only."
)
GATE_NO_CREDENTIAL_VALIDATION_TEXT = "This console does not validate credentials."
GATE_NO_EXECUTION_TEXT = (
    "This console does not call providers, models, /v1/solve, MCP, tools, "
    "browser automation, network, CLI, or subprocesses."
)
GATE_CAPS_NOT_BILLING_TEXT = (
    "Cost caps are configured limits, not billing accuracy or spend verification."
)
GATE_KEY_CATEGORICAL_TEXT = (
    "Key status is present/missing only; no raw or partial key values are "
    "displayed."
)
GATE_NOT_READINESS_TEXT = (
    "A complete display-only gate is not provider readiness, production "
    "readiness, validation, benchmark evidence, or superiority evidence."
)
GATE_LIVE_BLOCKED_TEXT = (
    "Live execution remains blocked unless a separate future live-provider lane "
    "explicitly authorizes it."
)
GATE_BOUNDARY_NOTE = (
    "display-only; no provider call or credential validation performed"
)

GATE_BOUNDARY_TEXTS = (
    GATE_CONFIG_VISIBILITY_TEXT,
    GATE_NO_CREDENTIAL_VALIDATION_TEXT,
    GATE_NO_EXECUTION_TEXT,
    GATE_CAPS_NOT_BILLING_TEXT,
    GATE_KEY_CATEGORICAL_TEXT,
    GATE_NOT_READINESS_TEXT,
    GATE_LIVE_BLOCKED_TEXT,
)

# ---------------------------------------------------------------------------
# Dry-run preview boundary text. The dry-run preview panel is a display-only
# read of what a *future* dry-run execution lane would prepare or require. It
# executes nothing. These strings are asserted by tests and rendered verbatim so
# an operator sees that this is a preview of readiness, not a dry-run run, and
# that preview readiness is local metadata completeness only.
# ---------------------------------------------------------------------------
DRY_RUN_PREVIEW_DISPLAY_ONLY_TEXT = "Dry-run preview is display-only."
DRY_RUN_NO_SOLVE_TEXT = (
    "This console does not execute a solve from this panel."
)
DRY_RUN_NO_V1_SOLVE_TEXT = "This console does not call /v1/solve."
DRY_RUN_NO_PROVIDER_TEXT = (
    "This console does not call providers, models, MCP, browser automation, "
    "network, CLI, or subprocesses."
)
DRY_RUN_NO_ARTIFACT_MUTATION_TEXT = (
    "This console does not create, edit, delete, upload, save, or mutate "
    "artifacts."
)
DRY_RUN_NO_OUTPUT_TEXT = (
    "This console does not generate route, confidence, SAFE-OUT, expert trace, "
    "shortlist, diagnostics, answer text, model output, provider result, "
    "billing result, benchmark result, or readiness result."
)
DRY_RUN_READINESS_MEANING_TEXT = (
    "Preview readiness is local metadata completeness only."
)
DRY_RUN_NOT_EVIDENCE_TEXT = (
    "A preview-ready state is not answer-quality, validation, production, "
    "provider readiness, benchmark evidence, billing accuracy, or superiority "
    "evidence."
)
DRY_RUN_FUTURE_LANE_TEXT = (
    "A future dry-run execution lane must be separately authorized."
)

DRY_RUN_BOUNDARY_TEXTS = (
    DRY_RUN_PREVIEW_DISPLAY_ONLY_TEXT,
    DRY_RUN_NO_SOLVE_TEXT,
    DRY_RUN_NO_V1_SOLVE_TEXT,
    DRY_RUN_NO_PROVIDER_TEXT,
    DRY_RUN_NO_ARTIFACT_MUTATION_TEXT,
    DRY_RUN_NO_OUTPUT_TEXT,
    DRY_RUN_READINESS_MEANING_TEXT,
    DRY_RUN_NOT_EVIDENCE_TEXT,
    DRY_RUN_FUTURE_LANE_TEXT,
)
DRY_RUN_BOUNDARY_NOTE = (
    "display-only; no solve, provider call, CLI, artifact mutation, or "
    "generated output"
)

# Safe labels naming the existing local metadata a future dry-run would read.
# These are display-only names for surfaces this console already assembles; the
# preview never reads or synthesizes any runtime output.
DRY_RUN_WOULD_USE = (
    "local_capture_summary",
    "local_artifact_status",
    "artifact_freshness_metadata",
    "provider_cost_gate_status",
)

# Safe freshness-warning labels (mismatch flags surfaced from the existing
# sequence-coherence metadata, not ordering states).
_DRY_RUN_MISMATCH_FLAGS = frozenset(
    {"packet_id_mismatch", "counts_mismatch", "digest_invalid", "digest_unverifiable"}
)

# Portable behavior-contract file. We only check for its presence and list
# well-known high-level surface labels. We never parse or expose private
# chain-of-thought or the file's internal prompt content.
_PORTABLE_CONTRACT_PATH = "alpha_solver_portable.py"
_PORTABLE_CONTRACT_SURFACES = (
    "SolverEnvelope",
    "SAFE-OUT",
    "confidence",
    "route/expert trace",
    "local-output honesty",
    "Substantive Lift",
)

# Environment variables inspected for *presence* only. Values are never read
# into any response.
_PROVIDER_ENV = "MODEL_PROVIDER"
_EMERGENCY_STOP_ENV = "ALPHA_PROVIDER_EMERGENCY_STOP"
_LIVE_PREVIEW_ENV = "ALPHA_LIVE_PREVIEW_ENABLED"
_COST_CAP_ENVS = (
    "ALPHA_PROVIDER_MAX_COST_USD",
    "ALPHA_PROVIDER_MAX_INPUT_TOKENS",
    "ALPHA_PROVIDER_MAX_OUTPUT_TOKENS",
    "ALPHA_PROVIDER_MAX_REQUESTS",
)
# Safe per-cap labels (env name -> stable payload key). Only presence/absence of
# each cap is ever surfaced; the configured value itself is never read.
_CAP_LABELS = {
    "ALPHA_PROVIDER_MAX_COST_USD": "max_cost_usd",
    "ALPHA_PROVIDER_MAX_INPUT_TOKENS": "max_input_tokens",
    "ALPHA_PROVIDER_MAX_OUTPUT_TOKENS": "max_output_tokens",
    "ALPHA_PROVIDER_MAX_REQUESTS": "max_requests",
}
_COST_CAP_ENV = "ALPHA_PROVIDER_MAX_COST_USD"
_TOKEN_REQUEST_CAP_ENVS = (
    "ALPHA_PROVIDER_MAX_INPUT_TOKENS",
    "ALPHA_PROVIDER_MAX_OUTPUT_TOKENS",
    "ALPHA_PROVIDER_MAX_REQUESTS",
)
# Provider credential env var names surfaced as present/missing only. The names
# are shown; the values never are. GOOGLE_API_KEY is included so google/gemini
# provider gating can reason about its required key categorically.
_KEY_ENVS = ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY")

# Provider -> required credential env var(s), mirroring the categorical
# provider-key requirements in ``scripts/check_env.py``
# (``_required_keys_for_provider`` + ``_NO_KEY_PROVIDERS``). This is a small,
# display-only copy: it reasons about env *presence* categories only, never reads
# or validates a key value, and is intentionally not imported from that CLI
# script to avoid coupling the console route to CLI code. ``local`` and ``none``
# require no key; ``local_llm`` is handled separately below (it must never be
# satisfied by a hosted-provider key).
_NO_KEY_PROVIDERS = frozenset({"local", "none"})
_LOCAL_LLM_PROVIDER = "local_llm"
_PROVIDER_REQUIRED_KEYS = {
    "openai": ("OPENAI_API_KEY",),
    "anthropic": ("ANTHROPIC_API_KEY",),
    "gemini": ("GOOGLE_API_KEY",),
    "google": ("GOOGLE_API_KEY",),
}

_TRUTHY = {"1", "true", "yes", "on"}


def _escape(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def _truthy_env(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in _TRUTHY


def _key_presence(name: str) -> str:
    """Return only a categorical presence marker, never the value."""

    raw = os.getenv(name)
    if raw is None:
        return "missing"
    return "present" if raw.strip() else "missing"


def _contract_present() -> bool:
    root = Path(__file__).resolve().parents[3]
    return (root / _PORTABLE_CONTRACT_PATH).is_file()


def _cost_caps_status() -> str:
    present = sum(1 for name in _COST_CAP_ENVS if os.getenv(name, "").strip())
    if present == 0:
        return "not configured"
    if present == len(_COST_CAP_ENVS):
        return "configured"
    return "partially configured"


def _cap_present(name: str) -> str:
    """Return only a categorical presence marker for a cap, never its value."""

    return "present" if os.getenv(name, "").strip() else "missing"


def _cap_status() -> Dict[str, str]:
    """Per-cap present/missing status (no configured value is ever read)."""

    return {label: _cap_present(env) for env, label in _CAP_LABELS.items()}


def _cap_completeness() -> str:
    """Overall cap completeness across the four cost/token/request caps."""

    present = sum(1 for name in _COST_CAP_ENVS if os.getenv(name, "").strip())
    if present == 0:
        return "none_configured"
    if present == len(_COST_CAP_ENVS):
        return "configured"
    return "partially_configured"


def _cost_cap_status() -> str:
    """present/missing for the spend cap only (a configured limit, not billing)."""

    return "present" if os.getenv(_COST_CAP_ENV, "").strip() else "missing"


def _token_request_cap_status() -> str:
    """missing/partial/present across the token and request caps."""

    present = sum(
        1 for name in _TOKEN_REQUEST_CAP_ENVS if os.getenv(name, "").strip()
    )
    if present == 0:
        return "missing"
    if present == len(_TOKEN_REQUEST_CAP_ENVS):
        return "present"
    return "partial"


def _provider_mode_label(provider: str) -> str:
    """Human-readable mode label; never implies live execution is enabled."""

    return f"{provider} (live provider execution not enabled from this console)"


def _required_key_envs_for_provider(provider: str) -> Tuple[str, ...]:
    """Return the credential env var(s) the configured provider would require.

    Mirrors ``scripts/check_env.py`` categorically (presence only). ``local`` and
    ``none`` need no key; ``local_llm`` is handled separately (it must not be
    satisfied by any hosted-provider key). Unknown providers declare no required
    key here — live execution stays blocked by the always-on blockers regardless.
    """

    return _PROVIDER_REQUIRED_KEYS.get(provider, ())


def _provider_key_status(provider: str, key_status: Mapping[str, str]) -> str:
    """Categorical status of the *configured provider's* required key(s).

    Returns ``not_required`` (local/none), ``not_evaluated`` (local_llm, whose
    local runtime configuration this display-only gate does not assess),
    ``present`` (all required keys present), or ``missing`` (a required key is
    absent). Reasoning is over ``key_status`` presence categories only; no key
    value is read or validated.
    """

    if provider == _LOCAL_LLM_PROVIDER:
        return "not_evaluated"
    if provider in _NO_KEY_PROVIDERS:
        return "not_required"
    required = _required_key_envs_for_provider(provider)
    if not required:
        # Unknown provider: no known required key here. Live execution stays
        # blocked by the always-on blockers regardless.
        return "not_required"
    if all(key_status.get(env) == "present" for env in required):
        return "present"
    return "missing"


def _live_execution_blockers(
    *,
    emergency_stop_engaged: bool,
    provider_key_status: str,
    cost_cap_status: str,
    token_request_cap_status: str,
    live_preview_enabled: bool,
) -> List[str]:
    """Return safe blocker labels explaining why live execution stays blocked.

    ``display_only_lane`` and ``live_provider_calls_disabled`` are always
    present: this console is display-only and never enables live calls,
    regardless of configuration. The remaining labels describe what a future,
    separately authorized live-provider lane would still need in place. The
    provider-key blocker is derived from the *configured provider's* required
    key, not from any key. No credential is validated and no provider is
    contacted to derive these.
    """

    blockers = ["display_only_lane", "live_provider_calls_disabled"]
    if emergency_stop_engaged:
        blockers.append("emergency_stop_engaged")
    if provider_key_status == "not_evaluated":
        # local_llm: keep the gate blocked with a specific, safe label rather
        # than treating any hosted-provider key as satisfying it.
        blockers.append("local_llm_configuration_not_evaluated")
    elif provider_key_status == "missing":
        blockers.append("missing_provider_key")
    if cost_cap_status != "present":
        blockers.append("missing_cost_cap")
    if token_request_cap_status != "present":
        blockers.append("missing_token_or_request_cap")
    if not live_preview_enabled:
        blockers.append("live_preview_surface_disabled")
    return blockers


def _build_provider_gate(provider: str) -> Dict[str, Any]:
    """Assemble the display-only provider / model / cost gate status.

    Pure function over environment *presence* and truthiness only. It never
    reads a secret value, never validates a credential, and never contacts a
    provider. ``live_execution_gate`` is always ``blocked`` because this console
    is display-only; the blockers list explains why.
    """

    emergency_stop_engaged = _truthy_env(_EMERGENCY_STOP_ENV)
    live_preview_enabled = _truthy_env(_LIVE_PREVIEW_ENV)
    key_status = {name: _key_presence(name) for name in _KEY_ENVS}
    provider_key_status = _provider_key_status(provider, key_status)
    cost_cap_status = _cost_cap_status()
    token_request_cap_status = _token_request_cap_status()
    blockers = _live_execution_blockers(
        emergency_stop_engaged=emergency_stop_engaged,
        provider_key_status=provider_key_status,
        cost_cap_status=cost_cap_status,
        token_request_cap_status=token_request_cap_status,
        live_preview_enabled=live_preview_enabled,
    )

    return {
        "configured_provider": provider,
        "provider_mode_label": _provider_mode_label(provider),
        "live_provider_calls": "disabled",
        "console_calls_providers": False,
        "emergency_stop": "engaged" if emergency_stop_engaged else "not engaged",
        "live_preview_surface": "enabled" if live_preview_enabled else "disabled",
        "key_status": key_status,
        # Required key(s) for the configured provider (env var names only) and the
        # categorical status of that specific requirement.
        "required_provider_keys": list(_required_key_envs_for_provider(provider)),
        "provider_key_status": provider_key_status,
        # ``cost_caps`` retains the prior categorical summary for compatibility.
        "cost_caps": _cost_caps_status(),
        "cap_status": _cap_status(),
        "cap_completeness": _cap_completeness(),
        "cost_cap_status": cost_cap_status,
        "token_request_cap_status": token_request_cap_status,
        "live_execution_gate": "blocked",
        "live_execution_blockers": blockers,
        "gate_boundary": GATE_BOUNDARY_NOTE,
        "note": NO_KEYS_TEXT + ". Key status is present/missing only.",
    }


# ---------------------------------------------------------------------------
# Dry-run preview. A display-only read over the *already assembled* local
# artifact status and provider-gate status. It maps that existing safe metadata
# to bounded labels that answer "what would a future dry-run prepare, and what is
# still missing before a separate dry-run execution lane could be considered?".
#
# It executes nothing. It never reads raw artifact content, never calls a
# provider, never runs a solve or CLI, never mutates an artifact, and never
# synthesizes any Alpha Solver runtime field. Every value is derived from the
# two safe sub-payloads passed in.
# ---------------------------------------------------------------------------
def _dry_run_input_source_status(capture_state: Any) -> str:
    """Map the local capture state to a bounded input-source label."""

    if capture_state == "export_ready":
        return "capture_export_ready"
    if capture_state == "structurally_valid":
        return "capture_structurally_valid"
    if capture_state in {"invalid_json", "invalid_structure"}:
        return "capture_invalid"
    return "capture_missing"


def _dry_run_preflight_status(anchor_state: Any, lift_state: Any) -> Dict[str, str]:
    """Map anchor/lift preflight states to bounded present/missing/invalid labels."""

    def _one(prefix: str, state: Any) -> str:
        if state == "present":
            return f"{prefix}_present"
        if state == "missing":
            return f"{prefix}_missing"
        return f"{prefix}_invalid"

    return {
        "anchor": _one("anchor", anchor_state),
        "lift": _one("lift", lift_state),
    }


def _dry_run_freshness_warnings(sequence_coherence: Mapping[str, Any]) -> List[str]:
    """Derive safe freshness warnings from the existing sequence-coherence data.

    Only bounded labels are emitted, drawn solely from the ordering ``state`` and
    the already-safe mismatch ``flags`` in ``local_artifacts.freshness``. The
    always-present ``metadata_only_no_claim`` marker is dropped, and no raw
    artifact content is read.
    """

    warnings: List[str] = []

    def _add(label: str) -> None:
        if label not in warnings:
            warnings.append(label)

    older_labels = {
        "evidence_packet_vs_capture": "evidence_packet_older_than_capture",
        "anchor_preflight_vs_capture": "anchor_preflight_older_than_capture",
        "lift_preflight_vs_capture": "lift_preflight_older_than_capture",
    }
    for key, older_label in older_labels.items():
        entry = sequence_coherence.get(key) or {}
        if entry.get("state") == "older_than_capture":
            _add(older_label)
        for flag in entry.get("flags", []):
            if flag in _DRY_RUN_MISMATCH_FLAGS:
                _add(flag)
    return warnings


def _dry_run_preview_blockers(
    *,
    capture_state: Any,
    packet_state: Any,
    anchor_state: Any,
    lift_state: Any,
    freshness_warnings: List[str],
) -> List[str]:
    """Return safe labels naming what is missing before a future dry-run lane.

    ``provider_live_execution_blocked`` and ``display_only_lane`` are always
    present: provider/live execution is always blocked from this console and this
    is a display-only lane, regardless of how complete the local metadata is.
    """

    blockers: List[str] = []
    if capture_state == "missing":
        blockers.append("missing_capture")
    elif capture_state in {"invalid_json", "invalid_structure"}:
        blockers.append("invalid_capture")
    if packet_state == "missing":
        blockers.append("missing_evidence_packet")
    elif packet_state in {
        "invalid_json",
        "invalid_structure",
        "digest_invalid",
        "digest_unverifiable",
    }:
        blockers.append("invalid_or_unverified_evidence_packet")
    if anchor_state == "missing" or lift_state == "missing":
        blockers.append("missing_preflight_reports")
    if any(w.endswith("_older_than_capture") for w in freshness_warnings):
        blockers.append("stale_derived_artifacts")
    blockers.append("provider_live_execution_blocked")
    blockers.append("display_only_lane")
    return blockers


def _dry_run_preview_readiness(
    *,
    capture_state: Any,
    packet_state: Any,
    anchor_state: Any,
    lift_state: Any,
    freshness_warnings: List[str],
) -> str:
    """Return a bounded local-metadata-completeness label.

    This means only whether the preview has enough local metadata to explain the
    next step. It is never answer quality, route readiness, provider readiness,
    production readiness, validation, benchmark evidence, or superiority.
    """

    if capture_state in {"invalid_json", "invalid_structure"}:
        return "unavailable"
    capture_ok = capture_state in {"structurally_valid", "export_ready"}
    packet_ok = packet_state == "digest_valid"
    preflight_ok = anchor_state == "present" and lift_state == "present"
    stale = any(w.endswith("_older_than_capture") for w in freshness_warnings)
    mismatch = any(w in _DRY_RUN_MISMATCH_FLAGS for w in freshness_warnings)
    if capture_ok and packet_ok and preflight_ok and not stale and not mismatch:
        return "preview_ready"
    return "needs_artifacts"


def _build_dry_run_preview(
    local_artifacts: Mapping[str, Any], provider_gate: Mapping[str, Any]
) -> Dict[str, Any]:
    """Assemble the display-only dry-run preview payload.

    Pure function over the already-safe ``local_artifacts`` and ``provider_gate``
    sub-payloads. Executes nothing and synthesizes no runtime field.
    """

    capture_state = (local_artifacts.get("capture") or {}).get("state")
    packet_state = (local_artifacts.get("evidence_packet") or {}).get("state")
    anchor_state = (local_artifacts.get("anchor_preflight") or {}).get("state")
    lift_state = (local_artifacts.get("lift_preflight") or {}).get("state")
    sequence_coherence = (local_artifacts.get("freshness") or {}).get(
        "sequence_coherence", {}
    )

    freshness_warnings = _dry_run_freshness_warnings(sequence_coherence)
    preview_blockers = _dry_run_preview_blockers(
        capture_state=capture_state,
        packet_state=packet_state,
        anchor_state=anchor_state,
        lift_state=lift_state,
        freshness_warnings=freshness_warnings,
    )
    preview_readiness = _dry_run_preview_readiness(
        capture_state=capture_state,
        packet_state=packet_state,
        anchor_state=anchor_state,
        lift_state=lift_state,
        freshness_warnings=freshness_warnings,
    )

    return {
        "preview_mode": "display_only",
        "dry_run_execution": "not_enabled",
        "would_use": list(DRY_RUN_WOULD_USE),
        "input_source_status": _dry_run_input_source_status(capture_state),
        "evidence_packet_status": packet_state or "missing",
        "preflight_status": _dry_run_preflight_status(anchor_state, lift_state),
        "freshness_warnings": freshness_warnings,
        "provider_gate_summary": {
            "live_execution_gate": provider_gate.get("live_execution_gate"),
            "provider_key_status": provider_gate.get("provider_key_status"),
            "cap_completeness": provider_gate.get("cap_completeness"),
            "live_execution_blockers": list(
                provider_gate.get("live_execution_blockers", [])
            ),
        },
        "preview_readiness": preview_readiness,
        "preview_blockers": preview_blockers,
        "boundary": DRY_RUN_BOUNDARY_NOTE,
        "boundary_notes": list(DRY_RUN_BOUNDARY_TEXTS),
    }


def build_console_status() -> Dict[str, Any]:
    """Assemble the read-only operator console status payload.

    Pure function over configuration and environment *presence*. Performs no
    provider, network, model, or tool call, and never reads a secret value into
    the returned structure.
    """

    provider = os.getenv(_PROVIDER_ENV, "local").strip().lower() or "local"
    local_artifacts = artifacts.build_artifact_status()
    provider_gate = _build_provider_gate(provider)
    dry_run_preview = _build_dry_run_preview(local_artifacts, provider_gate)

    return {
        "console": {
            "title": "Alpha Solver Operator Console",
            "mode": "local-first",
            "live_provider_calls": "disabled",
            "claim_boundary": (
                "no benchmark/readiness/superiority evidence"
            ),
            "boundary_notes": [
                LOCAL_FIRST_TEXT,
                LIVE_DISABLED_TEXT,
                NO_KEYS_TEXT,
            ],
        },
        "portable_contract": {
            "present": _contract_present(),
            "source_path": _PORTABLE_CONTRACT_PATH,
            "contract_mode": "portable standalone behavior contract",
            "surfaces": list(_PORTABLE_CONTRACT_SURFACES),
            "note": (
                "High-level surfaces only. Private chain-of-thought is not "
                "parsed or exposed and this console does not modify the "
                "contract file."
            ),
        },
        "run_setup": {
            "run_modes": [
                {"id": "dry-run", "available": True},
                {"id": "local-only", "available": True},
                {"id": "chatgpt-copy-paste", "available": True},
                {"id": "live-provider", "available": False},
            ],
            "live_run_button_enabled": False,
            "note": (
                "This MVP does not enable live API execution. "
                + LIVE_DISABLED_TEXT
                + "."
            ),
        },
        "route_trace": {
            "route": "not run yet",
            "confidence": "not run yet",
            "safe_out_state": "not run yet",
            "expert_team": "not run yet",
            "shortlist": "not run yet",
            "diagnostics": "not run yet",
            "note": "No solve has run from this console; fields are placeholders.",
        },
        "provider_gate": provider_gate,
        "dry_run_preview": dry_run_preview,
        "preflight_capture": {
            "workflows": [
                {
                    "id": "anchor-preflight",
                    "command": (
                        "python scripts/operator_run_capture.py anchor-preflight "
                        "--case-packet <case_packet.json>"
                    ),
                },
                {
                    "id": "lift-preflight",
                    "command": (
                        "python scripts/operator_run_capture.py lift-preflight "
                        "--capture <capture.json>"
                    ),
                },
                {
                    "id": "init-capture",
                    "command": (
                        "python scripts/operator_run_capture.py init "
                        "--case-packet <case_packet.json> --out <capture.json>"
                    ),
                },
                {
                    "id": "validate-capture",
                    "command": (
                        "python scripts/operator_run_capture.py validate "
                        "--capture <capture.json>"
                    ),
                },
                {
                    "id": "export-evidence-packet",
                    "command": (
                        "python scripts/operator_run_capture.py export "
                        "--capture <capture.json> --out <packet.json>"
                    ),
                },
            ],
            "docs": "docs/OPERATOR_RUN_CAPTURE.md",
            "note": ARTIFACT_BOUNDARY_TEXT + ".",
        },
        "evidence_receipt": {
            "receipt_id": "not generated yet",
            "export_digest": "not generated yet",
            "validation_status": "not run yet",
            "note": (
                "Receipts are structural support artifacts, not answer-quality "
                "proof."
            ),
        },
        "local_artifacts": local_artifacts,
        "local_receipts": receipts.build_receipt_store_status(),
    }


# ---------------------------------------------------------------------------
# Rendering. All rendering runs through ``_escape`` so no assembled value can
# inject markup, and the status payload never carries a secret value.
# ---------------------------------------------------------------------------
def _kv_rows(pairs: Mapping[str, Any]) -> str:
    return "".join(
        f'<div class="kv"><dt>{_escape(key)}</dt>'
        f"<dd>{_escape(value)}</dd></div>"
        for key, value in pairs.items()
    )


def _list_items(items: List[Any]) -> str:
    return "".join(f"<li>{_escape(item)}</li>" for item in items)


def receipts_auth_header() -> str:
    return "x-alpha-csrf"


def _render_page(status: Mapping[str, Any]) -> str:
    console = status["console"]
    contract = status["portable_contract"]
    run_setup = status["run_setup"]
    trace = status["route_trace"]
    gate = status["provider_gate"]
    dry_run = status["dry_run_preview"]
    capture = status["preflight_capture"]
    receipt = status["evidence_receipt"]
    receipt_store = status["local_receipts"]

    run_mode_rows = "".join(
        '<li class="mode">'
        f'<span class="mode-id">{_escape(mode["id"])}</span>'
        f'<span class="badge {"ok" if mode["available"] else "off"}">'
        f'{"available" if mode["available"] else "disabled"}</span>'
        "</li>"
        for mode in run_setup["run_modes"]
    )

    key_rows = "".join(
        f'<div class="kv"><dt>{_escape(name)}</dt>'
        f'<dd><span class="badge {"ok" if state == "present" else "muted"}">'
        f"{_escape(state)}</span></dd></div>"
        for name, state in gate["key_status"].items()
    )

    # Per-cap presence rows (configured limits only; the value is never read).
    cap_rows = "".join(
        f'<div class="kv"><dt>{_escape(label)}</dt>'
        f'<dd><span class="badge {"ok" if state == "present" else "muted"}">'
        f"{_escape(state)}</span></dd></div>"
        for label, state in gate["cap_status"].items()
    )
    # Safe blocker labels explaining why live execution stays blocked.
    blocker_rows = "".join(
        f"<li>{_escape(blocker)}</li>"
        for blocker in gate["live_execution_blockers"]
    )
    gate_boundary_html = "".join(
        f"<li>{_escape(text)}</li>" for text in GATE_BOUNDARY_TEXTS
    )

    workflow_rows = "".join(
        "<li class=\"workflow\">"
        f'<code class="wf-id">{_escape(item["id"])}</code>'
        f'<pre class="wf-cmd">{_escape(item["command"])}</pre>'
        "</li>"
        for item in capture["workflows"]
    )

    contract_badge = "present" if contract["present"] else "missing"

    # Local artifact status (read-only; counts/states/digests only).
    local = status["local_artifacts"]
    no_artifacts_msg = local["no_artifacts_message"]
    cap = local["capture"]
    pkt = local["evidence_packet"]
    anchor = local["anchor_preflight"]
    lift = local["lift_preflight"]

    def _state_badge(state: Any) -> str:
        good = {"structurally_valid", "export_ready", "digest_valid", "present"}
        bad = {"invalid_json", "invalid_structure", "digest_invalid"}
        text = str(state)
        cls = "ok" if text in good else "off" if text in bad else "muted"
        return f'<span class="badge {cls}">{_escape(text)}</span>'

    def _no_artifacts_note() -> str:
        return f'<p class="note">{_escape(no_artifacts_msg)}</p>'

    # Route and Trace: local capture counts + route metadata presence count.
    if cap.get("state") in {"structurally_valid", "export_ready"}:
        cap_counts = cap.get("counts", {})
        trace_artifact_html = _kv_rows(
            {
                "captured (local)": cap_counts.get("captured", 0),
                "excluded (local)": cap_counts.get("excluded", 0),
                "pending (local)": cap_counts.get("pending", 0),
                "route metadata present": cap.get("route_metadata_present_count", 0),
            }
        )
    elif cap.get("state") == "missing":
        trace_artifact_html = _no_artifacts_note()
    else:
        trace_artifact_html = (
            f'<div class="kv"><dt>local capture</dt><dd>'
            f'{_state_badge(cap.get("state"))}</dd></div>'
        )

    # Preflight and Capture: whether reports exist and need attention.
    def _preflight_rows(label: str, summary: Mapping[str, Any]) -> str:
        state = summary.get("state")
        if state == "present":
            return (
                f'<div class="kv"><dt>{_escape(label)}</dt><dd>'
                f'{_state_badge(state)} · needs attention: '
                f'{_escape(summary.get("needs_attention_count", 0))}</dd></div>'
            )
        return (
            f'<div class="kv"><dt>{_escape(label)}</dt><dd>'
            f'{_state_badge(state)}</dd></div>'
        )

    preflight_artifact_html = _preflight_rows(
        "anchor preflight report", anchor
    ) + _preflight_rows("lift preflight report", lift)

    # Evidence and Receipt: root, capture/packet states, digest, id, counts.
    pkt_counts = pkt.get("counts", {})
    evidence_artifact_html = _kv_rows(
        {
            "artifact root": local["artifact_root"],
            "local artifacts detected": "yes" if local["detected"] else "no",
        }
    ) + (
        f'<div class="kv"><dt>capture state</dt><dd>'
        f'{_state_badge(cap.get("state"))}</dd></div>'
        f'<div class="kv"><dt>evidence packet state</dt><dd>'
        f'{_state_badge(pkt.get("state"))}</dd></div>'
        + _kv_rows(
            {
                "packet id": pkt.get("packet_id") or "—",
                "content digest": pkt.get("content_digest") or "—",
                "packet captured": pkt_counts.get("captured", "—"),
                "packet excluded": pkt_counts.get("excluded", "—"),
                "packet total": pkt_counts.get("total", "—"),
            }
        )
    )
    boundary_html = "".join(
        f"<li>{_escape(text)}</li>" for text in local["boundaries"]
    )
    evidence_no_artifacts = "" if local["detected"] else _no_artifacts_note()

    # Artifact freshness and sequence coherence (local filesystem metadata only;
    # never a quality/readiness signal). Only safe labels/timestamps/states are
    # rendered — no absolute path and no raw artifact content.
    freshness = local["freshness"]
    fresh_files = freshness["files"]
    fresh_seq = freshness["sequence_coherence"]

    def _freshness_row(label: str, meta: Mapping[str, Any]) -> str:
        return (
            f'<div class="kv"><dt>{_escape(label)}</dt><dd>'
            f'<span class="badge muted">{_escape(meta["age_label"])}</span>'
            f' · {_escape(meta["modified_at_utc"] or "—")}'
            f' · age {_escape(meta["age_seconds"] if meta["age_seconds"] is not None else "—")}s'
            "</dd></div>"
        )

    freshness_files_html = (
        _freshness_row("capture", fresh_files["capture"])
        + _freshness_row("evidence packet", fresh_files["evidence_packet"])
        + _freshness_row("anchor preflight", fresh_files["anchor_preflight"])
        + _freshness_row("lift preflight", fresh_files["lift_preflight"])
    )

    def _coherence_row(label: str, entry: Mapping[str, Any]) -> str:
        # Drop the always-present metadata-only marker from the visible flags.
        flags = [f for f in entry["flags"] if f != "metadata_only_no_claim"]
        flag_text = ", ".join(flags) if flags else "—"
        return (
            f'<div class="kv"><dt>{_escape(label)}</dt><dd>'
            f'<span class="badge muted">{_escape(entry["state"])}</span>'
            f' · flags: {_escape(flag_text)}</dd></div>'
        )

    coherence_html = (
        _coherence_row(
            "evidence packet vs capture", fresh_seq["evidence_packet_vs_capture"]
        )
        + _coherence_row(
            "anchor preflight vs capture", fresh_seq["anchor_preflight_vs_capture"]
        )
        + _coherence_row(
            "lift preflight vs capture", fresh_seq["lift_preflight_vs_capture"]
        )
    )

    freshness_boundary_html = "".join(
        f"<li>{_escape(text)}</li>" for text in freshness["boundaries"]
    )

    # Dry-Run Preview card (display-only). Every value comes from the already-safe
    # dry_run_preview payload; nothing here executes, mutates, or synthesizes
    # runtime output.
    dr_would_use_html = "".join(
        f"<li>{_escape(item)}</li>" for item in dry_run["would_use"]
    )
    dr_warnings = dry_run["freshness_warnings"]
    dr_warnings_html = (
        "".join(f"<li>{_escape(w)}</li>" for w in dr_warnings)
        if dr_warnings
        else "<li>none</li>"
    )
    dr_blockers_html = "".join(
        f"<li>{_escape(b)}</li>" for b in dry_run["preview_blockers"]
    )
    dr_boundary_html = "".join(
        f"<li>{_escape(text)}</li>" for text in dry_run["boundary_notes"]
    )
    dr_gate = dry_run["provider_gate_summary"]

    receipt_items = receipt_store["recent"]
    receipt_rows = (
        "".join(
            "<li>"
            f"<strong>{_escape(item.get('receipt_id') or 'invalid')}</strong>"
            f" · {_escape(item.get('created_at_utc') or 'unknown time')}"
            f" · {_escape(item.get('state'))}"
            f" · {_escape(item.get('content_digest') or '—')}"
            f" · {_escape((item.get('snapshot_summary') or {}).get('preview_readiness') or '—')}"
            "</li>"
            for item in receipt_items
        )
        if receipt_items
        else "<li>No local receipts saved yet.</li>"
    )
    receipt_boundary_html = "".join(
        f"<li>{_escape(text)}</li>" for text in receipt_store["boundary_notes"]
    )

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Alpha Solver · Operator Console</title>
    <style>
      :root {{ color-scheme: light dark; font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; line-height: 1.5; }}
      body {{ margin: 0; min-height: 100vh; background: radial-gradient(circle at top, #f6f8ff, #e4e8f4); color: #1d2038; }}
      .container {{ max-width: 1120px; margin: 0 auto; padding: 2.5rem 1.25rem 4rem; }}
      h1 {{ margin: 0 0 0.35rem; font-size: 1.75rem; }}
      .subtitle {{ color: #565b8f; margin: 0 0 1.25rem; font-weight: 600; }}
      .banner {{ border: 1px solid #c7d2fe; background: rgba(238, 242, 255, 0.9); border-radius: 14px; padding: 1rem 1.15rem; color: #30365f; margin-bottom: 1.5rem; }}
      .banner ul {{ margin: 0.5rem 0 0; padding-left: 1.1rem; }}
      .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.1rem; align-items: start; }}
      .card {{ background: rgba(255, 255, 255, 0.94); border-radius: 16px; padding: 1.15rem 1.25rem; box-shadow: 0 18px 55px rgba(31, 35, 71, 0.08); min-width: 0; }}
      .card h2 {{ margin: 0 0 0.75rem; font-size: 1.08rem; }}
      .kv {{ display: grid; grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr); gap: 0.4rem 0.75rem; padding: 0.25rem 0; border-bottom: 1px solid rgba(86, 97, 246, 0.1); }}
      dt {{ color: #565b8f; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.03em; text-transform: uppercase; margin: 0; }}
      dd {{ margin: 0; font-weight: 600; overflow-wrap: anywhere; }}
      ul {{ margin: 0; padding-left: 1.1rem; }}
      li {{ margin: 0.2rem 0; overflow-wrap: anywhere; }}
      li.mode, li.workflow {{ list-style: none; }}
      ul.modes, ul.workflows {{ padding-left: 0; }}
      .mode {{ display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; padding: 0.35rem 0; border-bottom: 1px solid rgba(86, 97, 246, 0.1); }}
      .mode-id {{ font-weight: 700; }}
      .badge {{ display: inline-block; border-radius: 999px; padding: 0.12rem 0.6rem; font-size: 0.76rem; font-weight: 800; }}
      .badge.ok {{ background: rgba(16, 185, 129, 0.16); color: #047857; }}
      .badge.off {{ background: rgba(244, 63, 94, 0.14); color: #9f1239; }}
      .badge.muted {{ background: rgba(100, 116, 139, 0.16); color: #475569; }}
      .surfaces li {{ font-weight: 600; }}
      .workflow {{ padding: 0.4rem 0; border-bottom: 1px solid rgba(86, 97, 246, 0.1); }}
      .wf-id {{ font-weight: 800; color: #3730a3; }}
      pre.wf-cmd {{ white-space: pre-wrap; overflow-wrap: anywhere; background: #111827; color: #e5e7eb; border-radius: 10px; padding: 0.55rem 0.7rem; margin: 0.35rem 0 0; font-size: 0.82rem; }}
      .note {{ color: #5f668f; font-size: 0.85rem; margin: 0.65rem 0 0; }}
      .subhead {{ margin: 1rem 0 0.35rem; font-size: 0.95rem; color: #30365f; }}
      .disabled-btn {{ margin-top: 0.75rem; border: 0; border-radius: 999px; padding: 0.6rem 1.15rem; font: inherit; font-weight: 700; color: #475569; background: rgba(100, 116, 139, 0.16); cursor: not-allowed; }}
      a.status-link, a.refresh-link {{ display: inline-block; margin-top: 0.75rem; color: #4f46e5; font-weight: 700; }}
      a.refresh-link {{ margin-right: 0.85rem; }}
      .receipt-btn {{ margin-top: 0.75rem; border: 0; border-radius: 999px; padding: 0.6rem 1.15rem; font: inherit; font-weight: 800; color: #ffffff; background: #4f46e5; cursor: pointer; }}
    </style>
  </head>
  <body>
    <main class="container">
      <h1>{_escape(console["title"])}</h1>
      <p class="subtitle">{_escape(LOCAL_FIRST_TEXT)}</p>
      <section class="banner" aria-label="Operator console mode and boundaries">
        <strong>{_escape(LIVE_DISABLED_TEXT)}.</strong>
        <ul>
          <li>Mode: {_escape(console["mode"])}</li>
          <li>Live provider calls: {_escape(console["live_provider_calls"])}</li>
          <li>Claim boundary: {_escape(console["claim_boundary"])}</li>
          <li>{_escape(CLAIM_BOUNDARY_TEXT)}.</li>
          <li>{_escape(NO_KEYS_TEXT)}.</li>
          {boundary_html}
        </ul>
      </section>

      <div class="cards">
        <article class="card" id="card-portable-contract">
          <h2>Portable Contract Status</h2>
          {_kv_rows({
              "present": contract_badge,
              "source path": contract["source_path"],
              "contract mode": contract["contract_mode"],
          })}
          <p class="note">Surfaces (high-level only):</p>
          <ul class="surfaces">{_list_items(contract["surfaces"])}</ul>
          <p class="note">{_escape(contract["note"])}</p>
        </article>

        <article class="card" id="card-run-setup">
          <h2>Run Setup</h2>
          <p class="note">Prompt input is disabled in this MVP shell.</p>
          <textarea placeholder="Prompt entry is disabled in this MVP" disabled aria-disabled="true" style="width:100%;min-height:70px;border-radius:10px;border:1px solid #cdd5ef;padding:0.6rem;font:inherit;background:rgba(255,255,255,0.6);"></textarea>
          <ul class="modes">{run_mode_rows}</ul>
          <button type="button" class="disabled-btn" disabled aria-disabled="true">Live run (disabled)</button>
          <p class="note">{_escape(run_setup["note"])}</p>
        </article>

        <article class="card" id="card-dry-run-preview">
          <h2>Dry-Run Preview</h2>
          <p class="note">Display-only preview of what a future dry-run would prepare and require. Nothing on this panel starts a dry-run.</p>
          {_kv_rows({
              "preview mode": dry_run["preview_mode"],
              "dry-run execution": dry_run["dry_run_execution"],
              "preview readiness": dry_run["preview_readiness"],
              "input source": dry_run["input_source_status"],
              "evidence packet": dry_run["evidence_packet_status"],
              "anchor preflight": dry_run["preflight_status"]["anchor"],
              "lift preflight": dry_run["preflight_status"]["lift"],
          })}
          <p class="note">Would use (existing local metadata only):</p>
          <ul class="surfaces">{dr_would_use_html}</ul>
          <p class="note">Freshness warnings (local metadata only):</p>
          <ul class="surfaces">{dr_warnings_html}</ul>

          <h3 class="subhead">Provider gate summary (live execution stays blocked)</h3>
          {_kv_rows({
              "live execution gate": dr_gate["live_execution_gate"],
              "provider key (configured provider)": dr_gate["provider_key_status"],
              "cap completeness": dr_gate["cap_completeness"],
          })}
          <p class="note">Preview blockers (what is missing before a future dry-run lane):</p>
          <ul class="surfaces">{dr_blockers_html}</ul>
          <p class="note">{_escape(dry_run["boundary"])}.</p>
          <ul class="surfaces">{dr_boundary_html}</ul>
        </article>

        <article class="card" id="card-route-trace">
          <h2>Route and Trace</h2>
          {_kv_rows({
              "route": trace["route"],
              "confidence": trace["confidence"],
              "SAFE-OUT state": trace["safe_out_state"],
              "expert/team": trace["expert_team"],
              "shortlist": trace["shortlist"],
              "diagnostics": trace["diagnostics"],
          })}
          <p class="note">{_escape(trace["note"])}</p>
          <p class="note">Local capture counts (structural only):</p>
          {trace_artifact_html}
        </article>

        <article class="card" id="card-provider-gate">
          <h2>Provider and Cost Gate</h2>
          {_kv_rows({
              "configured provider": gate["configured_provider"],
              "provider mode": gate["provider_mode_label"],
              "live provider calls": gate["live_provider_calls"],
              "console calls providers": gate["console_calls_providers"],
              "emergency stop": gate["emergency_stop"],
              "live preview surface": gate["live_preview_surface"],
          })}

          <h3 class="subhead">Live Execution Gate (display-only)</h3>
          {_kv_rows({
              "gate result": gate["live_execution_gate"],
              "provider key (configured provider)": gate["provider_key_status"],
              "cap completeness": gate["cap_completeness"],
              "cost cap": gate["cost_cap_status"],
              "token/request caps": gate["token_request_cap_status"],
          })}
          <p class="note">Blockers (why live execution stays blocked):</p>
          <ul class="surfaces">{blocker_rows}</ul>
          <p class="note">Cap presence (configured limits only, not billing truth):</p>
          {cap_rows}
          <p class="note">Key presence (categorical only):</p>
          {key_rows}
          <p class="note">{_escape(gate["gate_boundary"])}.</p>
          <ul class="surfaces">{gate_boundary_html}</ul>
          <p class="note">{_escape(gate["note"])}</p>
        </article>

        <article class="card" id="card-preflight-capture">
          <h2>Preflight and Capture Entry</h2>
          <p class="note">Local workflows (run from a terminal, not from this console):</p>
          <ul class="workflows">{workflow_rows}</ul>
          <p class="note">Docs: {_escape(capture["docs"])}</p>
          <p class="note">{_escape(capture["note"])}</p>
          <p class="note">Local preflight report status:</p>
          {preflight_artifact_html}
        </article>



        <article class="card" id="card-local-receipt-store">
          <h2>Local Receipt Store</h2>
          {_kv_rows({
              "receipt root": receipt_store["receipt_root"],
              "recent receipt count": receipt_store["count"],
              "store state": ", ".join(receipt_store["states"]),
              "boundary": receipt_store["boundary"],
          })}
          <form method="post" action="{RECEIPTS_ROUTE}" data-csrf-header="{_escape(receipts_auth_header())}" onsubmit="event.preventDefault(); fetch(this.action, {{method: 'POST', headers: {{'{_escape(receipts_auth_header())}': document.cookie.split('; ').find(r => r.startsWith('alpha_dashboard_csrf='))?.split('=')[1] || ''}}}}).then(() => window.location.href='{ROUTE}');">
            <button type="submit" class="receipt-btn">Save local receipt snapshot</button>
          </form>
          <p class="note">Recent receipts (safe metadata only):</p>
          <ul class="surfaces">{receipt_rows}</ul>
          <ul class="surfaces">{receipt_boundary_html}</ul>
        </article>

        <article class="card" id="card-evidence-receipt">
          <h2>Evidence and Receipt</h2>
          {_kv_rows({
              "receipt id": receipt["receipt_id"],
              "export digest": receipt["export_digest"],
              "validation status": receipt["validation_status"],
          })}
          <p class="note">{_escape(receipt["note"])}</p>
          <p class="note">Local artifact status:</p>
          {evidence_artifact_html}
          {evidence_no_artifacts}
          <ul class="surfaces">{boundary_html}</ul>
          <p class="note">{_escape(ARTIFACT_BOUNDARY_TEXT)}.</p>

          <h3 class="subhead">Artifact Freshness and Sequence Coherence</h3>
          <p class="note">Local filesystem metadata only. Status generated at: {_escape(local["status_generated_at_utc"])}</p>
          {freshness_files_html}
          <p class="note">Derived-vs-capture ordering (metadata only):</p>
          {coherence_html}
          <ul class="surfaces">{freshness_boundary_html}</ul>
          <a class="refresh-link" href="{ROUTE}">Refresh (reload this read-only page)</a>
        </article>
      </div>

      <a class="status-link" href="{STATUS_ROUTE}">Read-only status JSON</a>
    </main>
  </body>
</html>"""


@router.get(ROUTE, response_class=HTMLResponse)
async def operator_console_page() -> HTMLResponse:
    """Render the read-only operator console shell."""

    return HTMLResponse(content=_render_page(build_console_status()))


@router.post(RECEIPTS_ROUTE)
async def operator_console_create_receipt() -> RedirectResponse:
    """Create one safe local receipt snapshot and return to the console."""

    status = build_console_status()
    receipts.create_receipt_snapshot(status)
    return RedirectResponse(ROUTE, status_code=303)


@router.get(STATUS_ROUTE)
async def operator_console_status() -> JSONResponse:
    """Return the read-only operator console status as JSON.

    The payload is assembled by :func:`build_console_status` and never contains
    a raw secret value.
    """

    return JSONResponse(content=build_console_status())
