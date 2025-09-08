import json
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:  # Preferred factory
    from alpha_solver_entry import get_solver  # type: ignore
except Exception:  # pragma: no cover - fallback when entrypoint missing
    get_solver = None  # type: ignore

try:  # Fallback monolith module
    from Alpha_Solver import AlphaSolver  # type: ignore
except Exception:  # pragma: no cover
    AlphaSolver = None  # type: ignore


def _new_solver():
    if get_solver:
        return get_solver()
    assert AlphaSolver is not None, "AlphaSolver not found; adjust import."
    return AlphaSolver()


def _solve(solver, query: str, seed: int, cache: dict | None):
    try:
        return solver.solve(query, seed=seed, branching_factor=3, max_depth=3, cache=cache)
    except TypeError:  # pragma: no cover - legacy solvers
        return solver.solve(query, cache=cache)


def main() -> None:
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1337
    query = "Break down (42 + 18) * 2 using ToT and return the final integer only."

    solver = _new_solver()
    cache: dict = {}
    runs = []
    for i in range(3):
        res = _solve(solver, query, seed, cache)
        tot = res.get("tot", {})
        best = tot.get("best_path", {})
        steps = best.get("steps") or res.get("steps", [])
        if steps and isinstance(steps[0], dict):
            steps = [s.get("text", "") for s in steps]
        runs.append(
            {
                "i": i,
                "best_path_hash": best.get("hash") or res.get("best_path_hash"),
                "confidence": res.get("confidence", tot.get("confidence")),
                "steps": steps,
                "cache_hit": res.get("cache_hit", tot.get("cache_hit", False)),
                "response_time_ms": res.get("response_time_ms"),
            }
        )

    all_hash = {r["best_path_hash"] for r in runs}
    all_steps = {tuple(r["steps"]) for r in runs}
    min_conf = min(float(r["confidence"] or 0) for r in runs)

    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "seed": seed,
        "query": query,
        "hashes_equal": (len(all_hash) == 1),
        "ordering_equal": (len(all_steps) == 1),
        "min_confidence": min_conf,
        "runs": runs,
    }

    out = Path("artifacts/determinism_report.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2))
    print(f"Wrote {out}")
    print(
        json.dumps(
            {
                "hashes_equal": report["hashes_equal"],
                "ordering_equal": report["ordering_equal"],
                "min_confidence": report["min_confidence"],
            }
        )
    )
    if not (
        report["hashes_equal"]
        and report["ordering_equal"]
        and report["min_confidence"] >= 0.70
    ):
        sys.exit(2)


if __name__ == "__main__":  # pragma: no cover
    main()
