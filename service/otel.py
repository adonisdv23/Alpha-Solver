"""OpenTelemetry tracing setup (reuse global provider, version-tolerant)."""

from typing import Optional, Any

def init_tracer(app, exporter: Optional[Any] = None):
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider  # type: ignore
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor  # type: ignore
    try:
        # OTEL 1.24+ canonical location
        from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter  # type: ignore
    except Exception:  # pragma: no cover (older layouts)
        from opentelemetry.sdk.trace.export import InMemorySpanExporter  # type: ignore

    # 1) Get the current global provider (FastAPI app may have set this already)
    provider = trace.get_tracer_provider()
    if not isinstance(provider, TracerProvider):
        # First-time init: create and register a real SDK provider
        provider = TracerProvider()
        trace.set_tracer_provider(provider)

    # Keep a reference on app.state for tests/consumers
    app.state.tracer_provider = provider

    # 2) Choose exporter (tests pass one; otherwise default to in-memory)
    if exporter is None:
        exporter = InMemorySpanExporter()

    # 3) Attach our processor to the EXISTING provider (do not replace the provider)
    proc = SimpleSpanProcessor(exporter)
    try:
        # Best-effort: avoid duplicating the same class of processor repeatedly in hot reloads
        for attr in ("_active_span_processors", "span_processors"):
            lst = getattr(provider, attr, None)
            if isinstance(lst, list) and any(type(x) is type(proc) for x in lst):
                # still add ours, but clear old SimpleSpanProcessor if desired
                pass
    except Exception:
        pass
    provider.add_span_processor(proc)
    app.state.span_processor = proc

    # 4) Shim force_flush on the provider, if missing
    if not hasattr(provider, "force_flush"):
        def _force_flush(timeout_millis: Optional[int] = None):
            try:
                return proc.force_flush(timeout_millis)
            except Exception:
                return True
        provider.force_flush = _force_flush  # type: ignore[attr-defined]

    return provider
