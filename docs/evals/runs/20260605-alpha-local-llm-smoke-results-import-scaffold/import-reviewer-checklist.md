# Import Reviewer Checklist

Lane ID: `ALPHA-LOCAL-LLM-SMOKE-RESULTS-IMPORT-SCAFFOLD-001`

This checklist is for a future reviewer. It is scaffold documentation only and does not import results.

## Source evidence gate

- [ ] `ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-001.md` exists.
- [ ] If the evidence file is missing, import stopped.
- [ ] Required fields are present.
- [ ] The exact command is copied from source evidence, not inferred.
- [ ] stdout, stderr, and exit code are copied from source evidence, not inferred.

## Redaction review

- [ ] No provider keys appear.
- [ ] No secrets appear.
- [ ] No credentials appear.
- [ ] No private URLs appear.
- [ ] No nonpublic endpoints appear.
- [ ] No sensitive environment dumps appear.
- [ ] Endpoint is sanitized to localhost or loopback pattern only.
- [ ] Exact model name appears only if approved for repo disclosure.

## Classification review

- [ ] Classification is exactly one of the allowed classifications.
- [ ] Classification is supported by source evidence.
- [ ] No smoke outcome is inferred from missing evidence.

## Claim boundary review

- [ ] Evidence boundary remains narrow.
- [ ] No readiness claim is introduced.
- [ ] No validation claim is introduced.
- [ ] No superiority claim is introduced.
- [ ] No benchmark success claim is introduced.
- [ ] No billing claim is introduced.
- [ ] No provider-orchestration claim is introduced.
- [ ] No production claim is introduced.
- [ ] No local-LLM-quality claim is introduced.
