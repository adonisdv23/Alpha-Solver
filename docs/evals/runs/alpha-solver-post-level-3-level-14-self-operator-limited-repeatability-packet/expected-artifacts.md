# Expected artifacts

A future repeatability execution lane must preserve these artifacts below the
fresh output root:

| Artifact | Required status |
| --- | --- |
| `inputs/approval-record.json` | Present. |
| `inputs/proposed-task.json` | Present. |
| `inputs/source-evidence-index.json` | Present. |
| `inputs/repeatability-plan-verification.json` | Present and passing. |
| `dry-run-result.json` | Present; records wrapper classification and non-execution. |
| `execution-gate-result.json` | Present; records gate status. |
| `checks/release-gate-check.json` | Present; release-gate checker output. |
| `checks/consistency-check.stdout.txt` | Present; bare packet consistency checker output. |
| `checks/consistency-check-packet.stdout.txt` | Present; limited repeatability packet-scoped consistency checker output. |
| `checks/commands-run.txt` | Present; exact commands, UTC timestamps, and exit codes. |
| `checks/git-status-before.txt` | Present and empty or explicitly records no tracked changes. |
| `checks/git-status-after.txt` | Present and empty or explicitly records no tracked changes. |
| `checks/forbidden-surface-proof.md` | Present; records non-execution proof for forbidden surfaces. |
| `checks/source-artifact-mutation-check.md` | Present; records no source-artifact mutation. |
| `checks/redaction-review.md` | Present; records redaction review result. |
| `checks/raw-artifact-inventory.md` | Present; records raw artifact inventory shape. |
| `notes/operator-log.md` | Present; records supervised observations. |
| `stop-state.json` | Absent on success; present only if a stop condition occurs. |

If `stop-state.json` exists, the future lane is terminal and must not claim a
successful repeatability outcome.
