# Allowed local commands

Future preflight may allow local read-only or offline commands such as:

- `git status --short`
- `git branch --show-current`
- `git diff --name-only`
- `git diff --cached --name-only`
- `git diff --check`
- `git diff --cached --check`
- `python --version`
- `python scripts/check_local_llm_packet_consistency.py <packet>`
- `make check-local-llm-orchestration-guardrails`

Allowed commands must be run locally and must not require network, credentials, providers, browsers, deployment, or billing.
