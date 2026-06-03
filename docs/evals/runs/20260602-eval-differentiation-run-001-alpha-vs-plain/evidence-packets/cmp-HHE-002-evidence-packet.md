# cmp-HHE-002 · Evidence Packet

## Packet identity

| Field | Value |
| --- | --- |
| `packet_id` | `cmp-HHE-002-evidence-packet` |
| `comparison_id` | `cmp-HHE-002` |
| `parent_run_id` | `20260602-eval-differentiation-run-001-alpha-vs-plain` |
| `run_directory` | `docs/evals/runs/20260602-eval-differentiation-run-001-alpha-vs-plain/` |
| `prompt_id` | `HHE-002` |
| `prompt_family` | `higher-headroom release-note claim boundary` |
| `difficulty_headroom` | `high` |
| `evidence_strength` | `repo-preserved-sanitized-artifact; official-blind-scorer-result` |
| `non_claims_confirmed` | `yes` |

## Source artifact references

| Source artifact | Path |
| --- | --- |
| `blinded_score_sheet path` | `blinded-score-sheet.csv` |
| `blinding_map path` | `blinding-map.csv` |
| `paired_output_capture path` | `paired-output-captures/cmp-HHE-002-paired-output-capture.md` |
| `comparison_score_table path` | `score-table.csv` |
| `run_report path` | `run-summary.md` |

Storage boundary: this packet indexes sanitized artifacts already preserved under `docs/evals/runs/` and does not duplicate raw provider payloads, provider account identifiers, private user data, full traces, environment dumps, dashboard credentials, cookies, CSRF/session values, or credential strings.

## Blinded scoring and unblinding record

- Blinded scoring completed before unblinding: yes, per operator packet and Source Packet B confirmations.
- Scorer used only Output A / Output B labels: yes.
- Unblinding applied after scoring: yes, using the operator-approved map.
- Plain surface after unblinding: Output A
- Alpha surface after unblinding: Output B

## Score decision aid

| Field | Value |
| --- | ---: |
| `plain_total` | 55 |
| `alpha_total` | 52 |
| `total_delta` | -3 |
| `winning_surface` | Plain |

See `score-table.csv` for all 14 dimensions. Do not rescore from this packet.

## Evidence-limited explanation

The official blind scorer preferred Output A for `cmp-HHE-002`. After applying the approved unblinding map, the plain total is 55, the Alpha total is 52, and the Alpha-minus-plain delta is -3. This is a local result for this one comparison only.

## Conservative interpretation

Outcome label: `Plain local advantage`.

This packet supports only a local, evidence-limited observation for one prompt in one four-comparison A3-1 run. It does not support broad claims about Alpha Solver, plain providers, product readiness, or benchmark success.

## Redactions performed

- Redactions performed: none required for synthetic prompt/output text.
- Sanitization reviewer: artifact population pass.
- Storage boundary confirmed: yes.
- Omitted unsafe material: raw provider payloads, response IDs, headers, cookies, auth tokens, environment dumps, private data, and secret-like values.

## Non-claims

This packet does not claim MVP validation, Alpha Solver superiority, answer-quality superiority, production readiness, broad runtime readiness, benchmark success, exact billing accuracy, or provider reasoning orchestration.
