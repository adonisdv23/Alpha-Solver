.PHONY: run test test-gates fmt lint env-check clean

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
