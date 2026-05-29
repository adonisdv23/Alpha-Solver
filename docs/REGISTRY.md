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

## Registry exports versus backlog

`data/alpha_solver_master_table_v0_7_0.csv` and
`data/alpha_solver_master_table_v0_7_0.xlsx` are registry/tool-model catalog
exports. They are **not the active task backlog** and should not be used to
decide implementation status, PR status, backlog priority, or the next
development action. Treat them as registry provenance, source material, audit
context, or historical export data.

Source-of-truth boundaries:

- External backlog workbook: planning/status ledger maintained outside this
  repository.
- `.specs/`: implementation contracts for approved behavior changes.
- GitHub PRs, commits, and test results: implementation evidence and review
  history.
- `registries/` and `schemas/`: runtime and governance registry assets.
- `data/alpha_solver_master_table_v0_7_0.*`: registry export/provenance data,
  not backlog.

Quick identification guide:

- Backlog rows usually have fields such as `status`, `priority`, `spec path`,
  `PR URL`, `implementation evidence`, and `next action`.
- Registry export rows usually have fields such as `id`, `name`, `type`,
  `bucket`, `ecosystem`, `modality`, `registry_file`, `primary_use_case`,
  `capabilities`, `limitations`, `pricing`, `compliance`, and `latency`.

Do not delete, rename, archive, or move these `data/` files without a separate
migration and reference check. If they are renamed later, update all docs and
any scripts or manual workflows that reference them.
