# Checks Run

The required checks for this docs-only packet are recorded here after execution:

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `test "$(git diff --name-only | rg -v '^docs/evals/runs/alpha-solver-demo-evidence-packet-to-demo-001/' | wc -l)" -eq 0`
- `find docs/evals/runs/alpha-solver-demo-evidence-packet-to-demo-001 -maxdepth 1 -type f | sort`
- Required boundary phrase scan with `rg` against this packet directory.

## Evidence boundary

These checks are local documentation and static boundary checks only. They do not modify global source-of-truth files, product UI, runtime behavior, dashboards, public APIs, `/v1/solve`, providers, local models, Google Sheets, or implementation paths.
