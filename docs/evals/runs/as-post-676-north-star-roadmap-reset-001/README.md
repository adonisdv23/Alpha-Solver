# AS-POST-676-NORTH-STAR-ROADMAP-RESET-001

## TLDR

This source-truth reset pauses further UI and real-run cockpit implementation until the operator selects a product direction. The post-#663 through post-#676 Operator Console sequence improved local-first visibility and operator-facing status, but human validation after PR #676 exposed a north-star question: Alpha Solver should remain centered on reasoning/routing plus discrimination/evidence, not drift into a generic LLM cockpit.

## Why this reset exists

After PR #676, the operator still asked how to use the page, whether it was just an FAQ/status page, whether the team was building in the right direction, and whether the work aligned with Alpha Solver's original goal. That feedback requires a roadmap/source-truth reset before any B012 cockpit implementation or B013 real-run provider work.

## Source-truth baseline

- Main baseline verified through GitHub API: `bef685c43676019c0de97157935b4f3b60f177d0`.
- PR #676 was verified merged with that merge commit.
- Open PR list was verified empty before editing.
- No equivalent post-#676 north-star reset packet was found before this packet was created.

## PR #663 through #676 sequence summary

- #663: case-packet anchor preflight CLI.
- #664: protected local-first Operator Console shell.
- #665: local artifact status.
- #666: artifact freshness and sequence coherence.
- #667: provider/model/cost gate panel.
- #668: Dry-Run Preview.
- #669: Local Receipt Store.
- #670: ChatGPT copy/paste capture guidance.
- #671: process hardening no-provider-call/write-boundary test helper.
- #672: Manual Next Step Guide.
- #673: First 5 Minutes docs.
- #674: Daily-Use Walkthrough docs.
- #675: progressive disclosure.
- #676: flow-first orientation band.

## North-star diagnosis

Alpha Solver's primary product identity is reasoning/routing plus discrimination/evidence. Recent Operator Console work is adjacent and useful when tied to Value Read, route/expert preview, capture, receipts, SAFE-OUT/confidence inspection, or evidence-boundary workflows. It is not enough by itself to select a generic cockpit or playground direction.

## Product direction options

| Option | Direction | Classification |
|--------|-----------|----------------|
| A | Bounded smoke-test cockpit | Useful support surface, not core product proof. |
| B | Value Read / discrimination workbench | Strongest north-star alignment. |
| C | Route and expert-preview control surface | Strong alignment with reasoning/routing layer. |
| D | CLI/artifact operator companion | Safe and aligned support surface. |
| E | Full real-run Operator Cockpit | Potentially useful later, but too broad unless bounded by prior decisions. |
| F | Read-only status checkpoint | Already built enough for current evidence needs; not next. |

See `product-direction-options.md` for the full options table.

## Selected next state

`OPERATOR_REVIEW_REQUIRED_AFTER_POST_676_NORTH_STAR_ROADMAP_RESET_001`

This selected next state is a review/decision state, not an implementation lane. No B012 implementation, B013 real-run provider work, provider calls, `/v1/solve` exposure, scoring, unblinding, final interpretation, value claim, readiness claim, or superiority claim is authorized by this reset.

## Non-actions

This lane does not implement runtime code, modify provider execution, modify Operator Console runtime behavior, modify webapp routes, add UI behavior, add routes, add POST routes, create a real-run cockpit, call providers, run models, expose `/v1/solve`, create action controls, create a generic LLM playground, score outputs, unblind results, reveal source identities, or mutate Google Sheets.

## Non-claims

This lane makes no value, readiness, benchmark, provider-validation, local-model-validation, production, public-readiness, security/privacy, or Alpha-superiority claim.

## Validation checks

Recorded in `checks-run.md`:

- GitHub API live-state preflight.
- Required source-truth and recent spec inspection.
- Existing-reset search.
- `git diff --check`.
- Narrative claim-safety check over the packet, spec, and updated source-truth docs.
