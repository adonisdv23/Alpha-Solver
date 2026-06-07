# Operator Runbook

This runbook is for a future controlled usage operator-run lane only. This packet does not start that lane and does not execute the controlled usage run.

## Step 1: prepare local prompt artifact

Create a bounded prompt file for the future run and record its path in the artifact log. The prompt must not request production integration, hosted provider use, benchmark comparisons, readiness conclusions, dashboard behavior, `/v1/solve` behavior, billing behavior, or evidence promotion.

## Step 2: perform preflight

Complete every item in `preflight-checklist.md` before execution. Stop if any item cannot be confirmed.

## Step 3: run exactly one controlled usage command

The future run should use the stable wrapper command identity and explicit local-only settings:

```bash
python -m alpha.local_llm.operator_cli \
  --enable-local-llm \
  --prompt-file ./controlled-usage-prompt.txt \
  --endpoint-url "http://127.0.0.1:11434/api/chat" \
  --model "<exact-local-model-name>" \
  --timeout-seconds "<finite-positive-timeout>" \
  > ./controlled-usage.stdout.json \
  2> ./controlled-usage.stderr.txt
```

Capture the exit code immediately after execution:

```bash
printf '%s\n' "$?" > ./controlled-usage.exit-code.txt
```

Do not add retries, fallback commands, alternate providers, hosted endpoints, dashboard calls, `/v1/solve` calls, smoke reruns, or benchmark loops.

## Step 4: normalize and redact artifacts

Create a redacted normalized JSON artifact from stdout. Preserve structural fields needed for review, including top-level status, metadata, and safety flags. Redact prompt content, unsafe diagnostic text, secrets, local usernames, machine paths, and raw model text if it contains sensitive content.

## Step 5: review result

Use `result-review-checklist.md`. The result is acceptable for Level 2 operator usability review only if no stop condition appears and all required provenance artifacts are present.

## Step 6: record non-actions

The future run record must explicitly state that it did not run hosted providers, expose `/v1/solve`, expose dashboard routes, add fallback, update Google Sheets, update backlog workbooks, or promote evidence.
