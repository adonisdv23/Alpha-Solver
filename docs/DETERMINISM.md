# Determinism

The determinism harness (**NEW-015**) ensures runs are repeatable.

## Harness usage

```bash
pytest -q -k determinism
# or in code
from service.determinism.harness import DeterminismHarness
DeterminismHarness(...).run_replay(["out/events.jsonl"])
```

## CI gate

CI fails on any flap: outputs, events, or metrics must match between runs. Noise injection is disabled; differing keys trigger a gate failure.

