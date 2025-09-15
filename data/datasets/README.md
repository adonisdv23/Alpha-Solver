# Test Datasets

Synthetic datasets used for baseline tests.

## Files

- `pii/labels_email_phone.jsonl` – 100 rows with either an email or phone number label.
- `routing/scenarios_routing.jsonl` – 30 routing scenarios labeled `llm_only` or `mcp`.
- `replay/replay_small.jsonl` – 10 deterministic replay events with expected results.

## Checksums (SHA256)

- `0691de2256066b7205239da48bded5353307c7bc96c1805a280f734a8db23ebc`  pii/labels_email_phone.jsonl
- `6b130f01a3081e5df438444db721604d0c5a5dda836a3eb01ed54654c7938a94`  routing/scenarios_routing.jsonl
- `92b8f10d202354bc3a0a76f5e3509ff5b2bea826b9f4a8932b7560b9da7ca8dd`  replay/replay_small.jsonl

Generated via `scripts/generate_synthetic_dataset.py` and sorted by `id` for determinism.
