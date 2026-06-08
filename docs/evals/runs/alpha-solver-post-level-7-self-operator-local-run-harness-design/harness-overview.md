# Harness Overview

## Design goal

A future Self Operator MVP local run harness should provide a deterministic, operator-readable wrapper around bounded local tasks. The harness should make it easy to confirm preconditions, run an explicitly scoped local task, preserve artifacts, and stop safely when the requested action leaves the approved local-only boundary.

## Future harness phases

1. **Prepare local run directory**
   - Create a timestamped local artifact directory under a repo-approved evidence path.
   - Record command provenance, branch name, git status, and packet/run identifier.
   - Refuse to overwrite prior artifacts unless the operator explicitly chooses a new local output path.

2. **Run preflights**
   - Validate that required local tools are present.
   - Validate no required credentials are requested or loaded.
   - Validate that the task manifest is local, bounded, and does not request external effects.
   - Validate that the repository is in an expected state for the operator's intended task.

3. **Execute bounded local task**
   - Run only an allowlisted local command or script.
   - Apply fixed timeout, output-size, and artifact-size limits.
   - Record stdout, stderr, exit status, and elapsed time.
   - Stop immediately if the task requests provider calls, browser control, deployment, dashboard exposure, credential access, billing activity, or evidence promotion.

4. **Capture artifacts**
   - Preserve raw local outputs.
   - Preserve redacted operator-facing summaries where needed.
   - Preserve stop-state and preflight outcomes.
   - Preserve a manifest proving artifacts stayed local.

5. **Close run state**
   - Mark the run as passed, failed, blocked, or stopped.
   - Avoid interpreting local artifacts as promoted evidence.
   - Require a separate authorized lane before any implementation, runtime change, evidence promotion, or external integration.

## Non-goal

This packet does not implement the harness. It only describes the design requirements for a possible future local-only harness.
