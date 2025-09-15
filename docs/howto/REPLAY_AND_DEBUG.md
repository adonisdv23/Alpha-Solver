# Replay and Debug

Record and replay solver runs to debug determinism:

```python
from service.replay.recorder import Recorder
from service.replay.player import Player

def run(payload, seed):
    return "ok", {}

rec = Recorder(snapshot_fn=lambda: {"version": 1})
record = rec.record("demo", {"x": 1}, seed=1, run_func=run)
player = Player(snapshot_fn=lambda: {"version": 1})
player.replay(record, run)
```
