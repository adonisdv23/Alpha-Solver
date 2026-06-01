# DEPLOY-CLOUDRUN-CONFIG-001 · Cloud Run MVP Preview Deployment

## 1. Purpose

This document describes the minimal Google Cloud Run setup for a controlled
operator-test deployment of the Alpha Solver MVP preview route:

```text
/dashboard/expert-preview
```

The first deployment is intended to make the already-implemented supervised
preview reachable behind the existing dashboard password gate. It is a deployment
configuration and operator-smoke lane only.

## 2. Scope boundaries

This lane adds Cloud Run deployment config and documentation only. It does not:

- deploy the service from Codex;
- change Alpha Solver runtime behavior;
- change provider expert-pass behavior;
- change clarify behavior;
- change eval artifact behavior;
- change behavioral demo checklist behavior;
- change preview behavior;
- change dashboard auth behavior;
- enable live OpenAI calls by default;
- add Firebase Hosting;
- add custom domain setup;
- update Google Sheets or backlog workbooks.

The root `Dockerfile` is Cloud Run-specific. The existing
`infrastructure/Dockerfile` is a generic placeholder image and does not start the
FastAPI app, so it should not be used as-is for this preview service.

## 3. Required Cloud Run settings

Suggested first service settings:

| Setting | Recommendation |
| --- | --- |
| Service name | `alpha-solver-mvp-preview` |
| Region | Choose a nearby region such as `us-central1` or `us-east1` |
| Runtime | Container from the root `Dockerfile` |
| CPU / memory | Start with 1 CPU / 512 MiB, or Cloud Run defaults if sufficient |
| Min instances | `0` |
| Max instances | `1` or `2` for controlled testing |
| Ingress | Cloud Run HTTPS service URL only for this phase |
| Cloud Run auth | `--allow-unauthenticated` is acceptable for controlled testing only because `/dashboard/*` is password-gated by the app; this is not a production-readiness claim |
| Provider mode | `MODEL_PROVIDER=local` |

Do not configure Firebase Hosting, a custom domain, or production traffic routing
for this phase.

## 4. Required environment variables

### Local-provider first deployment

Configure these variables before enabling dashboard access:

```text
MODEL_PROVIDER=local
ALPHA_DASHBOARD_PASSWORD=<strong non-default password>
ALPHA_DASHBOARD_SECRET_KEY=<long random secret>
```

`ALPHA_DASHBOARD_PASSWORD` must not be `alpha-dashboard`, and
`ALPHA_DASHBOARD_SECRET_KEY` must be explicitly set to a non-empty value. If the
password is missing/default or the secret key is missing/empty, the bundled app
fails closed and does not mount `/dashboard/*` routes.

If the Cloud Run service is reachable without Cloud Run IAM, also set a strong
API key for the JSON API surface instead of relying on development defaults:

```text
SERVICE_AUTH_KEYS=<strong random API key>
```

or:

```text
API_KEY=<strong random API key>
```

### Held live-provider variables

These variables are held until after local-provider Cloud Run smoke testing
succeeds and live-provider spend is explicitly approved:

```text
MODEL_PROVIDER=openai
OPENAI_API_KEY=<test-project-key>
ALPHA_LIVE_PREVIEW_ENABLED=true
ALPHA_LIVE_PREVIEW_MAX_REQUESTS=<low integer cap, for example 1 or 2>
```

Do not configure `OPENAI_API_KEY` for the first local-provider preview. Do not
switch `MODEL_PROVIDER` from `local` to `openai` until the operator explicitly
approves live-provider testing after the live-preview spend guard is merged and
deployed.

`ALPHA_LIVE_PREVIEW_ENABLED` defaults to fail-closed behavior. When
`MODEL_PROVIDER=openai` but `ALPHA_LIVE_PREVIEW_ENABLED` is unset or false,
`/dashboard/expert-preview` blocks preview submissions before constructing or
calling the provider client. `ALPHA_LIVE_PREVIEW_MAX_REQUESTS` is a per-process
request cap for the preview form; when unset, the app uses a very low default of
`1` allowed preview submission per service instance. Set it explicitly to the
lowest number needed for the approved operator test window.

