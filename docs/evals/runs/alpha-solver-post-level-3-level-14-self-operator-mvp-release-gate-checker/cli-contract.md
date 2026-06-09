# CLI Contract

Command:

```bash
python scripts/check_self_operator_release_gate.py --repo-root . --output <path>
```

Behavior:

- accepts `--repo-root`, defaulting to `.`;
- accepts `--output` for deterministic JSON;
- prints a concise gate summary;
- exits nonzero for blocked final statuses;
- never updates Google Sheets;
- never mutates source artifacts;
- never runs providers, models, APIs, browser automation, deployment, or billing;
- does not claim MVP readiness.
