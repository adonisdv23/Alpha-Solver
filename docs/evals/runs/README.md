# Eval Runs

This directory is the committed home for sanitized, summary-level future eval
run artifacts. Use `docs/evals/templates/run_report_template.md` for new run
reports and follow `docs/evals/ARTIFACT_PRESERVATION.md` before committing any
artifact.

Do not store raw provider payloads, secrets, dashboard credentials, cookies,
CSRF tokens, session values, provider account identifiers, full unredacted
request/response traces, or private user data unless explicitly sanitized and
needed.
