# Commands run

| # | Command | Exit code | Purpose |
| --- | --- | ---: | --- |
| 1 | `pwd && find .. -name AGENTS.md -print && git status --short --branch` | 0 | Locate repo instructions and inspect checkout status. |
| 2 | `cat AGENTS.md && git remote -v` | 0 | Read repo instructions and remote configuration. |
| 3 | `python - <<'PY' ... urllib.request.urlopen('https://api.github.com/repos/adonisdv23/Alpha-Solver/pulls/{n}') ... PY` | 0 | Verify live GitHub PR state for #497, #499, #500, #501, #502, #503, and #504. |
| 4 | `git fetch origin main --quiet` | 128 | Attempt remote refresh; failed because no `origin` remote is configured in this checkout. |
| 5 | `git branch -avv && rg -n "attestation\|LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-001\|data-sharing\|verification" docs .specs -g '*.md'` | 0 | Inspect local branch and search for verification/attestation context. |
| 6 | `find docs/evals/runs -maxdepth 2 -type f -iname '*.md' \| rg 'openai\|attestation\|smoke' \| sort \| sed -n '1,200p'; rg -n "LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-001\|operator attestation\|pre-smoke\|go\|no_go\|approved next lane" docs/evals/runs/openai* docs/evals/runs/*openai* -g '*.md'` | 0 | Confirm data-sharing packet presence and missing completed pre-smoke attestation. |
| 7 | `mkdir -p docs/evals/runs/local-openai-token-smoke-capture-001; cat > ...` | 0 | Create this blocked smoke-capture packet. |
| 8 | `python scripts/check_local_llm_doc_paths.py` | 0 | Validate local doc paths/links. |
| 9 | `python scripts/check_local_llm_evidence_boundaries.py` | 0 | Validate evidence-boundary wording. |
| 10 | `python scripts/check_local_llm_packet_consistency.py` | 0 | Validate packet consistency. |
