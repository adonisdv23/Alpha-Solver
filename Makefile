.PHONY: format test eval gates test-fast test-gates coverage

format:
	@pre-commit run --all-files

test:
        @pytest -q

# Produces artifacts/eval/{summary.json,router_compare.json}
eval:
        @python -m alpha.eval.harness --dataset datasets/mvp_golden.jsonl --seed 42 --compare-baseline

gates: format test eval
        @echo "✅ gates done"

test-fast:
        @pytest -q -k "not slow and not e2e"

test-gates:
        @pytest -q -k determinism --maxfail=1
        @pytest -q -k "policy or pii"
        @pytest -q -k budget
        @pytest -q -k metrics

coverage:
        @pytest --cov=. --cov-report=xml --cov-report=term
