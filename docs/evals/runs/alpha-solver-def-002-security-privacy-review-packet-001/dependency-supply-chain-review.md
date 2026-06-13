# Dependency and supply-chain review

Covers: declared dependencies, pinning discipline, lockfile/hash posture, and
vendored third-party code.

## Declared dependencies

- `requirements.txt` (runtime):
  `pytest`, `jsonschema`, `pyyaml`, `prometheus-client>=0.20,<1`,
  `fastapi>=0.111,<0.113`, `starlette<0.38`, `pydantic>=2.7,<3`,
  `httpx>=0.27,<0.28`, `uvicorn[standard]>=0.30,<0.32`.
- `requirements-dev.txt`: pulls `requirements.txt` plus `pytest>=8,<9`,
  `pytest-cov`, `pre-commit`, `ruff`, and pinned
  `opentelemetry-api==1.24.0` / `opentelemetry-sdk==1.24.0`.
- `pyproject.toml` declares an overlapping but **not identical** dependency set
  (`dependencies` at lines 17-26) with the same range style.

**Finding (DEP-1):** Dependency declarations are duplicated across
`requirements.txt` and `pyproject.toml` and are not guaranteed to stay in sync
(`requirements.txt` lists `jsonschema`/`pyyaml`/`pytest` that the `pyproject`
`dependencies` block does not). Drift risk. Tracked in `risk-register.md` as
RR-06.

## Pinning / lockfile / hash posture

- Runtime dependencies use **version ranges**, not exact pins, and there is **no
  lockfile** (no `requirements.lock`, `poetry.lock`, `pip-tools` compiled file,
  or hash-pinned `--require-hashes` manifest) in the dependency manifests.
- This means a fresh install can resolve to newer in-range releases than were
  reviewed, and installs are not protected against compromised-but-in-range
  package versions (no hash verification).

**Finding (DEP-2):** No lockfile and no hash pinning for runtime dependencies.
This is the primary supply-chain surface. Tracked as RR-07.

## Vendored third-party code

The repository contains directories that appear to **vendor / shim** third-party
libraries at the repo root, e.g. `slowapi/`, `prometheus_client/`,
`prometheus_fastapi_instrumentator/`, `jsonschema/`, and a `jsonlines_compat.py`
shim. Vendored copies:

- decouple the code from upstream security patching (no dependency resolver will
  bump them), and
- are not covered by dependency-scanning of declared requirements.

**Finding (DEP-3):** Vendored/shimmed third-party modules are present in-tree.
Their provenance, version, and patch status are not tracked by the dependency
manifests, creating an unscanned supply-chain surface. Tracked as RR-08.

> Note: this review did not deeply audit the contents of each vendored module
> (out of scope for a posture review) — it records the *surface* and the tracking
> gap. A follow-up inventory belongs in the gap-closure lane.

## Build / packaging

- Build backend is `setuptools` (`pyproject.toml:2-3`), `requires-python >= 3.12`.
- No automated dependency-audit (e.g. `pip-audit`) or SBOM generation was
  identified in scope; CI was **not** inspected for modification and is **not**
  changed by this lane.

## Summary

| ID | Gap | Severity |
| --- | --- | --- |
| RR-06 | Duplicated, potentially drifting dependency declarations | Low |
| RR-07 | No lockfile / no hash pinning (range-only) | Medium |
| RR-08 | In-tree vendored libs with untracked provenance/patch status | Medium |

The supply-chain posture is the weakest-tracked area: ranges without a lockfile
plus vendored copies. None requires a code change in *this* docs-only lane; all
feed the gap-closure plan.
