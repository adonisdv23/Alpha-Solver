# Validation Subject Under Test

## Future subject under test

The only future subject under test is the existing local LLM solver orchestration behavior reachable through the approved local-only operator CLI wrapper.

## Allowed invocation surface

The future frozen packet may reference only the operator wrapper shape:

```text
python -m alpha.local_llm.operator_cli --enable-local-llm --prompt ... --endpoint-url http://127.0.0.1:<port> --model <local-model> --timeout-seconds <finite-positive-seconds>
```

A future packet may choose `--prompt`, `--prompt-file`, or `--prompt-stdin`, but must freeze the exact choice before execution.

## Required exclusions

The subject under test excludes:

- production solver entrypoints;
- `/v1/solve`;
- dashboard routes;
- hosted provider adapters;
- provider fallback;
- hosted fallback;
- billing flows;
- benchmarks;
- Google Sheets or backlog workbook updates;
- evidence-model promotion mechanisms.

## Non-execution note

The invocation above is a design example only. This packet does not run it.
