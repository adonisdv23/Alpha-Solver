# Registry

Tool metadata lives under `registries/tools.json` and follows
`schemas/registry.schema.json`.

Run the preflight script to validate basic structure and tool ids:

```bash
make preflight
# or
python scripts/preflight.py --fix-ids
```

The script checks for required fields, duplicate ids, and that priors
are in the `[0,1]` range. Set `ALPHA_MIN_TOOLS` to require a minimum
count of tools.
