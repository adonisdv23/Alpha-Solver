class _NoopExporter:
    def export(self, spans):  # pragma: no cover
        return True

class SimpleSpanProcessor:
    def __init__(self, exporter=None):
        self._exporter = exporter or _NoopExporter()
    def force_flush(self):
        return True

def init_tracer(app, exporter=None):
    proc = getattr(app.state, "span_processor", None)
    if proc is not None:
        return proc
    proc = SimpleSpanProcessor(exporter)
    app.state.span_processor = proc
    return proc
