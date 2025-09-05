from __future__ import annotations
import gzip
import json
from pathlib import Path
from typing import Any, Dict, Optional


class JSONLLogger:
    """Simple JSONL logger with rotation and optional compression."""

    def __init__(self, path: str | Path, max_bytes: int = 1_000_000, compress: bool = True):
        self.path = Path(path)
        self.max_bytes = max_bytes
        self.compress = compress
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = self.path.open("a", encoding="utf-8")

    def _should_rotate(self) -> bool:
        try:
            return self._fh.tell() >= self.max_bytes
        except Exception:
            return False

    def _rotate(self) -> None:
        self._fh.close()
        rotated = self.path.with_suffix(self.path.suffix + ".1")
        if rotated.exists():
            rotated.unlink()
        self.path.rename(rotated)
        if self.compress:
            gz_path = rotated.with_suffix(rotated.suffix + ".gz")
            with rotated.open("rb") as f_in, gzip.open(gz_path, "wb") as f_out:
                f_out.writelines(f_in)
            rotated.unlink()
        self._fh = self.path.open("a", encoding="utf-8")

    def log(self, event: Dict[str, Any]) -> None:
        line = json.dumps(event, ensure_ascii=False)
        self._fh.write(line + "\n")
        self._fh.flush()
        if self._should_rotate():
            self._rotate()

    def close(self) -> None:
        self._fh.close()
