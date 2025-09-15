# Replay Guide

This project supports deterministic record and replay of request pipelines.

## Recording

```python
from service.replay.recorder import Recorder
from my_pipeline import run_pipeline

recorder = Recorder()
record = recorder.record(
    "sample", {"query": "hello"}, seed=1, run_func=run_pipeline
)
```

`record` contains the sanitized request, options, snapshot metadata and
stable hash of critical fields.

## Replaying

```python
from service.replay.player import Player
player = Player()
player.replay(record, run_pipeline)
```

Replay recomputes the snapshot and hash and raises `ReplayMismatch` if any
field deviates.  Differences are reported concisely as canonical JSON.

## Diffing

When a replay mismatch occurs, the raised error contains the differing keys,
including score changes and budget verdicts.  This helps focus debugging on
what changed without noisy timestamps.

## CI Gate

Set `REPLAY_CI=1` to enable the fast replay stability check in CI.  Any flap
causes the gate to fail.

## Snapshot

The recorder embeds a minimal snapshot of environment state such as registry
SHAs and gate configuration.  If any of these change, the replay hash also
changes, providing hardening against accidental drift.
