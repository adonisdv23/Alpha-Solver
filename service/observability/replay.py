from __future__ import annotations

import json
import os
from typing import Any, Callable, Dict, Iterator, List, Optional


class ReplayHarness:
    """Utilities to replay JSONL logs."""

    def __init__(self, log_path: str) -> None:
        self.log_path = log_path

    # ------------------------------------------------------------------
    def _log_files(self) -> List[str]:
        files: List[str] = []
        idx = 1
        while os.path.exists(f"{self.log_path}.{idx}"):
            files.append(f"{self.log_path}.{idx}")
            idx += 1
        if os.path.exists(self.log_path):
            files.append(self.log_path)
        return files

    # ------------------------------------------------------------------
    def iter_events(self, name: Optional[str] = None) -> Iterator[Dict[str, Any]]:
        for path in self._log_files():
            with open(path, encoding="utf-8") as fp:
                for line in fp:
                    line = line.strip()
                    if not line:
                        continue
                    event = json.loads(line)
                    if name is None or event.get("name") == name:
                        yield event

    # ------------------------------------------------------------------
    def _matches(self, data: Dict[str, Any], where: Dict[str, Any]) -> bool:
        for k, v in where.items():
            if k not in data:
                return False
            dv = data[k]
            if isinstance(v, dict) and isinstance(dv, dict):
                if not self._matches(dv, v):
                    return False
            else:
                if dv != v:
                    return False
        return True

    def filter(
        self, *, name: Optional[str] = None, where: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        events = list(self.iter_events(name))
        if where is None:
            return events
        return [e for e in events if self._matches(e, where)]

    # ------------------------------------------------------------------
    def to_requests(
        self, *, name: str, extractor: Callable[[Dict[str, Any]], Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        return [extractor(e) for e in self.iter_events(name)]
