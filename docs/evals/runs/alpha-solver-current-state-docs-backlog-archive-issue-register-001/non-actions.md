# Non-actions

What this lane did **not** do (by design):

- Did not call OpenAI or any provider; used no tokens; ran no evals; ran no
  product runtime; performed no deployment.
- Did not expose `/v1/solve` or any dashboard; did not access credentials; did
  not print secrets; did not update Google Sheets.
- Did not edit runtime/product code, provider/model code, tests, or CI.
- Did not modify the static-checker scripts (`scripts/check_local_llm_*.py`) or
  their tests.
- Did not delete any evidence packet; did not mutate historical evidence content.
- Did not reconstruct the missing Fable delta-audit text (DEF-003 remains open).
- Did not rewrite contaminated `.specs/*` files from memory (recommended a
  reconciliation lane instead).
- Did not resolve DEF-002 or DEF-003; did not fix CORS, secrets-at-rest,
  redaction, pricing, architecture overlap, or branches — these are recorded as
  inputs/issues for future lanes.

What it did: read-only GitHub/repo verification, audit-finding verification
against committed files, and creation/update of docs-only navigation/governance
files plus this evidence packet.
