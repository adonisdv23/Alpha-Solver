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

## ToT determinism and caching verification

The legacy ToT determinism checklist from the former lowercase duplicate is preserved here for continuity:

- Fixed seed: 1337
- 3 consecutive runs must produce:
  - identical `best_path_hash`
  - identical ordered `steps`
  - `confidence >= 0.70`
- Second identical call should return `cache_hit=True`.

Run:

- `make test-determinism`
- `make verify-determinism`

Artifacts:

- `artifacts/determinism_report.json`
