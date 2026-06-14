# Dependency inventory

## Python runtime declarations

| Source | Role | Observed declarations | Notes |
| --- | --- | --- | --- |
| `requirements.txt` | Primary pip install input for root Dockerfile and several CI jobs | `pytest`, `jsonschema`, `pyyaml`, `prometheus-client>=0.20,<1`, `fastapi>=0.111,<0.113`, `starlette<0.38`, `pydantic>=2.7,<3`, `httpx>=0.27,<0.28`, `uvicorn[standard]>=0.30,<0.32` | Mostly range based. Includes `pytest`, which is test tooling, in the primary requirements file. |
| `pyproject.toml` | Package metadata and build-system declaration | Build requirements: `setuptools>=68`, `wheel`. Project dependencies overlap with `requirements.txt`: `jsonschema`, `pyyaml`, `prometheus-client>=0.20,<1`, `fastapi>=0.111,<0.113`, `starlette<0.38`, `pydantic>=2.7,<3`, `httpx>=0.27,<0.28`, `uvicorn[standard]>=0.30,<0.32`. Optional `test`/`dev`: `pytest`. | Runtime metadata is range based and should remain compatible with the root requirements source. |
| `requirements-dev.txt` | Development install input | Includes `-r requirements.txt`, `pytest>=8,<9`, `pytest-cov`, `pre-commit`, `ruff`, `opentelemetry-api==1.24.0`, `opentelemetry-sdk==1.24.0`. | Mixed ranged and unpinned dev tools, with two exact OpenTelemetry pins. |
| `requirements-test.txt` | Additional test install input | `opentelemetry-api`, `opentelemetry-sdk`, `pytest-cov`. | Unpinned test-only declarations. |
| `clients/python/pyproject.toml` | Python SDK package metadata | Build requirement `setuptools>=67`; runtime dependency `requests`; Python `>=3.8`. | SDK dependency is unpinned and separate from the root application dependency set. |

## Constraint / pin artifact

| Source | Role | Observed pins |
| --- | --- | --- |
| `constraints.txt` | Current bounded pip constraints artifact used by selected CI, nightly, and release workflows | `fastapi==0.111.1`, `starlette==0.37.2`, `pydantic==2.11.7`, `httpx==0.27.2`, `uvicorn==0.31.1`, `prometheus-client==0.20.0`, `pytest==8.2.0`, `pytest-cov==5.0.0`, `pre-commit==4.6.0`, `ruff==0.6.9`, `opentelemetry-api==1.24.0`, `opentelemetry-sdk==1.24.0`. |

`constraints.txt` is a pin artifact, not a complete lockfile. It does not include hashes and does not enumerate all transitive dependencies.

## Container dependency sources

| Source | Base image / install path | Dependency boundary |
| --- | --- | --- |
| `Dockerfile` | `python:3.12-slim`; upgrades pip; installs `-r requirements.txt` without constraints | Runtime image can resolve newer in-range releases than constrained CI/release jobs. |
| `infrastructure/Dockerfile` | `python:3.11-slim`; installs `-r requirements.txt` without constraints | Placeholder/generic image path; also unconstrained at install time. |
| `infrastructure/docker-compose.yml` | `api.build: ..` is a string build context from the `infrastructure/` directory, so Compose resolves the context to the repository root and uses the root `Dockerfile` unless overridden; this file does not set a `dockerfile:` override. Auxiliary services use `otel/opentelemetry-collector:latest`, `prom/prometheus:latest`, and `grafana/grafana-oss:latest`. | The API service inherits the root `Dockerfile` dependency resolution (`python:3.12-slim`, `requirements.txt` without constraints), not `infrastructure/Dockerfile`. Auxiliary image tags are not digest pinned. |
| `infrastructure/docker-compose.prod.yml` | `api.build: ..` is a string build context from the `infrastructure/` directory, so Compose resolves the context to the repository root and uses the root `Dockerfile` unless overridden; this file does not set a `dockerfile:` override. Auxiliary services use `otel/opentelemetry-collector:latest`, `prom/prometheus:latest`, and `grafana/grafana-oss:latest`. | The API service inherits the root `Dockerfile` dependency resolution (`python:3.12-slim`, `requirements.txt` without constraints), not `infrastructure/Dockerfile`. Auxiliary image tags are not digest pinned. |

## Workflow dependency sources

| Workflow | Dependency behavior |
| --- | --- |
| `.github/workflows/ci.yml` | Installs `requirements.txt` without `constraints.txt`. |
| `.github/workflows/gates.yml` | Installs `requirements.txt pytest-json-report` without `constraints.txt`. |
| `.github/workflows/nightly.yml` | Installs `requirements-dev.txt -c constraints.txt`. |
| `.github/workflows/release.yml` | Installs `requirements-dev.txt -c constraints.txt`; builds release artifacts. |
| `.github/workflows/reliability-slo.yml` | Installs `requirements.txt pytest-json-report` without `constraints.txt`; starts `redis:7`. |
| `.github/workflows/tests.yml` | Installs `requirements.txt`, `requirements-test.txt`, pytest/pytest-cov, build, and ruff with `-c constraints.txt` where specified. |
| `.github/workflows/docker-publish.yml` | Builds `infrastructure/Dockerfile`; registry push is a placeholder echo for tags. |

## Vendored and shimmed dependency surface

The DEF-002 security/privacy dependency review identified in-tree vendored or shim-like modules such as `slowapi/`, `prometheus_client/`, `prometheus_fastapi_instrumentator/`, `jsonschema/`, and `jsonlines_compat.py`. This lane records that they remain outside normal pip resolver and vulnerability-scanner coverage unless separately inventoried.

## Provider SDK boundary

No provider SDK was added by this lane. Provider dependencies remain limited to already declared packages and in-repo provider code observed through dependency manifests.
