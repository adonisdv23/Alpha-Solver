.PHONY: format test eval gates

format:
	@pre-commit run --all-files

test:
	@pytest -q

# Produces artifacts/eval/{summary.json,router_compare.json}
eval:
	@python -m alpha.eval.harness --dataset datasets/mvp_golden.jsonl --seed 42 --compare-baseline

gates: format test eval
	@echo "✅ gates done"
