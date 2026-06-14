# Validation evidence

## Commands run

| Command | Result | Notes |
| --- | --- | --- |
| `python -m pip check` | Pass | Installed environment reported no broken requirements. |
| `python -m pip list --format=json > /tmp/alpha_solver_pip_list.json` | Pass | Captured installed environment package list outside the repo to avoid committing environment-specific noise. |
| `python -m pip freeze > /tmp/alpha_solver_pip_freeze.txt` | Pass | Captured installed environment freeze outside the repo for local validation only. |
| `python - <<'PY' ... packaging specifier check ... PY` | Pass | Verified `constraints.txt` pinned values satisfy root `requirements.txt` specifiers for overlapping packages. |
| `python -m pytest -q tests/test_requirements_parity.py` | Fail | Requested focused parity check could not run because `tests/test_requirements_parity.py` is not present in this checkout. |
| `python -m pytest -q` | Fail | Full suite completed with 5 failures unrelated to this docs-only packet: three provider model expectation failures in `tests/test_api_endpoints.py`, one cost tracking failure in `tests/test_cost_tracking.py`, and one security validation failure in `tests/test_security.py`. |
| `python - <<'PY' ... packet file check ... PY` | Pass | Verified all required packet files exist. |
| `python - <<'PY' ... markdown no trailing whitespace check ... PY` | Pass | Checked new packet Markdown files for trailing whitespace. |

## Dependency check summary

- The installed local environment did not report broken Python package requirements.
- The existing constraints file pins overlap the root runtime requirements without violating their declared ranges.
- Full pytest did not pass in this environment; observed failures are recorded above and are outside this packet's docs-only dependency-provenance changes.
- This lane did not perform a network vulnerability audit, SBOM generation, Docker build, or provider call intentionally. The full-suite run did exercise an existing test path that made an HTTP request to OpenAI in the local environment; this lane did not add or authorize provider-calling behavior.

## Static docs check summary

- All required evidence packet files are present.
- New packet Markdown files passed a focused trailing-whitespace check.
