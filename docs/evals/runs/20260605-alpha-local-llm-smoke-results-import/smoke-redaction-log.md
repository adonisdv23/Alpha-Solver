# Smoke Redaction Log

Lane ID: `ALPHA-LOCAL-LLM-SMOKE-RESULTS-IMPORT-001`

## Redaction and sanitization checklist

- Provider keys removed or confirmed absent: confirmed absent in the pasted evidence.
- Secrets removed or confirmed absent: confirmed absent in the pasted evidence.
- Credentials removed or confirmed absent: confirmed absent in the pasted evidence.
- Private URLs removed or confirmed absent: confirmed absent in the pasted evidence.
- Nonpublic endpoints removed or confirmed absent: confirmed absent in the pasted evidence.
- Sensitive environment dumps removed or confirmed absent: confirmed absent; only machine, Python, model, version, endpoint pattern, timestamps, timeout, request summary, and response artifact are preserved.
- Endpoint shown only as localhost or loopback pattern: confirmed; preserved endpoint is `http://127.0.0.1:11434/api/chat`.
- Exact model name disclosed only because it is present in the pasted evidence and required for artifact preservation: `gemma3:4b`.
- stdout sanitized: confirmed; full system message is omitted while length and role order are preserved.
- stderr sanitized: no stderr content is present in the pasted evidence.

## Required preservation notes

The import preserves exact command result fields, timestamps, stdout-equivalent artifact contents, and operator notes from the pasted evidence unless redaction was required. No additional endpoint, access material, provider key, credential, or environment dump was added.
