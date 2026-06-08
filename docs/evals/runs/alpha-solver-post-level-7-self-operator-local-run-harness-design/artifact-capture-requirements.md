# Artifact Capture Requirements

A future local-only harness should capture enough information for local operator review without turning the run into promoted evidence.

## Required local artifacts

- `run-manifest.json` or equivalent local manifest containing run id, timestamp, branch, task id, command, timeout, and artifact directory.
- `preflight-results.md` or equivalent preflight summary.
- `command-provenance.txt` containing the exact local command executed.
- `stdout.txt` and `stderr.txt` for raw local command streams.
- `exit-status.txt` containing numeric exit status or stop-state marker.
- `elapsed-time.txt` containing local elapsed runtime.
- `artifact-inventory.md` listing every file written by the harness.
- `redaction-summary.md` confirming whether any secret-like strings were found and how they were handled.
- `stop-state.md` documenting pass, fail, blocked, or stopped state.
- `evidence-boundary.md` confirming the run is local, non-promotional, and not provider-backed.

## Capture rules

- Artifacts must be written only under the approved local artifact directory.
- Raw outputs must not be edited in place.
- Redacted summaries must be separate from raw captures.
- The harness must record when no task execution occurred because a preflight or stop state blocked the run.
- Artifact manifests must not claim production readiness, benchmark status, model quality, provider integration, dashboard availability, or deployment readiness.

## Retention boundary

Artifacts captured by the future harness remain local run artifacts. They are not promoted evidence unless a separate authorized evidence-promotion lane explicitly reviews and accepts them.
