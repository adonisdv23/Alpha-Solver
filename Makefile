help:
        @echo "Targets: run, sweep, telemetry, golden, test, preflight, dev-venv, release-notes"

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

preflight:
        python scripts/preflight.py

dev-venv:
        python -m venv .venv && .venv/bin/pip install -r requirements.txt -r requirements-dev.txt

release-notes:
        @cat RELEASE.md
