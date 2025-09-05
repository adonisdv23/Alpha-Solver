from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def timestamp_rfc3339z() -> str:
    """Return current UTC timestamp in RFC3339 format with Z suffix."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def ensure_dir(path: str | Path) -> Path:
    """Ensure directory exists and return Path."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_json_atomic(path: str | Path, obj: Any) -> Path:
    """Write JSON to path atomically.

    A temporary file is written then moved into place to avoid partial writes.
    """
    p = Path(path)
    ensure_dir(p.parent)
    tmp = p.with_suffix(p.suffix + '.tmp')
    with tmp.open('w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2)
    tmp.replace(p)
    return p
