# Selected next lane

Recommended next supply-chain lane:
`ALPHA-SOLVER-DEF-002-DEPENDENCY-SUPPLY-CHAIN-LOCK-HASH-SBOM-DECISION-001`

## Rationale

This packet captures provenance and update policy but intentionally does not introduce a full lockfile, hash-pinned requirements, SBOM, or vulnerability-audit artifact. The next supply-chain lane should make the operator/tooling decision needed to close or explicitly defer those controls.

## Suggested scope

- Choose the dependency source of truth.
- Decide whether `constraints.txt` becomes mandatory for Docker and all CI/release installs.
- Decide whether to generate a full transitive lockfile, hash-pinned requirements artifact, SBOM, or a documented risk acceptance.
- Inventory vendored/shimmed modules with provenance and replacement/removal decisions.

## Boundary

This selected next lane is a recommendation only. It does not authorize public exposure, provider calls, deployment, dependency upgrades, or DEF-002 closeout.
