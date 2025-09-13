"""Minimal OpenTelemetry setup that wires a SimpleSpanProcessor to the given exporter."""

from typing import Optional, Any

def init_tracer(app, exporter: Optional[Any] = None):
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor, InMemorySpanExporter

    # Fresh provider if we pass a custom exporter (tests); otherwise reuse if present
    provider = getattr(app.state, "tracer_provider", None)
    if exporter is not None or not isinstance(provider, TracerProvider):
        provider = TracerProvider()
        trace.set_tracer_provider(provider)
        app.state.tracer_provider = provider

    if exporter is None:
        exporter = InMemorySpanExporter()

    # Replace processors so the test's exporter is the one receiving spans
    try:
        provider._active_span_processor = None  # type: ignore[attr-defined]
    except Exception:
        pass
    for sp in getattr(provider, "_active_span_processors", []) or []:
        try:
            provider._active_span_processors.remove(sp)
        except Exception:
            pass
    proc = SimpleSpanProcessor(exporter)
    provider.add_span_processor(proc)
    app.state.span_processor = proc

    # Some OTEL builds don’t expose provider.force_flush; provide a small shim
    if not hasattr(provider, "force_flush"):
        def _force_flush(timeout_millis: Optional[int] = None):
            try:
                return proc.force_flush(timeout_millis)
            except Exception:
                return True
        provider.force_flush = _force_flush  # type: ignore[attr-defined]

    return provider
