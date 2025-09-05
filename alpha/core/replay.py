from __future__ import annotations
import gzip
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


@dataclass
class ReplaySession:
    session_id: str
    events: List[Dict[str, object]] = field(default_factory=list)


class ReplayHarness:
    def __init__(self, base_dir: str | Path = "artifacts/replay"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.events: List[Dict[str, object]] = []

    def record(self, event: Dict[str, object]) -> None:
        self.events.append(event)

    def save(self) -> str:
        session_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path = self.base_dir / f"{session_id}.jsonl.gz"
        with gzip.open(path, "wt", encoding="utf-8") as f:
            for ev in self.events:
                f.write(json.dumps(ev) + "\n")
        return session_id

    def load(self, session_id: str) -> ReplaySession:
        path = self.base_dir / f"{session_id}.jsonl.gz"
        events = [json.loads(line) for line in gzip.open(path, "rt", encoding="utf-8")]
        return ReplaySession(session_id=session_id, events=events)

    def replay(self, session: ReplaySession) -> Iterable[Dict[str, object]]:
        for ev in session.events:
            yield ev
