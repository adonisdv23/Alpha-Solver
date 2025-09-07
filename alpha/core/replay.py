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
    """Utility for recording and replaying solver sessions."""

    def __init__(self, base_dir: str | Path = "artifacts/replay", session_id: str | None = None):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.events: List[Dict[str, object]] = []
        self.session_id = session_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    def record(self, event: Dict[str, object]) -> None:
        self.events.append(event)

    def save(self) -> str:
        """Persist recorded events and return the session identifier."""
        path = self.base_dir / f"{self.session_id}.jsonl.gz"
        with gzip.open(path, "wt", encoding="utf-8") as f:
            for ev in self.events:
                f.write(json.dumps(ev) + "\n")
        return self.session_id

    def load(self, session_id: str) -> ReplaySession:
        path = self.base_dir / f"{session_id}.jsonl.gz"
        events = [json.loads(line) for line in gzip.open(path, "rt", encoding="utf-8")]
        self.session_id = session_id
        return ReplaySession(session_id=session_id, events=events)

    def replay(self, session: ReplaySession) -> Iterable[Dict[str, object]]:
        for ev in session.events:
            yield ev
