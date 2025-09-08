"""Deterministic JSON-backed cache for Tree-of-Thought."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Dict, Any

_DETERMINISTIC = os.getenv("ALPHA_DETERMINISM") == "1"


def load_cache(path: str) -> Dict[str, Any]:
    """Load cache from ``path`` if it exists."""

    p = Path(path)
    if p.exists():
        try:
            with p.open("r", encoding="utf-8") as fh:
                return json.load(fh)
        except json.JSONDecodeError:  # pragma: no cover - corrupt file
            return {}
    return {}


def save_cache(cache: Dict[str, Any], path: str) -> None:
    """Persist ``cache`` to ``path`` creating directories as needed."""

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as fh:
        json.dump(cache, fh, indent=2, sort_keys=True)
        fh.write("\n")


def make_key(query: str, depth: int, branch_path: tuple[str, ...], context_hash: str) -> str:
    """Return a deterministic cache key."""

    stable = json.dumps([query, depth, list(branch_path), context_hash], sort_keys=True)
    return hashlib.sha256(stable.encode("utf-8")).hexdigest()


def get(cache: Dict[str, Any], key: str) -> Any:
    return cache.get(key)


def put(cache: Dict[str, Any], key: str, value: Any) -> None:
    cache[key] = value


__all__ = ["load_cache", "save_cache", "make_key", "get", "put"]
