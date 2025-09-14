from __future__ import annotations

import socket
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from threading import Thread
from typing import Any, Callable, Dict, Iterable, Optional, Tuple


class SandboxViolation(Exception):
    """Raised when sandbox policy is violated."""


class SandboxDecision(Enum):
    """Outcome of sandbox policy evaluation or execution."""

    ALLOW = "ALLOW"
    DENY = "DENY"
    TIMEOUT = "TIMEOUT"
    SIZE_LIMIT = "SIZE_LIMIT"
    POLICY_VIOLATION = "POLICY_VIOLATION"


@dataclass
class SandboxPolicy:
    """Configuration controlling sandbox behaviour."""

    allow_network: bool = False
    network_allowlist: Iterable[str] = field(default_factory=list)
    allow_scripts: bool = False
    max_time_ms: int = 1500
    max_output_bytes: int = 65_536
    max_tokens: int = 4096


ALLOWED_DESCRIPTOR_KEYS = {"type", "hostname"}


def evaluate_descriptor(descriptor: Dict[str, Any], policy: SandboxPolicy) -> SandboxDecision:
    """Evaluate a tool descriptor against the sandbox policy.

    Unknown fields trigger a policy violation. Script descriptors are
    denied unless explicitly allowed. Network descriptors are denied
    when network access is disabled or the hostname is not allow-listed.
    """

    unknown = set(descriptor) - ALLOWED_DESCRIPTOR_KEYS
    if unknown:
        return SandboxDecision.POLICY_VIOLATION

    if descriptor.get("type") == "script" and not policy.allow_scripts:
        return SandboxDecision.DENY

    hostname = descriptor.get("hostname")
    if hostname:
        if not policy.allow_network or hostname not in policy.network_allowlist:
            return SandboxDecision.DENY

    return SandboxDecision.ALLOW


@contextmanager
def network_guard(policy: SandboxPolicy):
    """Simulate network restrictions by monkey-patching ``socket.create_connection``."""

    original = socket.create_connection

    def guarded(address: Any, *args: Any, **kwargs: Any):
        host: str
        if isinstance(address, tuple):
            host = address[0]
        else:
            host = address
        allowed = policy.allow_network and host in policy.network_allowlist
        if not allowed:
            raise SandboxViolation(f"network to {host} not allowed")
        # Return a dummy object; no real socket is opened.
        return object()

    socket.create_connection = guarded  # type: ignore[assignment]
    try:
        yield
    finally:
        socket.create_connection = original  # type: ignore[assignment]


def run_with_limits(
    callable_fn: Callable[..., Any],
    *,
    policy: SandboxPolicy,
    args: Tuple[Any, ...] = (),
    kwargs: Optional[Dict[str, Any]] = None,
) -> Tuple[Optional[Any], SandboxDecision, Dict[str, Any]]:
    """Execute ``callable_fn`` under sandbox limits.

    Returns a tuple of (result_or_none, decision, meta). ``meta`` contains
    timing and size information along with the policy budgets used.
    """

    if kwargs is None:
        kwargs = {}

    start = time.perf_counter()
    result_container: Dict[str, Any] = {}
    exc_container: Dict[str, BaseException] = {}

    def target() -> None:
        try:
            with network_guard(policy):
                result_container["value"] = callable_fn(*args, **kwargs)
        except BaseException as exc:  # noqa: BLE001 - we fail closed
            exc_container["error"] = exc

    thread = Thread(target=target, daemon=True)
    thread.start()
    thread.join(policy.max_time_ms / 1000)

    elapsed_ms = int((time.perf_counter() - start) * 1000)
    output_bytes = 0
    meta: Dict[str, Any] = {
        "elapsed_ms": elapsed_ms,
        "output_bytes": output_bytes,
        "max_time_ms": policy.max_time_ms,
        "max_output_bytes": policy.max_output_bytes,
        "allow_network": policy.allow_network,
    }

    if thread.is_alive():
        decision = SandboxDecision.TIMEOUT
        return None, decision, meta

    if "error" in exc_container:
        exc = exc_container["error"]
        if isinstance(exc, SandboxViolation):
            meta["class"] = "SECURITY/SANDBOX_VIOLATION"
            decision = SandboxDecision.POLICY_VIOLATION
        else:
            decision = SandboxDecision.POLICY_VIOLATION
        return None, decision, meta

    result = result_container.get("value")
    output_bytes = len(str(result).encode())
    meta["output_bytes"] = output_bytes
    if output_bytes > policy.max_output_bytes:
        decision = SandboxDecision.SIZE_LIMIT
        return None, decision, meta

    decision = SandboxDecision.ALLOW
    return result, decision, meta


def to_route_explain(decision: SandboxDecision, meta: Dict[str, Any]) -> Dict[str, Any]:
    """Return a minimal dict describing the sandbox outcome."""

    budgets = {
        "elapsed_ms": meta.get("elapsed_ms"),
        "max_time_ms": meta.get("max_time_ms"),
        "output_bytes": meta.get("output_bytes"),
        "max_output_bytes": meta.get("max_output_bytes"),
        "allow_network": meta.get("allow_network"),
    }
    return {"sandbox_decision": decision.name, "budgets": budgets}
