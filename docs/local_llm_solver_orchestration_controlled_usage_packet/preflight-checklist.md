# Preflight Checklist

Use this checklist only in a future separately approved controlled usage operator-run lane. Do not use this packet as authorization to run the command.

## Repo and command identity

- [ ] Record repo HEAD before running.
- [ ] Record repo status before running.
- [ ] Confirm the command identity is exactly:

```text
python -m alpha.local_llm.operator_cli
```

- [ ] Confirm no source or test changes are present unless explicitly authorized by the future lane.

## Local-only runtime settings

- [ ] Confirm explicit opt-in is present: `--enable-local-llm`.
- [ ] Confirm exactly one prompt source is used: `--prompt`, `--prompt-file`, or `--prompt-stdin`.
- [ ] Confirm endpoint is loopback only, for example `http://127.0.0.1:11434/api/chat` or another accepted loopback form.
- [ ] Confirm endpoint is not a hosted, remote, public, container-external, or non-loopback URL.
- [ ] Confirm timeout is finite and positive.
- [ ] Confirm the model value is the exact local model name intended for the future run.
- [ ] Confirm no hosted provider keys are required.
- [ ] Confirm no hosted provider keys are accepted as wrapper inputs.
- [ ] Confirm no hosted fallback is configured.
- [ ] Confirm no provider fallback is configured.

## Boundary checks

- [ ] Confirm the future command does not expose or call `/v1/solve`.
- [ ] Confirm the future command does not expose or call dashboard routes.
- [ ] Confirm the future command does not update Google Sheets.
- [ ] Confirm the future command does not update backlog workbooks.
- [ ] Confirm the future lane is not evidence-model promotion.

## Expected output flags

The future result must be stopped and treated as invalid for this controlled usage process unless output artifacts confirm:

- [ ] `behavior_evidence=false`.
- [ ] `no_hosted_fallback=true`.
- [ ] `no_provider_keys_required=true`.
