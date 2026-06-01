# DEPLOY-CLOUDRUN-CONFIG-001 · Cloud Run MVP Preview Deployment Config

## Objective

Add minimal Google Cloud Run deployment configuration and operator documentation
for a controlled Alpha Solver MVP preview deployment of `/dashboard/expert-preview`.

## Scope

- Add a root Cloud Run-specific `Dockerfile`.
- Add a root `.dockerignore` for container build hygiene.
- Add `docs/deployment/CLOUD_RUN_MVP_PREVIEW.md` with settings, environment variables, deploy examples, and smoke checks.
- Keep first deployment mode on `MODEL_PROVIDER=local`.
- Keep live OpenAI testing held until local-provider Cloud Run smoke testing succeeds and spend is explicitly approved.

## Acceptance criteria

- The root `Dockerfile` uses Python 3.12, installs `requirements.txt`, copies the repo, and starts `service.app:app` with Uvicorn on `0.0.0.0` using Cloud Run `PORT` with an `8080` fallback.
- `.dockerignore` excludes local caches, artifacts, logs, virtualenvs, VCS state, and local env files without excluding required app files.
- The Cloud Run MVP preview doc covers purpose, scope boundaries, required settings, required env vars, local build/run, deploy examples, smoke tests, fail-closed dashboard behavior, the bundled preview login redirect behavior, local-provider first workflow, held live OpenAI workflow, security notes, claim boundaries, troubleshooting, and backlog impact.
- No runtime behavior changes are made.
- No secrets are committed.
- No Cloud Run deployment is performed from Codex.

## Backlog impact

`DEPLOY-CLOUDRUN-CONFIG-001` should be marked Done only after the PR implementing
this spec is merged. It remains a deployment-config/docs lane under
`DEPLOY-CLOUDRUN-EPIC-001` and does not validate the MVP, claim production
readiness, or enable live OpenAI testing.

## Non-goals

- No Alpha Solver runtime behavior changes.
- No provider expert-pass behavior changes.
- No clarify behavior changes.
- No eval artifact behavior changes.
- No behavioral demo checklist behavior changes.
- No preview behavior changes.
- No dashboard auth behavior changes.
- No live OpenAI default.
- No Firebase Hosting.
- No custom domain setup.
- No Google Sheets or backlog workbook edits.
- No MVP validation claim.
- No Alpha Solver superiority claim.
- No answer-quality superiority claim.
- No production-readiness claim.
- No broad runtime-readiness claim.
- No answer-quality benchmark success claim.
- No provider reasoning orchestration claim.
