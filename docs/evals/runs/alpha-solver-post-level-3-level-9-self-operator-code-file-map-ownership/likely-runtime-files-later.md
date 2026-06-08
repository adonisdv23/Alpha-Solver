# Likely runtime files later

Future runtime lanes may inspect these files, but the first-code static test lane must not modify them:

- `alpha/local_llm/operator_cli.py`
- `alpha/local_llm/orchestration_runner.py`
- `alpha_solver_cli.py`
- `cli/alpha_solver_cli.py`
- `service/app.py`
- `alpha/api/`
- `alpha/webapp/`
- `alpha/providers/`
- `docs/ENTRYPOINTS.md`

Modification requires a later explicit runtime lane and must preserve Level 8 and Level 9 boundaries.
