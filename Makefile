.PHONY: smoke canon report test preflight all overnight

smoke:
	python 'Alpha Solver.py' --no-benchmark --no-telemetry

canon:
	python scripts/build_tools_canon.py

report:
	python scripts/report_expansion.py

test:
	python -m unittest -q

preflight:
        python scripts/preflight.py

all:
        make preflight && make canon && make report && make test

overnight:
        python scripts/overnight_run.py
