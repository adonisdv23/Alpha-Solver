# Operator Runbook

This runbook is for future manual execution by Adonis on a Mac only after the review gate returns `AUTHORIZE_MANUAL_LOCAL_ORCHESTRATION_SMOKE`.

## 0. Stop condition

Stop immediately if any of the following is true:

- review gate has not returned `AUTHORIZE_MANUAL_LOCAL_ORCHESTRATION_SMOKE`;
- local endpoint is not localhost or loopback;
- hosted fallback is configured or observed;
- provider keys are required or requested;
- the command would expose `/v1/solve` or dashboard surfaces;
- the command would dump the full environment;
- the command would commit or import smoke results automatically.

## 1. Confirm target

Manual smoke target:

`alpha.local_llm.orchestration_runner.run_local_llm_solver_orchestration`

Target boundaries:

- non-production local orchestration runner only;
- local expert two-pass path only;
- local Ollama loopback endpoint only;
- no `/v1/solve` exposure;
- no dashboard exposure;
- no hosted fallback;
- no provider keys.

## 2. Prepare local runtime outside this packet

Adonis may configure a local Ollama loopback endpoint and local model on his Mac. This packet does not specify model quality requirements and does not validate local model quality.

Use placeholders until execution time:

- endpoint: `<LOCAL_OLLAMA_LOOPBACK_ENDPOINT>` such as `http://127.0.0.1:11434/api/chat`;
- model: `<LOCAL_OLLAMA_MODEL>`;
- timeout seconds: `<LOCAL_TIMEOUT_SECONDS>`.

## 3. Execute only after authorization

After authorization, run the command/script from [exact-command-template.md](exact-command-template.md) from repo root.

## 4. Capture artifacts

Capture artifacts under:

`docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-source-artifact/`

The capture must include command provenance, Python script provenance, stdout, stderr, redacted JSON output, and repo status.

## 5. Fill templates

After local execution, fill:

- [smoke-result-log-template.md](smoke-result-log-template.md)
- [artifact-capture-template.md](artifact-capture-template.md)
- [interpretation-template.md](interpretation-template.md)
- [final-decision-template.md](final-decision-template.md)

## 6. Preserve later

The future artifact folder requires a later source artifact preservation PR or equivalent repo-source preservation step. This packet does not import results and does not close the track.
