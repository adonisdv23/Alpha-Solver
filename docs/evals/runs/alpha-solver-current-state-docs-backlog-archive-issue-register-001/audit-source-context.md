# Audit source context & verification

## Sources incorporated

1. Regular Claude Opus strategic audit (hypotheses).
2. Claude Code deep technical/source/security/spec audit (hypotheses).
3. Current live repo evidence (committed files + read-only GitHub state).
4. Recent merged PRs and evidence packets (#497–#509).

## Critical source rule applied

Audit findings were treated as **hypotheses to verify, not proof**. Each was
checked against committed repo files. Findings not verifiable from repo evidence
are marked `UNVERIFIED_AUDIT_INPUT`. We did **not** invent missing evidence,
**not** reconstruct missing Fable audit text, **not** treat operator-held
material as repo evidence, **not** treat planning packets as execution evidence,
and **not** treat OpenAI smoke as provider validation.

Classification legend: `CONFIRMED` · `PARTIALLY_CONFIRMED` · `UNVERIFIED` ·
`NOT_FOUND` · `CONTRADICTED`.

## Strategic audit inputs

| # | input | class | evidence / note |
|---|-------|-------|-----------------|
| 1 | Extensive evidence discipline, core value unresolved | CONFIRMED | Large disciplined packet history; no value experiment exists |
| 2 | Alpha-vs-plain experiments mixed/noisy (neg/pos/small-pos) | PARTIALLY_CONFIRMED | `.specs/EVAL-DIFFERENTIATION-RUN-001.md`, `.specs/OUTPUT-DIFF-*`, `.specs/HIGHER-HEADROOM-EVAL-001.md` exist; specific result distribution not re-scored here |
| 3 | Alpha penalized for verbosity → control brevity | PARTIALLY_CONFIRMED | `.specs/ALPHA-BREVITY-CONTROL-001.md` exists |
| 4 | First OpenAI smoke is plumbing only, not value proof | CONFIRMED | #502–#509 framed as plan/governance/smoke; #509 blocked before call |
| 5 | Risk of infrastructure accrual if packets keep accruing without value | CONFIRMED | Many packets vs zero value proof; this lane explicitly routes toward a value protocol |
| 6 | Local qwen smoke failed through retry 007; not success | PARTIALLY_CONFIRMED | Retry chain `…manual-smoke-retry-{002..007}…` exists; **retry-007 runner exit=0**; Level-3 closeout accepted only as **non-promotional artifact evidence** (`behavior_evidence=False`). Must **not** be mistaken for value/quality success |
| 7 | Real Alpha-vs-baseline protocol is a near-term priority | CONFIRMED | Recorded as top strategic opportunity; see `value-experiment-direction.md` |

## Claude Code deep technical audit inputs

| # | input | class | evidence / note |
|---|-------|-------|-----------------|
| 1 | No committed real secrets | CONFIRMED | `.env` gitignored; `dashboard_api_keys.json` not committed; redaction module present (not exhaustively re-scanned) |
| 2 | CI/workflows do not call providers | CONFIRMED | grep of `.github/workflows/*` → no `openai`/`anthropic` refs |
| 3 | Runtime/provider surfaces fail-closed by default | PARTIALLY_CONFIRMED | Telemetry allowlist; no SDK; httpx plumbing; full fail-closed not exhaustively verified |
| 4 | alpha/ and service/ are two overlapping stacks | CONFIRMED | Both carry providers/finops/observability/determinism/prompts/validation |
| 5 | Multiple entrypoints and monolith/reference files | CONFIRMED | `alpha_solver_portable.py` (977-line monolith), `alpha-solver-v91-python.py`, `alpha_solver_entry.py`, `alpha_solver_cli.py`, `service/app.py`; `docs/ENTRYPOINTS.md` |
| 6 | requirements small; no OpenAI/Anthropic SDK | CONFIRMED | `requirements.txt` (9 deps); `pyproject.toml` |
| 7 | Provider calls use httpx-style plumbing not SDK | CONFIRMED | httpx in deps; no SDK present |
| 8 | Security machinery exists (auth/redaction/audit/tenancy/validation/classification) | CONFIRMED | `service/{auth,audit,tenancy,validation}/`, `alpha/self_operator/{redaction,command_classification}.py` |
| 9 | DEF-002 better framed as assessment/threat-model/closure, not build-from-scratch | CONFIRMED | Follows from #8; machinery exists, gaps need review |
| 10 | CORS default risk | CONFIRMED | `alpha/core/config.py` origins default `*`; `service/app.py` `allow_credentials=True` |
| 11 | FileSecretsBackend (plaintext secret storage) risk | CONFIRMED | `alpha/webapp/routes/settings.py` writes raw keys as JSON |
| 12 | Provider telemetry may expose prompt content | CONTRADICTED (default path) / UNVERIFIED (opt-in) | `alpha/providers/telemetry.py` is allowlist-based, "never inspects payloads"; residual opt-in/verbose paths not exhaustively reviewed |
| 13 | commit.gpgsign=true breaks throwaway-git-repo test hermeticity | CONFIRMED | `git config` + PR #497 documents 2 failing tests |
| 14 | Hardcoded pricing | PARTIALLY_CONFIRMED | `service/finops/pricing.py` YAML + hardcoded `MODEL_SETS`; config defaults |
| 15 | Duplicate/overlapping OpenAI adapter/provider surfaces | CONFIRMED | `alpha/providers/*`, `alpha/local_llm/provider_adapter.py`, `service/adapters/`, `service/mcp/` |
| 16 | Sanitizer lacks Unicode normalization | CONFIRMED | `alpha/self_operator/redaction.py` regex-only, no `unicodedata`/NFKC |
| 17 | Orphaned docs / duplicated MVP docs | PARTIALLY_CONFIRMED | `docs/MVP_*` ↔ `.specs/MVP-*` overlap |
| 18 | Stale branches or stale refs | CONFIRMED | 60+ remote branches incl. merged `codex/*`, `claude/*`, `adonisdv23-patch-*` |
| 19 | ROADMAP stale / old PRs / wrong org links | CONFIRMED | `docs/ROADMAP.md` #91–#99, `github.com/alpha-solver/...` |
| 20 | `.specs` MCP-002 / NEW-010 carry MCP-005 Error Taxonomy under unrelated titles | CONFIRMED (systemic) | 22 `.specs/` files carry the taxonomy body; see `spec-health-findings.md` |

## UNVERIFIED_AUDIT_INPUT

No audit input required this marker in this pass — each was either verifiable
against committed files or recorded as `PARTIALLY_CONFIRMED`/`CONTRADICTED` with
the specific repo evidence. The prior Fable delta-audit full text remains
**not committed** and was **not reconstructed** (tracked as DEF-003).
