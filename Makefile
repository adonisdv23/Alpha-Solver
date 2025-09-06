preflight: ## Validate IDs & registries
	python scripts/preflight.py

test: ## Run tests
	pytest -q

regression: ## Run regression suite
	PYTHONPATH=. python -m alpha.core.regression

sweep: ## Rebuild canon & sweep queries
	python scripts/build_tools_canon.py
	PYTHONPATH=. python scripts/overnight_run.py --regions 'US,EU,APAC' --k 5 --queries docs/queries.txt

plan: ## Plan only (CLI)
	PYTHONPATH=. python -m alpha.cli --plan-only --regions 'US' --k 3 --queries docs/queries.txt

explain: ## Explain mode (CLI)
	PYTHONPATH=. python -m alpha.cli --explain --regions 'US' --k 3 --queries docs/queries.txt

exec: ## Execute local-only (CLI)
	PYTHONPATH=. python -m alpha.cli --execute --regions 'US' --k 3 --queries docs/queries.txt

telemetry: ## Generate telemetry leaderboard
	python scripts/telemetry_leaderboard.py --paths telemetry/*.jsonl --topk 5 --format md --out artifacts/leaderboard.md

quick-audit:
        python scripts/quick_audit.py

exec-test:
	pytest -q tests/test_math_exec.py tests/test_csv_exec.py tests/test_instruction_adapter.py

fmt:
	@echo "Temporary: Black formatting is disabled in CI. Use locally if desired."

fmt-check:
	@echo "Temporary: Black check is disabled in CI. Use locally if desired."

lint:
	ruff check alpha
