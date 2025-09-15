"""Minimal OpenTelemetry helpers for Alpha Solver.

This module wires a tracer with an in-memory exporter so tests can inspect
spans.  When OpenTelemetry is not installed a small no-op tracer is used
instead so importing this module never raises ImportError in constrained
environments.

The :func:`span` context manager performs attribute redaction to avoid
accidentally recording user supplied text or secrets in telemetry data.  A
latency attribute is automatically added if one is not supplied.
"""

from __future__ import annotations

import logging
import time
from contextlib import contextmanager
from typing import Any, Dict
from service.logging.redactor import redact, ERROR_COUNTER

try:  # Prefer the real OpenTelemetry SDK if available
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import (InMemorySpanExporter,
                                                SimpleSpanProcessor)

    HAVE_OTEL = True
except Exception:  # package missing or partial install
    trace = None  # type: ignore
    TracerProvider = InMemorySpanExporter = SimpleSpanProcessor = None  # type: ignore
    HAVE_OTEL = False


TRACER = None
EXPORTER = None
_STUB_SPANS = []  # used when OpenTelemetry SDK is unavailable

# --- redaction -----------------------------------------------------------

_DENY_KEYS = {"user_input", "secret", "password", "pii", "raw", "prompt", "token"}


def _clean_value(val: Any) -> Any:
    if isinstance(val, (str, dict)):
        return redact(val)
    return val


def _redact(attrs: Dict[str, Any]) -> Dict[str, Any]:
    """Redact and filter attributes before recording."""

    clean: Dict[str, Any] = {}
    for key, val in attrs.items():
        lowered = str(key).lower()
        if any(s in lowered for s in _DENY_KEYS):
            logging.getLogger(__name__).warning("dropping span attribute %s", key)
            continue
        try:
            clean[key] = _clean_value(val)
        except Exception:  # pragma: no cover - defensive
            ERROR_COUNTER.inc()
    return clean


# --- span helpers -------------------------------------------------------


@contextmanager
def span(name: str, **attrs: Any):
    """Start a traced span with basic attribute redaction.

    The active tracer is used if available; otherwise a no-op tracer.  The span
    is automatically annotated with ``latency_ms`` if the caller did not supply
    one.
    """

    tracer = TRACER or _StubTracer()
    clean = _redact(attrs)
    start = time.time()
    with tracer.start_as_current_span(name) as sp:  # pragma: no cover - context
        if hasattr(sp, "set_attribute"):
            for k, v in clean.items():
                sp.set_attribute(k, v)
        yield sp
        if hasattr(sp, "set_attribute") and "latency_ms" not in clean:
            sp.set_attribute("latency_ms", (time.time() - start) * 1000.0)


# --- tracer init/export helpers ----------------------------------------


def init_tracer(app: Any | None = None):
    """Initialise a tracer with an in-memory exporter.

    The exporter allows tests to verify spans without external dependencies.
    When OpenTelemetry is unavailable a no-op tracer is returned.
    """

    global TRACER, EXPORTER

    if not HAVE_OTEL:
        TRACER = _StubTracer()
        if app is not None and hasattr(app, "state"):
            app.state.tracer = TRACER
        return TRACER

    provider = TracerProvider()  # type: ignore[call-arg]
    EXPORTER = InMemorySpanExporter()  # type: ignore[call-arg]
    provider.add_span_processor(SimpleSpanProcessor(EXPORTER))  # type: ignore[arg-type]
    trace.set_tracer_provider(provider)  # type: ignore[call-arg]
    TRACER = trace.get_tracer("alpha_solver")  # type: ignore[attr-defined]
    if app is not None and hasattr(app, "state"):
        app.state.tracer = TRACER
    return TRACER


def get_exported_spans():
    """Return spans recorded by the in-memory exporter."""

    if HAVE_OTEL and EXPORTER is not None:
        return list(EXPORTER.get_finished_spans())  # type: ignore[return-value]
    return list(_STUB_SPANS)


def reset_exported_spans() -> None:
    """Clear all spans from the exporter."""

    if HAVE_OTEL and EXPORTER is not None:
        EXPORTER.clear()  # type: ignore[operator]
    _STUB_SPANS.clear()


# --- fallback tracer implementation ------------------------------------


class _StubSpan:
    def __init__(self, name: str, parent_ctx: Any | None = None) -> None:
        self.name = name
        self.parent = parent_ctx
        self.attributes: Dict[str, Any] = {}
        self.context = type("_Ctx", (), {"span_id": id(self)})()

    def set_attribute(self, key: str, value: Any) -> None:
        self.attributes[key] = value


class _StubTracer:
    def __init__(self) -> None:
        self._stack: list[_StubSpan] = []

    def start_as_current_span(self, name: str):
        parent_ctx = self._stack[-1].context if self._stack else None
        span = _StubSpan(name, parent_ctx)

        @contextmanager
        def _cm():
            self._stack.append(span)
            try:
                yield span
            finally:
                self._stack.pop()
                _STUB_SPANS.append(span)

        return _cm()


__all__ = [
    "init_tracer",
    "span",
    "get_exported_spans",
    "reset_exported_spans",
    "HAVE_OTEL",
]

