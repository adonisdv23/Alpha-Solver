help:
	@echo "Targets: run, sweep, telemetry, golden, test"

run:
	python -m alpha.cli run --queries "demo query" --regions US --plan-only --seed 1234 || true

sweep:
	python -m alpha.cli run --queries-file docs/queries.sample.txt --regions US EU --explain || true

telemetry:
	python scripts/telemetry_leaderboard.py --paths telemetry/*.jsonl --topk 5 --format md || true

golden:
	pytest -q tests/test_golden_scenarios.py

test:
	pytest -q
