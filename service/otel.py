"""Minimal tracing helpers for the service."""

from opentelemetry import trace
from opentelemetry.sdk.trace.export import InMemorySpanExporter


class SimpleTracerProvider:
    def __init__(self, exporter: InMemorySpanExporter):
        self.exporter = exporter
    def add_span(self, name: str):
        self.exporter.add_span({"name": name})
    def force_flush(self):
        pass


def init_tracer(app, exporter: InMemorySpanExporter | None = None) -> SimpleTracerProvider:
    exporter = exporter or InMemorySpanExporter()
    provider = SimpleTracerProvider(exporter)
    trace.set_tracer_provider(provider)
    app.state.tracer_provider = provider
    return provider


__all__ = ["init_tracer"]
