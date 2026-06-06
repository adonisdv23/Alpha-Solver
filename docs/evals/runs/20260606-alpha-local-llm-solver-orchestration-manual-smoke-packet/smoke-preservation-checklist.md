# Smoke Preservation Checklist

Use this checklist before a future source artifact preservation PR or equivalent repo-source preservation step.

## Pre-execution checklist

- [ ] Review gate returned `AUTHORIZE_MANUAL_LOCAL_ORCHESTRATION_SMOKE`.
- [ ] Command will run from repo root.
- [ ] `PYTHONPATH` uses repo root.
- [ ] Endpoint is localhost or loopback.
- [ ] Model is local.
- [ ] Timeout is finite.
- [ ] No provider keys are configured or required.
- [ ] No hosted fallback is configured.
- [ ] No `/v1/solve` exposure is involved.
- [ ] No dashboard exposure is involved.

## Artifact checklist

- [ ] Redacted JSON output captured.
- [ ] Command provenance captured.
- [ ] Python script provenance captured.
- [ ] stdout captured.
- [ ] stderr captured.
- [ ] Repo status captured.
- [ ] Repo HEAD captured.
- [ ] Provider key values absent.
- [ ] Full environment dump absent.
- [ ] Private URLs absent.
- [ ] Private local paths replaced with `<REPO_ROOT>` or another approved placeholder.

## Boundary checklist

- [ ] `behavior_evidence=false` preserved.
- [ ] `no_hosted_fallback=true` preserved.
- [ ] `no_provider_keys_required=true` preserved.
- [ ] No local model quality claim added.
- [ ] No `/v1/solve` readiness claim added.
- [ ] No dashboard readiness claim added.
- [ ] No MVP validation claim added.
- [ ] No production readiness claim added.
- [ ] No benchmark evidence claim added.
- [ ] No provider orchestration evidence claim added.
- [ ] No Alpha superiority claim added.
- [ ] No evidence-model promotion claim added.
- [ ] No broad runtime readiness claim added.
