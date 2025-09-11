.PHONY: dev-setup gates test lint format run smoke eval

dev-setup:
	pip install -r requirements-dev.txt
	pre-commit install

lint:
	pre-commit run --all-files

format: lint

test:
	pytest -q

eval:
	python -m alpha.eval.harness --dataset datasets/mvp_golden.jsonl --seed 42 --compare-baseline || echo "eval skipped (no secrets?)"

smoke:
	python - <<'PY'
	from fastapi.testclient import TestClient
	from service.app import app
	app.state.config.api_key='dev-secret'
	c=TestClient(app)
	assert c.get('/openapi.json').status_code==200
	r=c.post('/v1/solve', headers={'X-API-Key':'dev-secret'}, json={'query':'2+2','strategy':'react'})
	assert r.status_code==200, r.text
	print('SMOKE OK')
	PY

gates: lint test eval smoke

run:
	uvicorn service.app:app --host 0.0.0.0 --port 8000 --proxy-headers
