# ToT Determinism & Caching Verification

- Fixed seed: 1337
- 3 consecutive runs must produce:
  - identical `best_path_hash`
  - identical ordered `steps`
  - `confidence >= 0.70`
- Second identical call should return `cache_hit=True`.

Run:
- `make test-determinism`
- `make verify-determinism`
Artifacts:
- `artifacts/determinism_report.json`
