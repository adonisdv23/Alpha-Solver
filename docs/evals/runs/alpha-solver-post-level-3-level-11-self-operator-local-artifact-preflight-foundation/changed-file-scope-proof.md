# Changed-file scope proof

Allowed source/helper scope:

- `alpha/self_operator/__init__.py`
- `alpha/self_operator/artifact_schema.py`
- `alpha/self_operator/artifact_store.py`
- `alpha/self_operator/command_classification.py`
- `alpha/self_operator/preflight.py`
- `alpha/self_operator/redaction.py`
- `pyproject.toml` package registration for `alpha.self_operator`

Allowed tests and inert fixtures:

- `tests/test_self_operator_artifact_schema.py`
- `tests/test_self_operator_artifact_store.py`
- `tests/test_self_operator_command_classification.py`
- `tests/test_self_operator_preflight.py`
- `tests/fixtures/self_operator_artifacts/*.json`
- `tests/fixtures/self_operator_preflight/*.json`

Allowed docs packet:

- `docs/evals/runs/alpha-solver-post-level-3-level-11-self-operator-local-artifact-preflight-foundation/*.md`

No provider, API, dashboard, CLI behavior, credential, deployment, billing, browser, Google Sheets, source-artifact, evidence-promotion, or acceptance files were changed.