## 5. Secret handling

For quick local-only container testing, placeholders may be passed as environment
variables. Do not reuse those placeholders for a real Cloud Run preview.

For controlled Cloud Run testing, prefer Secret Manager for sensitive values:

- `ALPHA_DASHBOARD_PASSWORD`
- `ALPHA_DASHBOARD_SECRET_KEY`
- any future `OPENAI_API_KEY`

Non-sensitive values such as `MODEL_PROVIDER=local` can be plain Cloud Run
environment variables.

Never commit secrets, paste real secrets into this document, or put real secrets
in deployment commands checked into git.

## 6. Local build and run commands

Build the Cloud Run image locally:

```bash
docker build -t alpha-solver-cloudrun-preview .
```

Run it locally with placeholder preview values:

```bash
docker run --rm -p 8080:8080 \
  -e PORT=8080 \
  -e MODEL_PROVIDER=local \
  -e ALPHA_DASHBOARD_PASSWORD=local-non-default-password \
  -e ALPHA_DASHBOARD_SECRET_KEY=local-dashboard-secret \
  alpha-solver-cloudrun-preview
```

Then smoke-check the local container:

```bash
curl -i http://127.0.0.1:8080/healthz
curl -i http://127.0.0.1:8080/dashboard/expert-preview
```

The second command should redirect unauthenticated users to `/login` when both a
non-default dashboard password and dashboard secret key are configured.

## 7. Cloud Run deploy command examples

These commands are examples only. Replace project, region, image, and secret
names with operator-owned values. Do not paste real secrets into committed docs.

### Build and deploy from the root Dockerfile

```bash
PROJECT_ID=<google-cloud-project-id>
REGION=us-central1
SERVICE=alpha-solver-mvp-preview
IMAGE="gcr.io/${PROJECT_ID}/${SERVICE}:preview"

gcloud builds submit --project "${PROJECT_ID}" --tag "${IMAGE}" .

gcloud run deploy "${SERVICE}" \
  --project "${PROJECT_ID}" \
  --region "${REGION}" \
  --image "${IMAGE}" \
  --allow-unauthenticated \
  --cpu 1 \
  --memory 512Mi \
  --min-instances 0 \
  --max-instances 2 \
  --set-env-vars MODEL_PROVIDER=local \
  --set-secrets ALPHA_DASHBOARD_PASSWORD=alpha-dashboard-password:latest,ALPHA_DASHBOARD_SECRET_KEY=alpha-dashboard-secret-key:latest
```

If Secret Manager is not being used for an initial disposable test, set only
non-sensitive placeholders in commands and configure real sensitive values in the
Cloud Run console or through an operator-controlled secret process.

### Temporary fail-closed mount verification

To verify fail-closed behavior, deploy or revise a temporary test revision with
`ALPHA_DASHBOARD_PASSWORD` unset, `ALPHA_DASHBOARD_PASSWORD=alpha-dashboard`, or
a non-default password but missing/empty `ALPHA_DASHBOARD_SECRET_KEY`, then
request:

```bash
curl -i "${SERVICE_URL}/dashboard/expert-preview"
```

Expected result: dashboard routes should not mount, so the route should return
404 rather than exposing the preview behind a default password or an ephemeral
runtime signing secret.

## 8. Post-deploy smoke-test checklist

Use the Cloud Run service URL as `SERVICE_URL`.

### Service health

- [ ] Cloud Run revision becomes ready.
- [ ] `GET /healthz` returns 200.
- [ ] `GET /readyz` returns 200, if readiness is expected.

```bash
curl -i "${SERVICE_URL}/healthz"
curl -i "${SERVICE_URL}/readyz"
```

