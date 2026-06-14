# Lock and update strategy

## Strategy decision

Verdict for strategy selection: use the existing `constraints.txt` as the current minimal pin artifact, document its boundary, and defer any hash-pinned or transitive lockfile introduction to a dedicated dependency hardening lane.

## Why not change dependency versions now

This lane is a provenance and release-boundary gate. Upgrading, relaxing, or broadly regenerating dependencies would change runtime resolution behavior and require compatibility testing beyond this approved scope.

## Current artifact classification

| Artifact type | Current status | Decision |
| --- | --- | --- |
| Range declarations | Present in `requirements.txt`, `pyproject.toml`, `requirements-dev.txt`, `requirements-test.txt`, and SDK metadata. | Keep as compatibility declarations until a package-management source-of-truth lane decides otherwise. |
| Constraints file | Present as `constraints.txt`. | Treat as the current bounded install pin artifact for jobs that opt into `-c constraints.txt`. |
| Full lockfile | Not present. | Do not add in this lane. Needs tool choice and platform policy. |
| Hash-pinned install file | Not present. | Do not add in this lane. Needs transitive resolution, platform tag review, and hash-refresh workflow. |
| SBOM | Not observed in this lane. | Do not create in this lane; recommend later release-hardening lane. |

## Required update cadence

- **Routine cadence:** review dependency updates monthly or before each release candidate, whichever comes first.
- **Security cadence:** review critical/high vulnerability advisories as soon as practical and route them through a narrow emergency dependency lane when needed.
- **Release cadence:** before release artifacts are built from a release branch/tag, confirm whether the release workflow uses `constraints.txt` and record any intentionally unconstrained install paths.
- **Vendored/shim cadence:** review in-tree vendored/shim modules at least once per release cycle or when related upstream advisories are published.

## Review boundary for future updates

A future dependency update lane should include:

1. The package names and old/new versions.
2. Whether each change is runtime, dev-only, test-only, container base image, workflow action, or SDK-only.
3. Links or notes for changelog/security rationale.
4. Confirmation that no provider SDK was added unless already required and justified.
5. Focused tests for affected runtime surfaces plus `python -m pytest -q` when practical.
6. A statement of whether `constraints.txt`, package metadata, Docker installs, and workflow installs remain aligned.

## Release-boundary rule

A release should not claim complete dependency assurance unless a later lane provides at least one of these explicitly reviewed artifacts:

- a complete transitive lockfile for the chosen installer and supported platform set,
- a hash-pinned requirements artifact with documented refresh procedure,
- a generated SBOM plus vulnerability-audit evidence, or
- an explicit operator risk-acceptance packet that states why those controls are deferred.
