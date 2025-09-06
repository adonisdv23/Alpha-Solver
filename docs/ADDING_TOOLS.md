# Adding Tools

Each tool entry in the registry requires:

- `id` – unique identifier
- `name` – human-readable label
- `keywords` – list of searchable terms
- `priors` – numbers in `[0,1]` such as `sentiment_prior` and `adoption_prior`
- `regions` – list of region codes where the tool is available

## Priors and Region Weights

Priors combine with telemetry and optional dated priors. When dated priors are
present they are blended with recency using the environment variables
`ALPHA_RECENCY_PRIORS_PATH` and related settings. Region weights from
`ALPHA_REGION_WEIGHTS_PATH` multiply final scores before tie-breaks.

## Preflight Checks

Validate registry entries and priors before committing:

```bash
python scripts/preflight.py
```
