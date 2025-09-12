from __future__ import annotations
import logging

logger = logging.getLogger("alpha-solver.otel")


def init_tracer(app):
    """
    Initialize tracing and instrument the FastAPI app.
    Idempotent and safe if OpenTelemetry is not installed.
    Returns the tracer provider (or None if no-op).
    """
    try:
        # Lazy import so environments without OTEL still work
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    except Exception as exc:  # pragma: no cover - optional dep
        logger.info("OTEL not available; tracing disabled: %s", exc)
        return None

    # Idempotency: if we've already instrumented this app instance, skip
    if getattr(app.state, "_otel_instrumented", False):
        return trace.get_tracer_provider()

    # Ensure a provider is set (tests attach their own span exporter later)
    provider = trace.get_tracer_provider()
    if not isinstance(getattr(provider, "resource", None), Resource):
        resource = Resource.create({"service.name": "alpha-solver"})
        provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(provider)

    # Instrument the FastAPI app with the active provider
    try:
        FastAPIInstrumentor.instrument_app(app, tracer_provider=trace.get_tracer_provider())
    except Exception as exc:  # defensive: do not crash app startup
        logger.warning("Failed to instrument FastAPI app for OTEL: %s", exc)
        return trace.get_tracer_provider()

    app.state._otel_instrumented = True
    logger.info("OTEL FastAPI instrumentation enabled.")
    return trace.get_tracer_provider()
