# ALPHA-SOLVER-DEF-002-DEPENDENCY-SUPPLY-CHAIN-GATE-001

Verdict: `DEF_002_DEPENDENCY_SUPPLY_CHAIN_GATE_CAPTURED`

This docs-only packet captures the current dependency provenance, pinning posture, lock/constraint strategy, update cadence, and release-boundary review rules for the DEF-002 dependency supply-chain finding.

## Inputs read

- `requirements.txt`
- `requirements-dev.txt`
- `requirements-test.txt`
- `constraints.txt`
- `pyproject.toml`
- `clients/python/pyproject.toml`
- `Dockerfile`
- `infrastructure/Dockerfile`
- `infrastructure/docker-compose.yml`
- `infrastructure/docker-compose.prod.yml`
- `.github/workflows/`
- `docs/evals/runs/alpha-solver-def-002-security-privacy-review-packet-001/dependency-supply-chain-review.md`
- `docs/evals/runs/alpha-solver-public-exposure-readiness-gate-001/`

## Packet outputs

| File | Purpose |
| --- | --- |
| `dependency-inventory.md` | Inventory of dependency declaration, resolver, container, workflow, and vendored/shim sources observed in this lane. |
| `lock-strategy.md` | Decision on constraints, hash files, lockfiles, pinned requirements, update cadence, and review boundary. |
| `validation-evidence.md` | Commands run and results. |
| `residual-risks.md` | Remaining dependency assurance gaps and release blockers. |
| `selected-next-lane.md` | Recommended next lane after this packet. |
| `evidence-boundary.md` | Evidence limits and allowed/forbidden claims. |
| `non-actions.md` | Actions explicitly not taken. |

## Decision summary

The smallest safe provenance artifact for this lane is this evidence packet plus an explicit acknowledgement that the repository already has a `constraints.txt` pin set used by selected CI/release workflows. This lane does **not** regenerate or broaden pins, does **not** add a hash-pinned lockfile, and does **not** upgrade dependencies.

## Dependency decision

- Keep `requirements.txt` and `pyproject.toml` as range-based compatibility declarations for now.
- Treat `constraints.txt` as the current bounded install pin artifact for CI/release contexts that invoke `pip install ... -c constraints.txt`.
- Do not introduce `requirements.lock`, `uv.lock`, `poetry.lock`, or `--require-hashes` in this lane because doing so safely requires a dedicated resolver, platform policy, and review of transitive artifacts.
- Require future dependency updates to be reviewed as a narrow dependency lane with changelog/security notes and focused test evidence.

## Boundary

This packet captures supply-chain provenance and update policy only. It does not claim complete dependency assurance, production readiness, public readiness, DEF-002 closure, SBOM completeness, vulnerability absence, or transitive hash verification.
