# Eval Runs

This directory is the committed home for sanitized, summary-level future eval
run artifacts. Use `docs/evals/templates/run_report_template.md` for new run
reports and follow `docs/evals/ARTIFACT_PRESERVATION.md` before committing any
artifact.

Do not store raw provider payloads, secrets, dashboard credentials, cookies,
CSRF tokens, session values, provider account identifiers, full unredacted
request/response traces, or private user data unless explicitly sanitized and
needed.

Future Alpha-vs-plain comparison runs may also store side-by-side evidence
packets derived from `docs/evals/templates/side_by_side_evidence_packet_template.md`;
those packets are review/index/interpretation artifacts only and must reference,
not replace, the score table, paired-output capture, blinded score sheet,
blinding map, and run report.
