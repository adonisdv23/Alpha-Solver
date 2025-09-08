help:
	@echo "Targets: run, sweep, telemetry, golden, test, preflight, dev-venv, release-notes"

run:
	python -m alpha.cli run --queries "demo query" --regions US --plan-only --seed 1234 || true

sweep:
	python -m alpha.cli run --queries-file docs/queries.sample.txt --regions US EU --explain || true

policy-dry-run:
	python -m alpha.cli run --queries "demo" --policy-dry-run --budget-max-steps 3 --breaker-max-fails 1 || true

telemetry:
	python scripts/telemetry_leaderboard.py --paths telemetry/*.jsonl --format all || true
	sleep 1 && python scripts/overview_md.py || true

replay:
	python scripts/replay.py --plan artifacts/last_plan.json || true

bench:
	python scripts/bench.py --queries-file docs/queries.sample.txt --regions US --repeat 2 || true

nightly-local:
	ALPHA_DETERMINISM=1 GIT_COMMIT_SHA=$$(git rev-parse --short HEAD) python -m alpha.cli run --queries-file docs/queries.sample.txt --regions US --seed 1234 --plan-only || true
	$(MAKE) telemetry

golden:
	pytest -q tests/test_golden_scenarios.py

test:
	pytest -q

preflight:
	python scripts/preflight.py

dev-venv:
	python -m venv .venv && .venv/bin/pip install -r requirements.txt -r requirements-dev.txt

release-notes:
	python scripts/gen_release_notes.py

build:
	python -m build

dist:
	@ls -l dist || true

tag-release:
	@[ -n "$$V" ] || (echo "Usage: make tag-release V=1.0.1"; exit 2)
	python scripts/tag_release.py --version $$V

version-bump:
	@[ -n "$$PART" ] || (echo "Usage: make version-bump PART=patch|minor|major|prerelease"; exit 2)
	python scripts/bump_version.py --part $$PART

release:
	@echo "See RELEASE.md for steps. Push tag to trigger CI release."

.PHONY: test-determinism verify-determinism

test-determinism:
	pytest -q tests/test_tot_determinism.py

verify-determinism:
	python scripts/verify_tot_determinism.py 1337 && cat artifacts/determinism_report.json
