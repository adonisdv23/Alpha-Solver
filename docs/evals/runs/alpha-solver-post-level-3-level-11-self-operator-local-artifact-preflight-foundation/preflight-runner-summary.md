# Preflight runner summary

Implemented `ProposedTask`, `PreflightResult`, and `run_local_preflight`.

The runner only classifies proposed work. It blocks or stops when:

- explicit operator confirmation is missing;
- scope is unclear;
- changed files exceed allowed helper/test/fixture/docs packet scope;
- proposed command classification finds forbidden surfaces;
- artifact paths are unsafe;
- evidence boundary is missing;
- source-artifact mutation or evidence promotion is implied.

It does not execute requested tasks or proposed commands.