### Dashboard fail-closed behavior

- [ ] With `ALPHA_DASHBOARD_PASSWORD` unset, `/dashboard/expert-preview` does not mount.
- [ ] With `ALPHA_DASHBOARD_PASSWORD=alpha-dashboard`, `/dashboard/expert-preview` does not mount.
- [ ] With a non-default password but missing/empty `ALPHA_DASHBOARD_SECRET_KEY`, `/dashboard/expert-preview` does not mount.
- [ ] With a non-default password and non-empty `ALPHA_DASHBOARD_SECRET_KEY`, `/dashboard/expert-preview` mounts and is protected by auth.

### Route and auth checks

- [ ] Logged-out `GET /dashboard/expert-preview` redirects or blocks according to dashboard auth convention.
- [ ] Login works with the configured dashboard password.
- [ ] Login redirects to `/dashboard/expert-preview`, not `/requests`.
- [ ] `/requests` remains unmounted in the bundled preview app.
- [ ] Authenticated `GET /dashboard/expert-preview` returns 200.

Example cookie-jar flow:

```bash
curl -i -c /tmp/alpha-cookies.txt \
  -d "password=${ALPHA_DASHBOARD_PASSWORD}" \
  "${SERVICE_URL}/login"

curl -i -b /tmp/alpha-cookies.txt \
  "${SERVICE_URL}/dashboard/expert-preview"
```

### CSRF checks

- [ ] Authenticated `POST /dashboard/expert-preview` without `X-Alpha-CSRF` is rejected.
- [ ] Authenticated `POST /dashboard/expert-preview` with the `alpha_dashboard_csrf` cookie value in `X-Alpha-CSRF` succeeds.

```bash
curl -i -b /tmp/alpha-cookies.txt \
  -d "prompt=hello" \
  "${SERVICE_URL}/dashboard/expert-preview"

CSRF_TOKEN=$(awk '$6 == "alpha_dashboard_csrf" {print $7}' /tmp/alpha-cookies.txt | tail -n 1)

curl -i -b /tmp/alpha-cookies.txt \
  -H "X-Alpha-CSRF: ${CSRF_TOKEN}" \
  -d "prompt=Draft a short rollout checklist for a small internal preview." \
  "${SERVICE_URL}/dashboard/expert-preview"
```

### Preview and safety checks

- [ ] Preview page renders in `MODEL_PROVIDER=local` mode.
- [ ] The supervised preview disclaimer is visible.
- [ ] No secrets, API keys, bearer tokens, auth headers, raw request bodies, raw response bodies, raw provider payloads, or raw provider metadata are displayed.

## 9. Fail-closed dashboard behavior

The bundled FastAPI app mounts dashboard auth plus `/dashboard/expert-preview`
only when `ALPHA_DASHBOARD_PASSWORD` is configured, is not the documented
default `alpha-dashboard`, and `ALPHA_DASHBOARD_SECRET_KEY` is explicitly set to
a non-empty value. Otherwise dashboard routes return 404 and the JSON API
continues serving. Preserve this behavior for Cloud Run. The auth module's
standalone random-secret fallback is intentionally unchanged for custom app
integrations, but the bundled Cloud Run preview mount guard must not rely on it.

## 10. Bundled preview login landing

The shared dashboard auth router defaults successful login to `/requests` for
custom/full-dashboard consumers. The Cloud Run preview service intentionally
mounts `/login` and `/dashboard/expert-preview`, but not the full legacy
dashboard request page. The bundled `service.app:app` integration therefore
configures successful login to redirect directly to `/dashboard/expert-preview`;
`/requests` remains unmounted in this preview app.

## 11. Local-provider first workflow

