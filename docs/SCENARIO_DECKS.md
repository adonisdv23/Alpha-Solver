# Scenario Decks

This repository contains small curated decks of labeled scenarios used for smoke and quality tests.  Each record in `data/scenarios/decks/*.jsonl` includes:

* `id` – unique and sorted within the file
* `intent` – task category such as `summarize`, `extract`, or `codegen`
* `prompt` – the user request
* `route_expected` – expected routing result (`llm_only` or `mcp`)
* `notes` – short curator hint
* optional `expectations` metadata

## Curation rubric

1. Prompts are concise and self contained.
2. IDs are stable (`deck-<intent>-NNNN`) and sorted.
3. At least 90% of scenarios expect the `llm_only` route to keep quality gates fast.
4. Prompts should be ≤1000 characters after whitespace normalization.

Use `scripts/decks_curate.py --check data/scenarios/decks/*.jsonl` to validate schema and uniqueness.

## Extending decks

1. Add new scenarios to the appropriate `core_<intent>.jsonl` file.
2. Keep files UTF-8 encoded with one JSON object per line.
3. Run the curator script in check mode before committing.
4. Update or create tests if a new intent is introduced.

## Sampling

The curator script supports sampling for quick experiments:

```bash
python scripts/decks_curate.py --check --sample 5 --shuffle --seed 123 data/scenarios/decks/*.jsonl
```

This emits five random scenarios using a fixed RNG seed to ensure reproducibility.
