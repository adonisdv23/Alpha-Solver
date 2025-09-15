# Replay and Debug

The replay harness captures and verifies event sequences.

```python
from alpha.core.replay import ReplayHarness
h = ReplayHarness(base_dir="artifacts/replay_tmp")
# ... record events ...
h.save("session")
```

For debugging spans and metrics:

```python
from service.otel import init_tracer, span, get_exported_spans
init_tracer()
with span("debug"):
    pass
print(get_exported_spans())
```
