# Execution scope

## What executed

Exactly the four steps of the repaired
`execution-command-plan.md` of the merged first-supervised-use packet, in
order, in a single supervised sitting (UTC 2026-06-11T18:54:48Z to
2026-06-11T18:55:39Z), plus the operator-input drafting and recording steps
that plan prescribes (drafting `inputs/approval-record.json` and
`inputs/proposed-task.json` below the output root; recording
`checks/commands-run.txt` and `notes/operator-log.md`):

1. Local-only preconditions: clean working tree confirmed; HEAD recorded
   (`4f62d33b122d63e1fe12e7e0554788f465ee98db`); read-only release-gate
   checker exit 0 with JSON written below the output root.
2. Gate-and-record pipeline: one invocation of
   `alpha.self_operator.dry_run.run_local_dry_run_wrapper` with the drafted
   proposed task and approval record, via the repaired environment-handoff
   heredoc (`ROOT="$ROOT" python - <<'PY'` with `os.environ["ROOT"]`). The
   wrapper classified the single proposed command and executed nothing.
3. Supervised deterministic read-only consistency review:
   `python scripts/check_local_llm_packet_consistency.py`, exit 0, stdout
   captured below the output root.
4. Post-run verification: `git status --short` still empty.

## Where it executed

On branch `claude/eloquent-tesla-pmct3n`, created from current `main`
(`e04d4cc`, #478/#479 merged), at commit `4f62d33` — `main` plus exactly
the verified command-plan repair and this lane's pre-run records. The
combined repair-and-execution lane requires the repaired plan to be
committed before the run (the run's own precondition demands a clean tree),
and `main` itself had not moved; the first-use packet remains merged on
`main`, unmodified except through this lane's three allowed repair files.
The run wrote only below the output root
(`/tmp/alpha-solver-self-operator-first-supervised-use-execution-001`),
outside the repository checkout.

## Supervision basis

The repository operator (github: adonisdv23) explicitly authorized this
run — this lane and this run ID only — via the recorded
`OPERATOR_APPROVED_FIRST_USE_TARGET` / `OPERATOR_CONFIRMATION` fields
(`operator-confirmation-record.md`). The run was executed by the operator's
coding agent inside the operator's authorized session, step by step against
the repaired plan, with every command, exit code, and UTC timestamp
recorded contemporaneously; nothing is approved, merged, or promoted by
this lane itself — the resulting PR is the operator's review point. The
lane performed a read-only inspection (repo instructions, the merged
packet, the `alpha/self_operator/` modules, both checker scripts) before
any edit, and executed nothing until the repair gate, the recorded
confirmation, and the target-match proof had all passed.

## Scope identity

The approval record's `scope_summary` and both `scope_identity` metadata
fields carry the same scope text, drawn from the first-use packet's
`use-scope.md`; the execution gate compared them and reported
`identity_match: true`. Allowed activity stayed within `use-scope.md`
items 1–7; every forbidden surface stayed untouched
(`non-execution-proof.md`).
