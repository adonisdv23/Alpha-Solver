# Common Safe Fixes

## Fix a broken local LLM doc path

1. Use the checker output line number to find the bad reference.
2. Confirm the intended target exists with a read-only command such as `test -e <path>` or `find <parent> -maxdepth <n> -type f`.
3. Update the doc to the actual repo-relative path.
4. Re-run `python scripts/check_local_llm_doc_paths.py`.

Do not fix by deleting preserved source artifacts, renaming accepted packet directories, or hiding a path from the checker.

## Fix stale selected-next language

1. Identify the current selected-next state from authoritative selected-next files.
2. Mark old references as prior, preserved, historical, previous, or closed.
3. Keep exactly one current selected-next action in the doc section.
4. Re-run the docs path/link and packet consistency checkers.

Do not infer missing selected-next packet fields from memory, an external spreadsheet, or prior chat context.

## Fix a missing blocker fallback

1. Add an explicit blocker fallback lane in the correct authoritative doc or packet file.
2. Use the lane supplied by the active work item, not a guessed lane.
3. Preserve the distinction between blocker fallback and selected-next action.
4. Re-run `python scripts/check_local_llm_packet_consistency.py`.

For this runbook, the blocker fallback lane is:

```text
ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-POST-LEVEL-3-GUARDRAIL-RUNBOOK-FIX-001
```

## Fix a missing evidence boundary

1. Add explicit evidence-boundary or blocked-claims language near the sensitive claim.
2. Put final boundary and decision markers in authoritative packet or runbook files, not only logs.
3. State the non-action clearly: the doc does not run models, providers, benchmarks, routes, billing, evidence promotion, Google Sheets, or backlog workbook work.
4. Re-run all three direct checker commands.

## Fix unsupported claim terms safely

If a doc must mention a blocked term, keep the boundary in the same sentence, row, or nearby section. Use language such as "not accepted," "not authorized," "blocked," "non-claim," or "evidence boundary." Do not soften the checker, remove tests, or recast a blocked claim as an operational result.
