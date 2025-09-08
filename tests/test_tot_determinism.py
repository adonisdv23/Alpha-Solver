"""Determinism and caching tests for Tree-of-Thought solver."""

from __future__ import annotations

from typing import Any, List

import pytest

try:  # Preferred solver factory
    from alpha_solver_entry import get_solver  # type: ignore
except Exception:  # pragma: no cover - fallback when entrypoint missing
    get_solver = None  # type: ignore

try:  # Fallback monolith
    from Alpha_Solver import AlphaSolver  # type: ignore
except Exception:  # pragma: no cover
    AlphaSolver = None  # type: ignore

try:  # Direct TreeOfThought solver fallback
    from alpha.reasoning.tot import TreeOfThoughtSolver
except Exception:  # pragma: no cover
    TreeOfThoughtSolver = None  # type: ignore


def _new_solver(seed: int = 1337):
    if get_solver:
        return get_solver()
    if AlphaSolver is not None:
        return AlphaSolver()
    assert TreeOfThoughtSolver is not None, "TreeOfThoughtSolver not found; adjust import."
    return TreeOfThoughtSolver(seed=seed, branching_factor=3, max_depth=3)


def _solve(solver: Any, query: str, seed: int, cache: dict | None):
    try:
        return solver.solve(query, seed=seed, branching_factor=3, max_depth=3, cache=cache)
    except TypeError:
        return solver.solve(query, cache=cache)


@pytest.mark.parametrize("seed", [1337])
def test_tot_best_path_deterministic(seed: int) -> None:
    """Under a fixed seed the best path and ordering remain stable."""

    solver = _new_solver(seed)
    query = (
        "Break down (15 * 4) + 22 using step-by-step tree-of-thought and return"
        " final integer result."
    )

    best_hashes: List[str] = []
    order_snapshots: List[List[str]] = []

    for _ in range(3):
        result = _solve(solver, query, seed, cache=None)
        tot = result.get("tot", {})
        best = tot.get("best_path", {})
        best_hash = best.get("hash") or result.get("best_path_hash")
        assert best_hash, f"Missing best_path hash in result keys: {list(result.keys())}"
        best_hashes.append(best_hash)

        steps = best.get("steps") or result.get("steps", [])
        if steps and isinstance(steps[0], dict):
            steps = [s.get("text", "") for s in steps]
        order_snapshots.append(list(steps))

        conf = float(result.get("confidence", tot.get("confidence", 0)))
        assert conf >= 0.70, f"Confidence too low: {conf}"

    assert len(set(best_hashes)) == 1, f"Non-deterministic best path: {best_hashes}"
    assert len(set(tuple(s) for s in order_snapshots)) == 1, "Step ordering not stable"


def test_cache_hit_on_second_call() -> None:
    """Second identical call should return cache_hit=True."""

    seed = 1337
    solver = _new_solver(seed)
    cache: dict = {}
    query = "Compute 21 * 3 using ToT."

    r1 = _solve(solver, query, seed, cache)
    cache_hit1 = r1.get("cache_hit", r1.get("tot", {}).get("cache_hit", False))
    assert not cache_hit1, "First call should not be a cache hit"

    r2 = _solve(solver, query, seed, cache)
    cache_hit2 = r2.get("cache_hit", r2.get("tot", {}).get("cache_hit", False))
    assert cache_hit2, "Second call should hit cache"

    sol1 = r1.get("solution") or r1.get("answer")
    sol2 = r2.get("solution") or r2.get("answer")
    assert sol1 == sol2, "Cached solution mismatch"
