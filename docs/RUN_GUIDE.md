# Run Guide

Quick commands to exercise the Alpha Solver bundle:

```
make preflight
make canon
python 'Alpha Solver.py' --tools-canon artifacts/tools_canon.csv --region EU --k 5 --deterministic --no-benchmark --no-telemetry
make report
make test
```
