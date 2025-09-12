from __future__ import annotations


class _NoopProcessor:
    def force_flush(self, timeout_millis: int | None = None) -> bool:  # pragma: no cover
        return True


def init_tracer(app, exporter=None):
    proc = getattr(app.state, "span_processor", None)
    if proc is not None:
        return proc

    try:  # try real OTEL
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import (
            InMemorySpanExporter,
            SimpleSpanProcessor,
        )
    except Exception:  # pragma: no cover - optional dep
        proc = _NoopProcessor()
        app.state.span_processor = proc
        return proc

    provider = getattr(app.state, "tracer_provider", None)
    if provider is None or not isinstance(provider, TracerProvider):
        provider = TracerProvider()
        trace.set_tracer_provider(provider)
        app.state.tracer_provider = provider

    if exporter is None:
        exporter = InMemorySpanExporter()

    proc = SimpleSpanProcessor(exporter)
    provider.add_span_processor(proc)
    app.state.span_processor = proc
    return proc

