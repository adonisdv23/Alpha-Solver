# Alpha Solver Constrained Environment

## Quick Start
```
python 'Alpha Solver.py'
python test_alpha_solver_smoke.py
```
The main script runs entirely with bundled fallbacks when third‑party modules are missing.
Both commands emit logs under `logs/` and benchmark data under `benchmarks/`.

## Feature Matrix
| Feature | Real | Fallback |
| --- | --- | --- |
| Logging | jsonlines | jsonlines_compat |
| Telemetry | aiohttp client | local JSONL nullsink |
| Benchmarking | psutil | tracemalloc |
| Replay | gzip compression | plain JSON if gzip unavailable |

## Troubleshooting
| Symptom | Cause | Fix |
| --- | --- | --- |
| Import error | files missing | ensure repo checked out fully |
| No logs | filesystem read-only | run on writable volume |
| Benchmark slow | high iterations | set `CI=true` env for short run |

## Exit Codes
0 on success.
Artifacts written to `logs/` and `benchmarks/`.
