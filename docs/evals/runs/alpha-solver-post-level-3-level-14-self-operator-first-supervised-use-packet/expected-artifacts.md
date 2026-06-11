# Expected artifacts

Artifacts the first supervised use is expected to produce, all below the
output root defined in `output-root.md`. Paths are relative to that root.

## Pipeline artifacts (written by the wrapper / artifact store)

| Artifact | Expectation |
| --- | --- |
| `dry-run-result.json` | Present on any completed wrapper invocation; carries the wrapper's non-execution marker text (the wrapper does not execute proposed commands; it only classifies proposed command text) and `redaction_status: redacted`. |
| `execution-gate-result.json` | Present; on success the gate status is `allowed_for_local_dry_run_wrapper`. |
| `stop-state.json` | Present only if the run stops; if present, the run is terminal and `stop-state-rules.md` applies. |

## Operator-drafted run inputs (preserved as evidence)

| Artifact | Expectation |
| --- | --- |
| `inputs/approval-record.json` | The validated approval record for this run. |
| `inputs/proposed-task.json` | The single docs-only proposed task for this run. |

## Supervised checker captures

| Artifact | Expectation |
| --- | --- |
| `checks/consistency-check.stdout.txt` | Captured stdout of the packet consistency checker run from `execution-command-plan.md`; expected to end with the checker's pass line and exit code 0 recorded alongside. |
| `checks/release-gate-check.json` | JSON output of the read-only release-gate precondition check, written below the root via its `--output` flag. |
| `checks/commands-run.txt` | The exact commands run, in order, with exit codes and UTC timestamps. |

## Operator notes

| Artifact | Expectation |
| --- | --- |
| `notes/operator-log.md` | The operator's contemporaneous supervision log: who supervised, start/stop times, observations, and any anomaly. |

## Success criteria

The first use succeeds only if all of: gate status
`allowed_for_local_dry_run_wrapper`; no `stop-state.json`; consistency
checker exit code 0; release-gate checker exit code 0; every artifact above
present, redacted, and inside the root; and no file changed inside the
repository checkout during the run (`git status --short` clean before
import).

## Repository-side import

The execution lane imports only copied, redacted versions of the artifacts
above into its own packet directory under `docs/evals/runs/`, after the
redaction review in `redaction-rules.md`. Raw artifacts never enter the
repository. How raw artifacts are preserved is fixed in `output-root.md`
rule 6.
