from contextlib import contextmanager
from typing import Any

try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    HAVE_OTEL = True
except Exception:  # package missing or partial install
    trace = None  # type: ignore
    TracerProvider = BatchSpanProcessor = None  # type: ignore
    HAVE_OTEL = False


class _NoopSpan:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class _NoopTracer:
    def start_as_current_span(self, *_: Any, **__: Any):
        @contextmanager
        def _cm():
            yield _NoopSpan()

        return _cm()


def init_tracer(app=None):
    """
    Initialize tracing if opentelemetry is available; otherwise install a no-op tracer.
    Must NEVER raise ImportError on clean CI environments.
    """
    if not HAVE_OTEL:
        tracer = _NoopTracer()
        if app is not None and hasattr(app, "state"):
            app.state.tracer = tracer
        return tracer

    # Real wiring (kept minimal; extend if needed)
    provider = TracerProvider()  # type: ignore
    # NOTE: exporter wiring can be added here when available; BatchSpanProcessor optional
    # provider.add_span_processor(BatchSpanProcessor(exporter))
    if trace is not None:
        trace.set_tracer_provider(provider)  # type: ignore
        tracer = trace.get_tracer("alpha_solver")  # type: ignore
    else:
        tracer = _NoopTracer()
    if app is not None and hasattr(app, "state"):
        app.state.tracer = tracer
    return tracer


__all__ = ["init_tracer", "HAVE_OTEL", "_NoopTracer"]

