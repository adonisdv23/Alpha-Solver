# Smoke Result Log Template

Lane ID: `ALPHA-LOCAL-LLM-SMOKE-RESULTS-IMPORT-SCAFFOLD-001`

This is a header-only template. It intentionally contains no actual result row and does not infer any smoke outcome.

## Allowed result classifications

- `not run`
- `skipped`
- `blocked`
- `pass`
- `fail`
- `error`
- `timeout`
- `connection failure`
- `endpoint locality rejection`
- `malformed response`
- `empty output`
- `prompt echo`
- `system echo`

## Future log columns

| source evidence file | lane ID | prerequisite PR link | command recorded | endpoint pattern | model disclosed | timeout seconds | start timestamp | end timestamp | exit code | executed/skipped/blocked | classification | stdout sanitized | stderr sanitized | raw artifact notes present | redaction notes present | evidence boundary present | non-claims present |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
