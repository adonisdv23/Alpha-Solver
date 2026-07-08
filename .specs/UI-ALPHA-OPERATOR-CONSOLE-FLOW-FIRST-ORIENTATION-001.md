# UI-ALPHA-OPERATOR-CONSOLE-FLOW-FIRST-ORIENTATION-001 · Operator Console Flow-First Orientation Band

Lane id: `AOC-B010-OPERATOR-CONSOLE-FLOW-FIRST-ORIENTATION-001`

This lane adds a read-only orientation band. It does not add execution, routes,
write paths, action controls, or status JSON semantics.

## Goal

Add a read-only flow-first orientation band above the existing
`/dashboard/operator-console` card grid so a human operator can understand the
page in the first few seconds:

1. What this page is.
2. What this page is not.
3. Whether the console will run anything.
4. Whether anything needs immediate attention.
5. What manual next step, if any, happens outside the console.

This is a render-layer UX orientation lane only.

## Motivation

After the progressive-disclosure lane (PR #675), a daily operator opened the
protected Operator Console and reported that the local-first and
live-provider-disabled signals were clear, but that the page was still an
"enormous amount of text," its purpose remained unclear, and the console was
"still unusable." The operator asked, in effect, what the page is for and how it
is meant to be used.

The remaining problem is not only text density: the page lacks a flow-first
mental model. A short, always-visible orientation band at the top answers what
the page is, what it is not, its current safety posture, whether anything needs
attention, and what manual step happens outside the console. It makes the
existing console easier to understand without making it more powerful.

## Scope

- Add a `_render_orientation_band(status)` render helper that emits one
  always-visible `<section class="orientation-band" id="orientation-band">`
  containing five elements: a one-line purpose, static non-interactive posture
  chips, an attention summary, a next-manual-action line, and a details-below
  pointer.
- Add two pure summarization helpers over the already-assembled in-memory status
  dict: `_orientation_attention_items(status)` and
  `_orientation_next_action(status)`.
- Render the band near the top of the page, after the existing mode banner and
  before the existing `<div class="cards">` grid.
- Add minimal CSS for the band and the static posture chips.
- Keep the existing card grid, the mode banner, the disabled live-run control,
  every card title, and all existing boundary text exactly as they are.

### One-line purpose

The band renders exactly:

> This is a local-first status console. It helps you review current local state
> and decide the next manual step. It does not run, call, or execute anything.

### Static posture chips

Four static, non-interactive `<span>` labels: `Local-first`,
`Live provider calls: disabled`, `Non-executing / read-only`, and
`No API keys displayed`. They are not buttons, links, forms, inputs, or toggles;
they submit nothing and imply no state that can be changed from the console.

### Attention summary

A read-only summary derived only from existing status values already rendered by
the cards below. The safe default is
`No immediate attention detected from local metadata.` When existing status data
indicates a missing/invalid/stale condition, the band summarizes up to three
bounded items derived from the in-memory status dict:

- `Capture artifact missing.` — from `local_artifacts.capture.state == "missing"`.
- `Local capture cannot be read.` — from an invalid capture state.
- `Evidence packet digest needs attention.` — from a `digest_invalid` /
  `digest_unverifiable` evidence-packet state.
- `Derived artifacts appear older than capture.` — from an existing
  `*_older_than_capture` freshness warning in `dry_run_preview.freshness_warnings`.

The summary invents no readiness semantics and never uses "ready", "validated",
"all clear", "passed", "healthy", "production readiness", "benchmark", "winner",
or "superiority" wording.

### Next manual action

A read-only line derived from the first existing
`chatgpt_copy_paste_capture.next_manual_steps` label (underscores rendered as
spaces), stated plainly as happening outside the console, e.g.
`Next manual step outside the console: validate capture from terminal.` When no
step is available the safe default is
`No manual action required from this console view.` The line is not a button, is
not clickable, dispatches nothing, and does not say the console performs the
action.

### Details-below pointer

A quiet pointer: `Details below: review surfaces, manual-only steps, blocked
behavior, and receipts.` Orientation only.

## Non-goals

- No provider execution, ChatGPT API integration, browser automation,
  `/v1/solve`, dry-run execution, or CLI/subprocess/shell execution from the
  console.
- No paste storage, capture editor, raw prompt viewer, or raw output viewer.
- No scoring, ranking, winner selection, queue, runner, scheduler, or worker
  behavior.
- No action control of any kind, no new route, no new POST route, no new write
  path, no new status payload field, and no changed status JSON semantics.
- No removal, weakening, or paraphrase of any existing boundary text.
- No JavaScript, no full layout redesign, and no card reordering.
- No readiness, validation, benchmark, production, answer-quality, or
  superiority claim.

These capabilities are mentioned only as blocked, unavailable, or out of scope.

## Allowed files

- `alpha/webapp/routes/operator_console.py`
- `tests/test_operator_console.py`
- `docs/OPERATOR_CONSOLE.md`
- `.specs/UI-ALPHA-OPERATOR-CONSOLE-FLOW-FIRST-ORIENTATION-001.md`
- `.specs/INDEX.md`

## Implementation notes

- The band is presentation-only. `build_console_status()` returns the same shape
  as before; the band is assembled entirely inside `_render_page` from the
  status dict that function already receives.
- `_orientation_attention_items` and `_orientation_next_action` are pure
  summarization helpers over the existing in-memory status dict. They fetch no
  new data, read no raw artifact content, and add no new state semantics.
- The posture chips are static `<span>` labels with `cursor: default`; no
  chip is wrapped in an anchor, button, form, input, or toggle.
- All band text runs through the shared `_escape` helper, consistent with the
  rest of the page.
- The band uses no `<details>` / `<summary>`, so the progressive-disclosure
  counts and the first-glance-safety-visible assertions are unaffected.

## Definition of done

- The page renders an always-visible orientation band with an `orientation-band`
  id above the existing `<div class="cards">` grid.
- The band contains the one-line purpose, the four static posture chips, the
  attention summary, the next-manual-action line, and the details-below pointer.
- The posture chips are non-interactive (not buttons, links, forms, or toggles).
- The attention summary and next-manual-action line are derived only from
  existing status values, with safe defaults.
- `Local-first operator console`, `Live provider calls are disabled in this MVP`,
  `No API keys are displayed`, the existing claim-boundary text, the disabled
  live-run control, and every existing card id and title remain present.
- Status JSON shape and semantics are unchanged.
- Focused Operator Console tests pass.
- Documentation explains the band, the posture chips, why the attention summary
  is local-metadata-only, why the next manual action happens outside the console,
  and what it does not prove.

## Boundary checklist

- [x] Render-only presentation change.
- [x] Band rendered above the existing card grid; the grid is preserved.
- [x] Static, non-interactive posture chips (no buttons, links, forms, toggles).
- [x] Attention summary derived only from existing status values.
- [x] Next manual action derived only from existing next-step data; happens
      outside the console.
- [x] No JavaScript and no new frontend dependency.
- [x] No boundary text removed, weakened, or paraphrased.
- [x] First-glance safety signals remain visible.
- [x] No provider calls, ChatGPT calls, `/v1/solve`, browser automation, CLI,
      shell, or subprocess execution.
- [x] No prompt submission, paste storage, capture editor, or raw viewer.
- [x] No scoring, ranking, winner selection, queue, runner, scheduler, or worker.
- [x] No action control, new route, new POST route, or new write path.
- [x] No new status payload field and no changed status JSON semantics.
- [x] No new or renamed card id.
- [x] Local Receipt Store remains the only controlled write path.

## Non-claims

This lane does not claim readiness, validation success, benchmark validity,
production readiness, answer quality, scoring, ranking, winner selection,
provider readiness, billing accuracy, or model superiority. The band is a
presentation change that makes existing safety information and manual next steps
easier to understand; it does not make the console more capable and does not
validate the product. It is out of scope for the band to prove any of these.

## Test plan

Focused tests must prove:

- The orientation band exists.
- The band appears before the existing card grid.
- The band contains the one-line purpose.
- The band shows the four static posture chips (local-first,
  live-provider-disabled, non-executing/read-only, no API keys displayed).
- The posture chips are non-interactive: not buttons, links, forms, or toggles.
- The band includes an attention summary (both the derived and the safe-default
  paths).
- The band includes a next-manual-action line that happens outside the console.
- The band uses safe, non-readiness language: no "validated", "ready",
  "all clear", "passed", "healthy", "production readiness", "benchmark",
  "winner", or "superiority".
- Existing safety boundary strings remain present in the served HTML.
- Existing card ids remain present.
- The live-run button remains disabled.
- No new form is added except the existing receipt form.
- No new POST route is added except the existing receipt route.
- Status JSON shape is unchanged (no orientation field leaks into the payload).
- No raw prompt/output viewer, paste editor, queue, runner, scheduler, scoring,
  ranking, winner selection, or action control is introduced.
