"""Helper utilities for basic evaluation metrics."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Dict, Iterable, List


def compute_token_savings(baseline_stats: Dict[str, int], new_stats: Dict[str, int]) -> float:
    """Return percentage token savings between two runs.

    ``baseline_stats`` and ``new_stats`` must contain a ``tokens`` integer.
    The result is a fraction in ``[0, 1]``.
    """
    base = int(baseline_stats.get("tokens", 0))
    new = int(new_stats.get("tokens", 0))
    if base <= 0:
        return 0.0
    return max(0.0, (base - new) / base)


def aggregate_tokens(stats: Iterable[Dict[str, int]]) -> int:
    """Sum ``tokens`` from each stats mapping."""

    return sum(int(s.get("tokens", 0)) for s in stats)


def latency_percentile(latencies: List[int], pct: float) -> float:
    """Return the ``pct`` percentile from ``latencies``.

    A tiny helper to avoid pulling heavy dependencies.
    """

    if not latencies:
        return 0.0
    latencies = sorted(latencies)
    k = int(round((pct / 100) * (len(latencies) - 1)))
    return float(latencies[k])


def determinism_hash(path: Path | str) -> str:
    """Return a sha256 hash of the file at ``path``."""

    return sha256(Path(path).read_bytes()).hexdigest()


def determinism_verdict(hash_a: str, hash_b: str) -> bool:
    """True when two hashes match exactly."""

    return hash_a == hash_b


__all__ = [
    "compute_token_savings",
    "aggregate_tokens",
    "latency_percentile",
    "determinism_hash",
    "determinism_verdict",
]
