# Technical Debt and Runtime Notes

> Created by lane `ALPHA-SOLVER-CURRENT-STATE-DOCS-BACKLOG-ARCHIVE-ISSUE-REGISTER-001`.
> Verification date **2026-06-13**. Verified against committed files. **No
> runtime/product/provider/test/CI code is changed in this lane** — these are
> recorded inputs. Each item is classified: `BLOCKS_SMOKE` ·
> `BLOCKS_PUBLIC_RUNTIME` · `AFTER_SMOKE` · `AFTER_VALUE_PROTOCOL` ·
> `LATER_HARDENING`.

| item | status | evidence path | classification |
|------|--------|---------------|----------------|
| **alpha/service overlap** | CONFIRMED | both `alpha/` and `service/` carry providers, finops, observability, determinism, prompts, validation | `LATER_HARDENING` (document canonical runtime path before public; ISS-012) |
| **Multiple entrypoints** | CONFIRMED (documented as intentional) | `alpha_solver_portable.py` (977-line portable monolith), `alpha-solver-v91-python.py` (modular reference), `alpha_solver_entry.py` (import bridge), `alpha_solver_cli.py`, `service/app.py`; roles in `docs/ENTRYPOINTS.md` | `LATER_HARDENING` (intentional; keep the map current) |
| **Duplicate provider/adapter surfaces** | CONFIRMED | `alpha/providers/{openai,base,fake,accounting,safeout,telemetry}.py`, `alpha/local_llm/provider_adapter.py`, `service/adapters/`, `service/mcp/` | `BLOCKS_PUBLIC_RUNTIME` (pick canonical adapter before public; ISS-008) |
| **Hardcoded pricing** | PARTIALLY_CONFIRMED | `service/finops/pricing.py` (YAML `config/cost_models.yaml` + hardcoded `MODEL_SETS`), `alpha/core/config.py` cost defaults | `AFTER_SMOKE` (consolidate pricing source-of-truth; ISS-007) |
| **Sanitizer Unicode normalization** | CONFIRMED gap | `alpha/self_operator/redaction.py` — regex only, no `unicodedata`/NFKC | `BLOCKS_PUBLIC_RUNTIME` (redaction-evasion risk; ISS-009) → DEF-002 |
| **Commit-signing test hermeticity** | CONFIRMED | `git config commit.gpgsign=true`, `gpg.ssh.program=/tmp/code-sign`; throwaway-repo tests fail: `tests/test_smoke_quickstart.py::test_release_script`, `tests/test_tag_release.py::test_tag_release` (per PR #497) | `LATER_HARDENING` (test-env hermeticity; do not edit tests here; ISS-006) |
| **Orphan / duplicate MVP docs** | PARTIALLY_CONFIRMED | `docs/MVP_READINESS_CHECKPOINT.md` ↔ `.specs/MVP-READINESS-CHECKPOINT-001.md`; `docs/MVP_TESTER_HANDOFF.md`; `.specs/MVP-CLOSEOUT-001.md` | `LATER_HARDENING` (dedup; operator decision; ISS-010) |
| **Stale branches / refs** | CONFIRMED | GitHub `list_branches`: 60+ branches incl. merged `codex/*`, `claude/*`, `adonisdv23-patch-*`, `batch-c-artifact-*` | `LATER_HARDENING` (operator branch cleanup; ISS-011) |

## Notes

- **Nothing here `BLOCKS_SMOKE`.** The next tiny synthetic smoke is gated only on
  OpenAI project/billing clarification (ISS-015), not on technical debt.
- `BLOCKS_PUBLIC_RUNTIME` items (duplicate adapters, redaction normalization)
  must be resolved before any public/runtime/provider exposure.
- Multiple entrypoints are **intentional** per `docs/ENTRYPOINTS.md`; the debt is
  keeping the architecture map current, not collapsing the files.
- This lane records inputs only; remediation happens in dedicated future lanes.
