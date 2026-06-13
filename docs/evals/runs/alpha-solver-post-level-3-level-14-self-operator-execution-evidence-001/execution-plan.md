# Execution Plan

## Selected execution target

Two existing, in-repository, provider-free entry points for the Self Operator were selected:

1. **Self Operator test suite** — `python -m pytest tests/test_self_operator_*.py`
   - 17 test files, 213 tests, exercising the Self Operator modules under `alpha/self_operator/`:
     preflight, dry-run wrapper, execution-gate, release-gate, artifact store, approval, stop-state,
     command classification, result import, acceptance interpretation, import-blocker triage, and the
     static guardrail suites.
2. **Self Operator release-gate checker CLI** — `python scripts/check_self_operator_release_gate.py --repo-root .`
   - A deterministic, operator-invokable command that inspects only local file/directory evidence and
     emits a JSON report.

These were chosen because they are the safest representations of the Self Operator *executing* under the
intended local, operator-supervised flow without any provider, model, token, or network dependency.

## Why this target is safe under the local/offline boundary

The Self Operator package `alpha/self_operator/` is a deterministic, offline-first harness. Verified
properties:

- **No provider/model imports.** No `openai`, `anthropic`, `requests`, or `httpx` imports in the package.
- **No credential/secret/env reads.** The modules do not read `OPENAI_API_KEY`, `MODEL_PROVIDER`,
  `MODEL_SET`, or other provider env vars.
- **No command execution.** Module docstrings state the boundary directly, e.g. `alpha/self_operator/dry_run.py`:
  *"never executes proposed commands or calls external systems"*; `alpha/self_operator/release_gate.py`:
  *"inspects only local file and directory evidence, never runs providers or models, never updates Google
  Sheets, and never mutates source evidence artifacts."*
- **No provider test markers.** The Self Operator tests carry none of the repo's `live` / `openai`
  markers (those gate the single `tests/providers/test_openai_live_smoke.py`, which stays skipped without
  `ALPHA_LIVE_OPENAI=1` and a non-empty key). The Self Operator suite is therefore unaffected by provider
  environment variables.
- **Deterministic.** No RNG or wall-clock dependence in the asserted behavior (timestamp providers are
  injectable in tests).

## Environment setup note (disclosed)

The container started without Python dependencies installed. Test dependencies were installed from PyPI
via `pip install -r requirements.txt -r requirements-test.txt` so the offline test suite could run. This
is **environment setup**, not a provider/model/token/API call. Notably, the base requirements do not
include the OpenAI SDK, product code under `alpha/` and `service/` does not import `openai` directly, and
only the single gated/skipped live-smoke test references it.

## Authoritative validation approach

`OPENAI_API_KEY`, `MODEL_PROVIDER`, and `MODEL_SET` are present in this environment (their values were
never printed; only boolean presence was checked). Consistent with prior repo practice (PR #496), the
authoritative full-suite validation run unsets these:

```
env -u MODEL_PROVIDER -u MODEL_SET -u OPENAI_API_KEY -u OPENAI_BASE_URL python -m pytest -q
```

Provider-related passes or failures are not treated as evidence for this local/offline lane.
