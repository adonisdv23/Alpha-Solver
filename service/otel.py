from __future__ import annotations
import logging

logger = logging.getLogger("alpha-solver.otel")


def init_tracer(app, exporter=None):
    """Initialize tracing and instrument the FastAPI app.
    Idempotent and safe if OpenTelemetry is not installed.
    Returns the span processor (or None if no-op).
    """

    if getattr(app.state, "otel_ready", False):
        return getattr(app.state, "span_processor", None)

    try:  # pragma: no cover - optional dep
        from opentelemetry import trace
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import (
            InMemorySpanExporter,
            SimpleSpanProcessor,
        )
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    except Exception as exc:
        logger.info("OTEL not available; tracing disabled: %s", exc)
        app.state.tracer_provider = None
        app.state.span_processor = None
        app.state.otel_ready = False
        return None

    provider = trace.get_tracer_provider()
    if not isinstance(provider, TracerProvider):
        resource = Resource.create({"service.name": "alpha-solver"})
        provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(provider)

    proc = SimpleSpanProcessor(exporter or InMemorySpanExporter())
    provider.add_span_processor(proc)

    try:  # defensive: do not crash app startup
        FastAPIInstrumentor().instrument_app(app)
    except Exception as exc:
        logger.warning("Failed to instrument FastAPI app for OTEL: %s", exc)

    app.state.tracer_provider = provider
    app.state.span_processor = proc
    app.state.otel_ready = True
    return proc
