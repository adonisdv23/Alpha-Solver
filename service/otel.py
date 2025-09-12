from __future__ import annotations

try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor, InMemorySpanExporter
except Exception:  # pragma: no cover - optional dependency shim
    class TracerProvider:
        def add_span_processor(self, processor):
            pass
    class SimpleSpanProcessor:
        def __init__(self, exporter):
            self._exporter = exporter
        def force_flush(self):
            pass
    class InMemorySpanExporter:
        def export(self, spans):
            pass
    class _Trace:
        _provider = None
        @staticmethod
        def set_tracer_provider(provider):
            _Trace._provider = provider
        @staticmethod
        def get_tracer_provider():
            return _Trace._provider
    trace = _Trace()


def init_tracer(app, exporter=None):
    """
    Idempotently ensure a TracerProvider is set, attach a span processor, and
    return the processor so tests can call .force_flush().
    This remains OTEL-optional; if initialization fails, we still return a
    dummy in-memory processor so callers never get None.
    """
    provider = getattr(app.state, "tracer_provider", None)
    if not isinstance(provider, TracerProvider):
        provider = TracerProvider()
        trace.set_tracer_provider(provider)
        app.state.tracer_provider = provider

    if exporter is None:
        exporter = InMemorySpanExporter()

    processor = SimpleSpanProcessor(exporter)
    provider.add_span_processor(processor)
    app.state.span_processor = processor
    return processor
