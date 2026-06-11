# First supervised-use scope

## Allowed scope

The execution lane may do all of the following, and nothing else:

1. Read, read-only, the input artifacts listed in `input-artifacts.md`.
2. Create the local output root defined in `output-root.md` (outside the
   repository) and write only below it during the run.
3. Draft one approval record and one proposed task for this lane and one
   fresh run ID, per `operator-confirmation-required.md`.
4. Invoke `alpha.self_operator.dry_run.run_local_dry_run_wrapper` once with
   that proposed task, that approval record, and that output root. The
   wrapper classifies proposed command text; it does not execute proposed
   commands.
5. Run the deterministic read-only checkers exactly as recorded in
   `execution-command-plan.md`, capturing output below the output root.
6. Preserve and review the resulting artifacts per `expected-artifacts.md`,
   apply `redaction-rules.md`, and import only copied, redacted artifacts
   into the execution lane's own packet directory under `docs/evals/runs/`
   through lane review.
7. Stop on any condition in `stop-state-rules.md` or `abort-conditions.md`
   and route per `blocker-fallback-lane.md`.

## Forbidden surfaces

All of the following remain forbidden for the first supervised use,
regardless of approval text. Naming them here forbids them; it does not
describe anything this packet or the first use does:

- provider calls of any kind;
- hosted model calls;
- local model calls (including Ollama);
- external API calls;
- browser automation;
- deployment of any kind;
- billing surfaces or billing actions;
- credential access, storage, display, or use;
- secret access, storage, display, or use;
- `/v1/solve` exposure or invocation;
- dashboard exposure;
- production use of any kind;
- benchmark superiority claims;
- autonomous operation (every step is operator-supervised);
- source-artifact mutation (all inputs are consumed read-only);
- Google Sheets reads or writes;
- implementing the deferred status CLI;
- any repository write outside the execution lane's own packet directory.

## Scope identity

The execution lane must carry this scope as its approval
`scope_summary` and proposed-task metadata scope identity, so the execution
gate can compare every identity dimension. Any change to this scope is a
new scope and requires a fresh charter, fresh confirmation, and a fresh
approval record.
