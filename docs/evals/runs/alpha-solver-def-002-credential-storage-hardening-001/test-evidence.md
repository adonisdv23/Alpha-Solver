# Test evidence

## Focused tests

Command:

```bash
python -m pytest -q tests/ui/test_settings.py
```

Result:

```text
.......                                                                  [100%]
```

Coverage from this focused test file includes:

- Synthetic provider key creation persists and masked display does not expose the
  raw key.
- Synthetic provider key update overwrites storage and masked audit records do
  not expose the raw key.
- Synthetic provider key deletion removes storage and logs only a masked value.
- Short synthetic keys are fully masked in display.
- Audit log content does not contain raw synthetic secret values.
- POSIX credential directory/file modes are restrictive.
- Existing permissive synthetic secret files/directories are tightened on write.

## Required static checks

The following static checks were run for this lane:

```bash
python scripts/check_local_llm_doc_paths.py
python scripts/check_local_llm_evidence_boundaries.py
python scripts/check_local_llm_packet_consistency.py
```

See the PR validation output for exact command results.

## Broad validation caveat

A broad `python -m pytest -q` run was attempted after the focused tests. It failed in unrelated provider/API tests and logs showed provider-backed `/v1/solve` execution due ambient configuration. That run breached this lane's no-provider-call validation boundary and is the reason the packet verdict is `STOP_INCONCLUSIVE`, even though the focused credential-storage tests passed.

## Provider boundary

The focused credential-storage tests did not run provider call tests, did not require real credentials, and used synthetic placeholder secret strings only. The later broad test attempt breached the no-provider-call boundary as noted above.
