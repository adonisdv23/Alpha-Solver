# Redaction Log Template

Lane ID: `ALPHA-LOCAL-LLM-SMOKE-RESULTS-IMPORT-SCAFFOLD-001`

This template defines future redaction requirements. It is not evidence that any smoke command ran.

## Required redaction rules

A future import must ensure:

- no provider keys
- no secrets
- no private URLs
- no nonpublic endpoints
- no sensitive environment dumps
- endpoint sanitized to localhost or loopback pattern only

## Future redaction checklist

- Provider keys removed or confirmed absent: `[future importer to fill]`
- Secrets removed or confirmed absent: `[future importer to fill]`
- Credentials removed or confirmed absent: `[future importer to fill]`
- Private URLs removed or confirmed absent: `[future importer to fill]`
- Nonpublic endpoints removed or confirmed absent: `[future importer to fill]`
- Sensitive environment dumps removed or confirmed absent: `[future importer to fill]`
- Endpoint shown only as localhost or loopback pattern: `[future importer to fill]`
- Exact model name disclosed only if approved for repo disclosure: `[future importer to fill]`
- stdout sanitized: `[future importer to fill]`
- stderr sanitized: `[future importer to fill]`
- raw artifact preservation notes sanitized: `[future importer to fill]`

## Redaction stop condition

If the future importer cannot remove or safely summarize sensitive content, import must stop rather than partially importing the result.
