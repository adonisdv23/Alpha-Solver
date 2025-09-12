from __future__ import annotations


def init_tracer(app, exporter=None):
    class _NoopProcessor:
        def force_flush(self, timeout_millis=None):
            return True

    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor, InMemorySpanExporter

        # Set up tracer provider if not already set
        if not hasattr(app.state, 'tracer_provider'):
            provider = TracerProvider()
            trace.set_tracer_provider(provider)
            app.state.tracer_provider = provider

        # Use provided exporter or default to InMemory
        if exporter is None:
            exporter = InMemorySpanExporter()

        # Create and add processor
        processor = SimpleSpanProcessor(exporter)
        app.state.tracer_provider.add_span_processor(processor)
        app.state.span_processor = processor
        return processor

    except ImportError:
        # OTEL not available, use noop
        processor = _NoopProcessor()
        app.state.span_processor = processor
        return processor
