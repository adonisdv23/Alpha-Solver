# Evidence packet template

Lane ID: `ALPHA-SOLVER-LOCAL-MODEL-LAB-OLLAMA-SINGLEPATH-001`

## Run metadata

- Run date/time:
- Operator:
- Repo commit:
- Exact model: `gemma3:4b`
- Endpoint: `http://127.0.0.1:11434/api/chat`
- Timeout seconds: `30`
- Prompt fixture: synthetic toy note only
- Execution surface: `python -m alpha.local_llm.operator_cli`

## Boundary attestations

- Hosted provider calls: `0`
- Tokens used for hosted providers: `0`
- Provider credentials required: `no`
- Model pulls or installs performed by this lane: `0`
- Private data used: `no`
- `/v1/solve` exposure: `no`
- Dashboard exposure: `no`
- Public API exposure: `no`
- Multi-model routing or council work: `no`
- Scoring or benchmarking: `no`

## Smoke result

Record one of:

- `LOCAL_SMOKE_NOT_RUN_OPERATOR_AUTHORIZATION_REQUIRED`
- `LOCAL_SMOKE_BLOCKED_PREREQUISITE_MISSING`
- `LOCAL_SMOKE_COMPLETED_NON_BEHAVIOR_EVIDENCE`

## Output capture

Paste or attach only bounded local CLI output. Do not include private data, tokens, hosted provider output, benchmark scores, model-quality assertions, or Alpha superiority claims.
