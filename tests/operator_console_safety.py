"""Reusable test-only guards for Operator Console execution/write boundaries."""

from __future__ import annotations

import builtins
import socket
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import pytest


class OperatorConsoleSafetyViolation(AssertionError):
    """Raised when a guarded Operator Console path crosses a forbidden boundary."""


@contextmanager
def operator_console_no_execution_guard(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Block execution-capable operations while allowing in-process test clients.

    Network blocking is at the socket layer. Loopback is allowed so FastAPI's
    in-process TestClient and any existing local-only harness assumptions remain usable,
    but non-loopback/provider egress raises before a real external connection.
    """

    original_connect = socket.socket.connect
    original_connect_ex = socket.socket.connect_ex

    def _is_loopback(address: object) -> bool:
        host = address[0] if isinstance(address, tuple) and address else address
        return str(host) in {"127.0.0.1", "::1", "localhost", "testserver"}

    def guarded_connect(self: socket.socket, address: object) -> object:
        if not _is_loopback(address):
            raise OperatorConsoleSafetyViolation(f"blocked outbound network egress: {address!r}")
        return original_connect(self, address)  # pragma: no cover - only if a local socket is used

    def guarded_connect_ex(self: socket.socket, address: object) -> int:
        if not _is_loopback(address):
            raise OperatorConsoleSafetyViolation(f"blocked outbound network egress: {address!r}")
        return original_connect_ex(self, address)  # pragma: no cover - only if a local socket is used

    def _blocked_process(*_args: object, **_kwargs: object) -> None:
        raise OperatorConsoleSafetyViolation("blocked subprocess/shell/CLI execution")

    monkeypatch.setattr(socket.socket, "connect", guarded_connect)
    monkeypatch.setattr(socket.socket, "connect_ex", guarded_connect_ex)
    monkeypatch.setattr(subprocess, "run", _blocked_process)
    monkeypatch.setattr(subprocess, "Popen", _blocked_process)
    monkeypatch.setattr(subprocess, "call", _blocked_process)
    monkeypatch.setattr(subprocess, "check_call", _blocked_process)
    monkeypatch.setattr(subprocess, "check_output", _blocked_process)
    yield


@contextmanager
def operator_console_no_get_write_guard(
    monkeypatch: pytest.MonkeyPatch, *, allowed_write_root: Path | None = None
) -> Iterator[None]:
    """Block filesystem writes from Operator Console GET/render/status paths.

    The optional allowlist is for receipt-write canaries or explicit receipt tests only;
    render/status tests normally pass no allowlist, so any write attempt fails.
    """

    original_open = builtins.open
    original_write_text = Path.write_text
    original_write_bytes = Path.write_bytes
    write_modes = {"w", "a", "x", "+"}

    def _is_allowed(path: object) -> bool:
        if allowed_write_root is None:
            return False
        try:
            Path(path).resolve().relative_to(allowed_write_root.resolve())
            return True
        except (TypeError, OSError, RuntimeError, ValueError):
            return False

    def guarded_open(file: object, mode: str = "r", *args: object, **kwargs: object) -> object:
        if any(flag in mode for flag in write_modes) and not _is_allowed(file):
            raise OperatorConsoleSafetyViolation(f"blocked unauthorized filesystem write: {file!r}")
        return original_open(file, mode, *args, **kwargs)

    def guarded_write_text(self: Path, *_args: object, **_kwargs: object) -> int:
        if not _is_allowed(self):
            raise OperatorConsoleSafetyViolation(f"blocked unauthorized Path.write_text: {self!s}")
        return original_write_text(self, *_args, **_kwargs)

    def guarded_write_bytes(self: Path, *_args: object, **_kwargs: object) -> int:
        if not _is_allowed(self):
            raise OperatorConsoleSafetyViolation(f"blocked unauthorized Path.write_bytes: {self!s}")
        return original_write_bytes(self, *_args, **_kwargs)

    monkeypatch.setattr(builtins, "open", guarded_open)
    monkeypatch.setattr(Path, "write_text", guarded_write_text)
    monkeypatch.setattr(Path, "write_bytes", guarded_write_bytes)
    yield
