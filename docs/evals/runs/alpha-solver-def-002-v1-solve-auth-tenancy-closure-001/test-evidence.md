# Test Evidence

Targeted tests run:

```text
python -m pytest -q tests/test_v1_solve_auth_tenancy_boundary.py tests/test_api_auth_ratelimit.py tests/test_default_credentials_hardening.py
```

Static compile and documentation checks run:

```text
python -m py_compile alpha/core/config.py service/app.py
python scripts/check_local_llm_doc_paths.py
python scripts/check_local_llm_evidence_boundaries.py
python scripts/check_local_llm_packet_consistency.py
git diff --check
```

Static evidence/spec presence check run:

```text
python - <<'PY'
from pathlib import Path
required = [
    'README.md', 'implementation-summary.md', 'v1-solve-boundary-evidence.md',
    'test-evidence.md', 'residual-risks.md', 'selected-next-lane.md',
    'evidence-boundary.md', 'non-actions.md',
]
root = Path('docs/evals/runs/alpha-solver-def-002-v1-solve-auth-tenancy-closure-001')
missing = [name for name in required if not (root / name).is_file()]
assert not missing, missing
assert 'ALPHA-SOLVER-DEF-002-V1-SOLVE-AUTH-TENANCY-CLOSURE-001.md' in Path('.specs/INDEX.md').read_text()
PY
```
