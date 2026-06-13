# Test evidence

## Focused tests

Command:

```bash
python -m pytest -q tests/ui/test_settings.py
```

Result:

```text
.........                                                                [100%]
```

Coverage from this focused test file includes:

- Synthetic provider key creation persists and masked display does not expose the
  raw key.
- Synthetic provider key update overwrites storage and masked audit records do
  not expose the raw key.
- Synthetic provider key deletion removes storage and logs only a masked value.
- Short synthetic keys are fully masked in display.
- Audit log content does not contain raw synthetic secret values.
- POSIX app-created credential/audit directory modes are restrictive.
- POSIX credential/audit file modes are restrictive.
- Existing permissive synthetic secret files are tightened on write when the
  parent directory is already private.
- Existing private caller-supplied parent directories are accepted without
  broadening permissions.
- Existing unsafe caller-supplied parent directories fail closed without being
  chmodded and without writing synthetic secret/audit files.

## Required static checks

The following static checks were run for this lane:

```bash
python scripts/check_local_llm_doc_paths.py
python scripts/check_local_llm_evidence_boundaries.py
python scripts/check_local_llm_packet_consistency.py
```

See the PR validation output for exact command results.

## Provider boundary

No provider call tests were run. No real credential was required. No token was
used. Tests used synthetic placeholder secret strings only.
