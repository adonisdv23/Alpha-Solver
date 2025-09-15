"""
OpenTelemetry tracing setup with graceful fallback when the package is
missing.  Consumers call :func:`init_tracer` which installs a tracer provider
on the FastAPI application if OpenTelemetry is available, otherwise a simple
no-op tracer is registered.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Optional, Any

try:  # pragma: no cover - import is trivial
    from opentelemetry import trace  # type: ignore
    from opentelemetry.sdk.trace import TracerProvider  # type: ignore
    from opentelemetry.sdk.trace.export import BatchSpanProcessor  # type: ignore
    HAVE_OTEL = True
except Exception:  # pragma: no cover - package not installed
    HAVE_OTEL = False


class _NoopTracer:
    """Minimal tracer used when OpenTelemetry isn't present."""

    def start_as_current_span(self, *a: Any, **k: Any):
        @contextmanager
        def cm():
            yield

        return cm()


def _ensure_app(app: Any) -> Any:
    """Ensure the passed app has a ``state`` attribute."""

    if app is None:
        from types import SimpleNamespace

        app = SimpleNamespace()
    if not hasattr(app, "state"):
        from types import SimpleNamespace

        app.state = SimpleNamespace()
    return app


def init_tracer(app: Any = None, exporter: Optional[Any] = None) -> Any:
    """Initialise tracing for ``app`` and return the provider/tracer.

    When OpenTelemetry is unavailable a :class:`_NoopTracer` instance is
    attached to ``app.state.tracer`` and returned.  This keeps the rest of the
    application code agnostic to the presence of the dependency.
    """

    app = _ensure_app(app)

    if not HAVE_OTEL:
        tracer = _NoopTracer()
        app.state.tracer = tracer
        return tracer

    from opentelemetry import trace  # type: ignore
    from opentelemetry.sdk.trace import TracerProvider  # type: ignore
    from opentelemetry.sdk.trace.export import (
        InMemorySpanExporter,
    )

    provider = trace.get_tracer_provider()
    if not isinstance(provider, TracerProvider):
        provider = TracerProvider()
        trace.set_tracer_provider(provider)

    app.state.tracer_provider = provider

    if exporter is None:
        exporter = InMemorySpanExporter()

    processor = BatchSpanProcessor(exporter)  # type: ignore[arg-type]
    provider.add_span_processor(processor)
    app.state.span_processor = processor

    if not hasattr(provider, "force_flush"):
        def _force_flush(timeout_millis: Optional[int] = None):
            try:
                return processor.force_flush(timeout_millis)
            except Exception:  # pragma: no cover - defensive
                return True

        provider.force_flush = _force_flush  # type: ignore[attr-defined]

    return provider
