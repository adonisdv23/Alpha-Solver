# Data Exports

This directory contains generated or imported data artifacts that can support
registry work, audits, and historical provenance. Files here are not the active
planning backlog unless a future document explicitly says so.

## Alpha Solver master table v0.7.0

The following files are registry/tool-model catalog exports:

- `alpha_solver_master_table_v0_7_0.csv`
- `alpha_solver_master_table_v0_7_0.xlsx`

They are **not the active task backlog**. Do not use these files to decide
implementation status, PR status, backlog priority, or the next development
action for the repository. They may still be useful as registry provenance,
source material, audit context, or historical export data for tool/model catalog
work.

## Source-of-truth boundaries

Use the following boundaries when deciding which artifact answers which kind of
question:

| Artifact | Role |
| --- | --- |
| External backlog workbook | Planning and status ledger maintained outside the repository. |
| `.specs/` | Repository implementation contracts for approved behavior changes. |
| GitHub PRs, commits, and test results | Implementation evidence and review history. |
| `registries/` and `schemas/` | Runtime and governance registry assets. |
| `data/alpha_solver_master_table_v0_7_0.*` | Registry export/provenance data, not backlog. |

## Quick identification guide

Backlog rows usually include planning fields such as `status`, `priority`,
`spec path`, `PR URL`, `implementation evidence`, and `next action`.

Registry export rows usually include catalog fields such as `id`, `name`,
`type`, `bucket`, `ecosystem`, `modality`, `registry_file`,
`primary_use_case`, `capabilities`, `limitations`, `pricing`, `compliance`,
and `latency`.

## Rename, deletion, and migration warning

Do not delete, rename, archive, or move `alpha_solver_master_table_v0_7_0.csv`
or `alpha_solver_master_table_v0_7_0.xlsx` without a separate migration and
reference check. If these files are renamed later, update all documentation and
any scripts or manual workflows that reference them.
