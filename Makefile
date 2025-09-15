.PHONY: run test test-gates fmt lint env-check clean smoke release

run:
	uvicorn service.app:app --host 0.0.0.0 --port 8000

test:
	pytest -q

test-gates:
	pytest -q -k "determinism or policy or budget or metrics"

fmt:
	black . >/dev/null 2>&1 || echo "black not installed"
	ruff --fix . >/dev/null 2>&1 || echo "ruff not installed"

lint:
	ruff . >/dev/null 2>&1 || echo "ruff not installed"

env-check:
	python scripts/check_env.py

clean:
	rm -rf **/__pycache__ .pytest_cache .ruff_cache

smoke:
	python -c "from tests.test_smoke_quickstart import run_smoke_suite; run_smoke_suite()"

release:
	python scripts/release.py --version 0.1.0

.PHONY: cli cli-test

cli:
	python cli/alpha_solver_cli.py --help

cli-test:
	pytest tests/test_cli_*.py --cov=cli --cov-report=term-missing
