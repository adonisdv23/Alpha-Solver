# Baseline Test Datasets

The `data/datasets` directory contains synthetic datasets used in the NEW-022 tests.

- **PII** – `pii/labels_email_phone.jsonl`
  - 100 labeled rows with emails and phone numbers.
  - Used by `tests/test_policy_dataset.py` to ensure ≥99% detection, no PII leakage and p95 redaction <50ms.
- **Routing** – `routing/scenarios_routing.jsonl`
  - 30 scenarios labeled `llm_only` or `mcp`.
  - Exercised in `tests/test_routing_accuracy.py` requiring ≥90% accuracy.
- **Replay** – `replay/replay_small.jsonl`
  - 10 deterministic events with expected results.
  - Verified by `tests/test_replay_stability.py` for 10/10 stable replays.

`tests/test_scenarios_smoke.py` performs a minimal end-to-end check across all datasets.
