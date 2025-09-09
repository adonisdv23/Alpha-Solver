CONTENT_TYPE_LATEST = "text/plain; version=0.0.4"

_REGISTRY = []

class _Metric:
    def __init__(self, name: str, *args, **kwargs):
        self.name = name
        self.value = 0
        _REGISTRY.append(self)
    def labels(self, *args, **kwargs):  # pragma: no cover - trivial
        return self

class Counter(_Metric):
    def inc(self, amount: float = 1) -> None:
        self.value += amount

class Histogram(_Metric):
    def observe(self, value: float) -> None:
        self.value = value

def generate_latest() -> bytes:
    metrics = [f"{m.name} {m.value}" for m in _REGISTRY]
    return "\n".join(metrics).encode()

def start_http_server(port: int) -> None:  # pragma: no cover - noop
    return None
