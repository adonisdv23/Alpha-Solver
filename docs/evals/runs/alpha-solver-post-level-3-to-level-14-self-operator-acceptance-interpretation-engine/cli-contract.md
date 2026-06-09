# CLI Contract

Command:

```bash
python scripts/interpret_self_operator_acceptance.py --import-summary INPUT.json --output OUTPUT.json
```

The CLI:
- writes deterministic JSON;
- prints a concise summary;
- exits nonzero for `blocked`;
- exits zero for `eligible_for_later_release_review` and `needs_review` only when no `P0` or `P1` exists;
- does not update Google Sheets;
- does not mutate source artifacts;
- does not claim MVP readiness.
