# Source evidence reviewed

## Commands used for source review

- `git status --short`
- `git branch --show-current`
- `find alpha service cli scripts tests docs/local_llm_solver_orchestration_operator_guide .github/workflows -maxdepth 3 -type f | sort`
- `sed -n '1,220p' docs/ENTRYPOINTS.md`
- `rg -n "check-local|local-llm|orchestration|guardrail|pytest|ci|lint|eval" Makefile scripts docs .github tests pyproject.toml`
- `sed -n '1,220p' alpha/local_llm/operator_cli.py`
- `sed -n '1,220p' alpha/local_llm/orchestration_runner.py`
- `sed -n '1,180p' .specs/LOCAL-LLM-SOLVER-ORCHESTRATION-001.md`
- `sed -n '1,160p' .specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md`

## Evidence reviewed

- Entrypoint role documentation identifies the portable behavior contract, modular/reference compatibility entrypoint, import bridge, root CLI wrapper, and command-oriented CLI as distinct surfaces that must not be casually merged or renamed.
- `alpha/local_llm/operator_cli.py` is an operator-only, default-off, local-only CLI wrapper that delegates to the local orchestration runner and states that it does not expose production solver, dashboard, hosted fallback, or provider fallback paths.
- `alpha/local_llm/orchestration_runner.py` is a non-production local solver orchestration runner that reuses the approved local LLM runtime config/backend path and preserves the non-evidence local runtime boundary.
- `.specs/LOCAL-LLM-SOLVER-ORCHESTRATION-001.md` and `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md` define important default-off, local-only, fail-closed, non-evidence, and no-silent-hosted-fallback constraints.
- `Makefile` exposes `check-local-llm-orchestration-guardrails`, which runs local LLM evidence-boundary, doc-path, and packet-consistency checks.
- `.github/workflows/ci.yml` runs the local LLM orchestration guardrail suite before the broader test suite.
- Focused tests already exist for local LLM operator CLI, runner, provider adapter, runtime integration, doc paths, evidence boundaries, and packet consistency.

## Review limits

This review was static and local. It did not run a local model, call Ollama, call hosted providers, exercise `/v1/solve`, exercise dashboard routes, deploy, benchmark, generate artifacts, or inspect credentials.