1. Build the root Dockerfile.
2. Run locally with `MODEL_PROVIDER=local` and placeholder dashboard values.
3. Confirm health, auth redirect, login, CSRF rejection, CSRF success, preview render, and safety checks.
4. Deploy to Cloud Run with `MODEL_PROVIDER=local`.
5. Repeat the Cloud Run smoke checklist.
6. Record results in the PR/release notes or operator handoff notes without adding MVP validation or production-readiness claims.

## 12. Held live OpenAI workflow

Live OpenAI preview is explicitly held until all of the following are true:

- local-provider Cloud Run smoke testing has succeeded;
- an operator explicitly approves live-provider spend;
- an operator provides a test-project OpenAI key through Secret Manager;
- bounded live smoke steps and rollback are documented.

Do not enable `MODEL_PROVIDER=openai` or configure `OPENAI_API_KEY` in the first
preview deployment.

## 13. Security notes

- Do not commit secrets.
- Do not paste real secrets into documentation or shell history that will be shared.
- Do not use `alpha-dashboard` as the dashboard password.
- Prefer Secret Manager for dashboard and provider secrets.
- Use a strong `SERVICE_AUTH_KEYS` or `API_KEY` if the Cloud Run service allows unauthenticated HTTP access.
- Keep max instances low during controlled testing.
- Treat Cloud Run unauthenticated access as a controlled-preview convenience only, not as production security posture.
- Keep live OpenAI held until explicitly approved.

## 14. Claim boundaries

This deployment config does not claim:

- MVP validation;
- Alpha Solver superiority;
- answer-quality superiority;
- production readiness;
- broad runtime readiness;
- answer-quality benchmark success;
- provider reasoning orchestration.

It only prepares the repo for a controlled Cloud Run MVP preview deployment.

## 15. Troubleshooting

| Symptom | Likely cause | Mitigation |
| --- | --- | --- |
| Cloud Run revision never becomes ready | Container is not listening on Cloud Run `PORT` or dependencies failed to install | Use the root `Dockerfile`; confirm the command starts Uvicorn with `--host 0.0.0.0 --port "${PORT:-8080}"` |
| `/dashboard/expert-preview` returns 404 | Dashboard password is unset/default or dashboard secret key is missing/empty | Configure a strong non-default `ALPHA_DASHBOARD_PASSWORD` and non-empty `ALPHA_DASHBOARD_SECRET_KEY`, then redeploy a new revision |
| Login redirects somewhere other than `/dashboard/expert-preview` | Bundled dashboard login redirect was not configured or regressed | Check `service.app:app` dashboard mounting and rerun the no-network UI tests |
| POST to preview returns 403 | Missing or invalid CSRF header | Send `X-Alpha-CSRF` with the value from the `alpha_dashboard_csrf` cookie |
| Preview attempts live provider calls | `MODEL_PROVIDER` is set to `openai` and live-preview opt-in/cap allowed the request | Revert to `MODEL_PROVIDER=local`; remove `OPENAI_API_KEY` from the first preview revision |
| Preview submit returns 403 with live preview disabled | `MODEL_PROVIDER=openai` without `ALPHA_LIVE_PREVIEW_ENABLED=true` | This is expected fail-closed behavior; keep held unless live-provider testing is explicitly approved |
| Preview submit returns 403 after one or a few live tests | `ALPHA_LIVE_PREVIEW_MAX_REQUESTS` cap reached for the Cloud Run instance | Stop testing or deploy a new approved revision with a low explicit cap |
| Secrets appear in output | Regression or unsafe manual logging | Stop testing, capture minimal evidence without secrets, rotate affected secrets, and fix before continuing |
| Cold starts are slow | `min-instances=0` | Accept for first testing or temporarily set `min-instances=1` for scheduled operator sessions |

## 16. Backlog impact

`DEPLOY-CLOUDRUN-CONFIG-001` should be marked Done only if the PR adding this
configuration is merged. This is a deployment-config/docs lane under
`DEPLOY-CLOUDRUN-EPIC-001`; it does not deploy the service, validate the MVP,
claim production readiness, or enable live OpenAI testing.
