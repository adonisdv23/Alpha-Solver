# Commands Run

```bash
pwd && find .. -name AGENTS.md -print && git status --short && git log --oneline --decorate -n 20
```

```bash
for d in docs/evals/runs/alpha-solver-openai-free-token-eval-smoke-harness-plan-001 docs/evals/runs/openai-data-sharing-operator-verification-001 docs/evals/runs/local-openai-token-smoke-capture-001 docs/evals/runs/openai-synthetic-smoke-prompt-fixture-001 docs/evals/runs/openai-data-sharing-operator-attestation-001; do [ -d "$d" ] && echo "OK $d" || echo "MISSING $d"; done
```

```bash
python scripts/check_local_llm_doc_paths.py
```

```bash
python scripts/check_local_llm_evidence_boundaries.py
```

```bash
python scripts/check_local_llm_packet_consistency.py
```

```bash
python -m pytest tests/test_local_llm_doc_paths.py tests/test_local_llm_evidence_boundaries.py tests/test_local_llm_packet_consistency.py -q
```

```bash
python -m pytest -q
```
