# Commands Run

All commands were run locally from the repository root. Exit codes are recorded verbatim. Provider env
var **values were never printed**; only boolean presence was checked.

## 0. Provider env presence (booleans only)

```
python -c "import os;print({k:(k in os.environ) for k in ['MODEL_PROVIDER','MODEL_SET','OPENAI_API_KEY','OPENAI_BASE_URL','ANTHROPIC_API_KEY']})"
```
Output:
```
{'MODEL_PROVIDER': True, 'MODEL_SET': True, 'OPENAI_API_KEY': True, 'OPENAI_BASE_URL': False, 'ANTHROPIC_API_KEY': False}
```

## 1. Environment setup (PyPI; not a provider/model/token call)

```
pip install --disable-pip-version-check -r requirements.txt -r requirements-test.txt
```
Exit code: `0`. Installed pytest 9.0.3, jsonschema 4.26.0, pyyaml, fastapi 0.112.4, httpx 0.27.2,
pydantic 2.13.4, starlette 0.37.2, uvicorn, prometheus-client, opentelemetry-api/sdk, pytest-cov, etc.
The OpenAI SDK is **not** in these requirements and was not installed.

## 2. Self Operator release-gate checker CLI (local file inspection only)

```
python scripts/check_self_operator_release_gate.py --repo-root . --output artifacts/self-operator-release-gate-report.json
```
Exit code: `0`. `final_status: eligible_for_release_closeout_review`; `ready: true (does not claim MVP
readiness)`; 11/11 gates `pass`. Full output and JSON in `execution-results.md` / `artifacts-index.md`.

## 3. Enumerate Self Operator test files, then run the suite (offline/deterministic)

First enumerate the exact files the glob resolves to (so the suite target is explicit and auditable):

```
python - <<'PY'
from pathlib import Path
for p in sorted(Path("tests").glob("test_self_operator_*.py")):
    print(p)
PY
```
Output (17 files):
```
tests/test_self_operator_acceptance_interpretation.py
tests/test_self_operator_approval.py
tests/test_self_operator_approval_stopstate_static.py
tests/test_self_operator_artifact_schema.py
tests/test_self_operator_artifact_schema_static.py
tests/test_self_operator_artifact_store.py
tests/test_self_operator_closeout_guardrails.py
tests/test_self_operator_command_classification.py
tests/test_self_operator_dry_run.py
tests/test_self_operator_execution_gate.py
tests/test_self_operator_forbidden_behavior_static.py
tests/test_self_operator_import_blocker_triage.py
tests/test_self_operator_preflight.py
tests/test_self_operator_release_gate.py
tests/test_self_operator_result_import.py
tests/test_self_operator_static_guardrails.py
tests/test_self_operator_stop_state.py
```

Then run the suite over exactly those files:

```
python -m pytest tests/test_self_operator_*.py -q --junit-xml=artifacts/self-operator-pytest-junit.xml
```
Exit code: `0`. Exact counts captured via JUnit XML (`--junit-xml=artifacts/self-operator-pytest-junit.xml`): **213 collected, 213 passed, 0
failed, 0 errors, 0 skipped** (1.43s).

## 4. Authoritative full-suite validation (provider env unset)

```
env -u MODEL_PROVIDER -u MODEL_SET -u OPENAI_API_KEY -u OPENAI_BASE_URL python -m pytest -q --junit-xml=artifacts/provider-env-unset-full-suite-junit.xml
```
Exit code: `1`. Exact counts via JUnit XML (`--junit-xml=artifacts/provider-env-unset-full-suite-junit.xml`): **1216 collected, 1211 passed, 2 failed, 0 errors, 3
skipped** (37.75s). Consistent with the PR #496 recorded full-suite behavior, the provider-env-unset full
suite still reports the same two unrelated failures (see `failure-analysis.md`).

## 5. Static guardrail checkers (run after this packet was created)

```
python scripts/check_local_llm_doc_paths.py
python scripts/check_local_llm_evidence_boundaries.py
python scripts/check_local_llm_packet_consistency.py
```
Results are recorded in `execution-results.md` (Validation section).

## Notes

- No command called OpenAI, Anthropic, any hosted provider, any local model, or any external API.
- No `/v1/solve` call, no dashboard, no browser automation, no Google Sheets, no deployment, no billing.
- The release-gate CLI's `--output artifacts/self-operator-release-gate-report.json` path was directed into an `artifacts/` path that the
  repo `.gitignore` excludes; the report content is therefore embedded in `artifacts-index.md` instead of
  committed as a separate file, keeping this packet markdown-only (consistent with PR #496).
