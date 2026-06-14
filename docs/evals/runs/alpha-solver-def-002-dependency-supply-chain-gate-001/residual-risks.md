# Residual risks

## Remaining gaps

| ID | Residual risk | Boundary |
| --- | --- | --- |
| DR-01 | `constraints.txt` is not a complete transitive lockfile and has no hashes. | Fresh installs can still depend on resolver behavior for transitive packages and cannot verify package file hashes. |
| DR-02 | Several install paths do not apply `constraints.txt`. | The root `Dockerfile`, the standalone `infrastructure/Dockerfile`, compose API builds that resolve to the root `Dockerfile`, and some workflows install range declarations directly. |
| DR-03 | Dependency declarations are split across root requirements, package metadata, dev/test files, SDK metadata, Dockerfiles, compose files, and workflows. | Drift can occur without a source-of-truth policy. |
| DR-04 | Vendored/shimmed in-tree modules are not covered by declared dependency scanning. | Their upstream provenance, version, and patch status require a separate inventory. |
| DR-05 | Container base images, compose auxiliary images, and GitHub Actions are not pinned by digest/SHA. | Image/action upstream changes can affect build behavior; compose auxiliary services use `latest` tags in the inspected files. |
| DR-06 | No SBOM or vulnerability-audit artifact is recorded by this lane. | Absence of known vulnerabilities is not proven. |
| DR-07 | Python SDK dependency `requests` is unpinned in `clients/python/pyproject.toml`. | SDK install behavior remains resolver-dependent. |

## Release impact

These residual risks remain blockers for any claim of complete dependency assurance. They do not by themselves change runtime code in this lane, but they must be closed or explicitly accepted before public/production readiness claims.

## Operator decision points

- Select package-management source of truth: requirements plus constraints, project metadata plus generated constraints, or a lockfile tool.
- Decide whether Docker and all workflows must enforce `constraints.txt` before release.
- Decide whether hash pinning is required for runtime releases.
- Decide whether vendored/shim modules should be removed, replaced, or separately tracked.
