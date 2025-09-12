from __future__ import annotations
import logging

logger = logging.getLogger("alpha-solver.otel")


def init_tracer(app, exporter=None):
    """Initialize tracing and instrument the FastAPI app.
    Idempotent and safe if OpenTelemetry is not installed.
    Returns the tracer provider (or None if no-op).
    """
    existing = getattr(app.state, "tracer_provider", None)
    if existing:
        return existing

    try:
        from opentelemetry import trace
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    except Exception as exc:  # pragma: no cover - optional dep
        logger.info("OTEL not available; tracing disabled: %s", exc)
        app.state.tracer_provider = None
        return None

    resource = Resource.create({"service.name": "alpha-solver"})
    provider = TracerProvider(resource=resource)
    if exporter is not None:
        try:
            provider.add_span_processor(SimpleSpanProcessor(exporter))
        except Exception as exc:  # defensive: exporter errors shouldn't crash
            logger.warning("Failed to attach OTEL exporter: %s", exc)
    trace.set_tracer_provider(provider)

    try:
        FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)
    except Exception as exc:  # defensive: do not crash app startup
        logger.warning("Failed to instrument FastAPI app for OTEL: %s", exc)

    app.state.tracer_provider = provider
    logger.info("OTEL FastAPI instrumentation enabled.")
    return provider
