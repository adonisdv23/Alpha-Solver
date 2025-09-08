from __future__ import annotations
import gzip
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional


@dataclass
class ReplaySession:
    session_id: str
    events: List[Dict[str, object]] = field(default_factory=list)


class ReplayHarness:
    def __init__(self, base_dir: str | Path = "artifacts/replay"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.events: List[Dict[str, object]] = []
        self._replay_iter: Optional[Iterator[Dict[str, object]]] = None

    def record(self, event: Dict[str, object]) -> None:
        self.events.append(event)

    def save(self, session_id: str | None = None) -> str:
        session_id = session_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path = self.base_dir / f"{session_id}.jsonl.gz"
        with gzip.open(path, "wt", encoding="utf-8") as f:
            for ev in self.events:
                f.write(json.dumps(ev) + "\n")
        return session_id

    def load(self, session_id: str) -> ReplaySession:
        path = self.base_dir / f"{session_id}.jsonl.gz"
        events = [json.loads(line) for line in gzip.open(path, "rt", encoding="utf-8")]
        return ReplaySession(session_id=session_id, events=events)

    def load_for_replay(self, session_id: str) -> None:
        session = self.load(session_id)
        self._replay_iter = iter(session.events)

    def verify(self, event: Dict[str, object]) -> None:
        if self._replay_iter is None:
            return
        expected = next(self._replay_iter, None)
        if expected is None:
            return
        ignore = {"timestamp", "session_id"}
        exp = {k: v for k, v in expected.items() if k not in ignore}
        cur = {k: v for k, v in event.items() if k not in ignore}
        exp_norm = json.loads(json.dumps(exp, sort_keys=True))
        cur_norm = json.loads(json.dumps(cur, sort_keys=True))
        if exp_norm != cur_norm:
            raise AssertionError("Replay mismatch")

    def replay(self, session: ReplaySession) -> Iterable[Dict[str, object]]:
        for ev in session.events:
            yield ev
