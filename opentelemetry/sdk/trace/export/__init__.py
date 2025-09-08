class InMemorySpanExporter:
    def __init__(self):
        self._spans = []
    def add_span(self, span):
        self._spans.append(span)
    def get_finished_spans(self):
        return self._spans

__all__ = ["InMemorySpanExporter"]
