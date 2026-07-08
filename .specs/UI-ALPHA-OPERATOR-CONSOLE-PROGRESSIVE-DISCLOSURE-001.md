# UI-ALPHA-OPERATOR-CONSOLE-PROGRESSIVE-DISCLOSURE-001 · Operator Console Progressive Disclosure

Lane id: `AOC-B009-OPERATOR-CONSOLE-PROGRESSIVE-DISCLOSURE-001`

## Goal

Reduce first-glance visual overwhelm on `/dashboard/operator-console` by moving
long, repeated boundary-note lists and reference-heavy blocks behind
closed-by-default native HTML `<details>` / `<summary>` elements.

This lane changes default visibility only. It does not remove boundary text and
does not add execution capability.

## Motivation

A daily operator opened the protected Operator Console in a local preview and
reported that the local-first and live-provider-disabled signals were clear, but
that there was "too much text" and "too much everything. no ux." The console's
safety boundaries are correct; the problem is that every long boundary list and
reference block renders fully expanded at once, so the operator cannot scan the
page. Progressive disclosure keeps all the safety information present while
collapsing the repeated detail so the page becomes scannable.

## Scope

- Add a small `_details(summary, body)` render helper that emits a
  closed-by-default native `<details class="disclosure"><summary>…</summary>…`
  element. No `open` attribute, no JavaScript, no frontend dependency.
- Wrap the following long, repeated boundary/reference blocks in that helper,
  keeping each card's title and a one-line boundary summary visible:
  - Dry-Run Preview: "would use" list and the long safety-boundary list.
  - Provider and Cost Gate: cap/key presence detail tables and the long
    safety-boundary list.
  - Preflight and Capture Entry: the terminal workflow command snippets.
  - Manual Next Step Guide: the boundary-reminder list.
  - ChatGPT Copy/Paste Capture: would-use, checklist/template, terminal
    snippets, route-metadata guidance, unsafe-actions list, and the long
    safety-boundary list.
  - Local Receipt Store: the receipt-boundary list.
  - Evidence and Receipt: the local-artifact boundary list and the freshness /
    sequence-coherence detail.
- Add minimal CSS for the disclosure summary affordance.
- Keep the primary header, mode banner, disabled live-run control, and card
  titles fully visible (never collapsed).

## Non-goals

- No action queue, task queue, job queue, processor, workbench, runner,
  scheduler, worker, dispatch, approval, retry, or action-control behavior.
- No provider execution, ChatGPT API integration, browser automation,
  `/v1/solve` invocation, dry-run execution, or CLI/subprocess/shell execution
  from the console.
- No paste storage, capture editor, raw prompt viewer, or raw output viewer.
- No new POST route, new write path, new status payload field, or new card id.
- No page-wide layout redesign and no card reordering.
- No JavaScript accordion or tab framework and no new frontend dependency.
- No readiness, validation, benchmark, production, scoring, ranking, winner, or
  superiority claim.
- No removal, weakening, paraphrase, or badge-replacement of existing boundary
  text.

## Allowed files

- `alpha/webapp/routes/operator_console.py`
- `tests/test_operator_console.py`
- `docs/OPERATOR_CONSOLE.md`
- `.specs/UI-ALPHA-OPERATOR-CONSOLE-PROGRESSIVE-DISCLOSURE-001.md`
- `.specs/INDEX.md`

## Implementation notes

- Progressive disclosure is native only: `<details>` / `<summary>` with no
  `open` attribute renders collapsed by default in the browser and requires no
  script.
- Because the collapsed body remains in the served HTML, every existing
  substring-based safety test continues to pass unchanged; collapse means less
  visible by default, not removed.
- The status JSON assembled by `build_console_status` is untouched: this is a
  render-layer change in `_render_page` only.
- Card ids, the disabled live-run control, and the single existing receipt form
  are preserved exactly.

## Definition of done

- The page renders long boundary/reference blocks inside closed-by-default
  native `<details>` / `<summary>` elements.
- The mode banner, `Local-first operator console`, `Live provider calls are
  disabled in this MVP`, `No API keys are displayed`, the claim boundary, the
  disabled live-run control, and every card title remain visible without
  expanding anything.
- All existing boundary text remains present in the served HTML.
- All existing card ids remain present.
- Status JSON shape is unchanged.
- Focused and broad Operator Console tests pass.
- Documentation notes that detailed boundary reminders may be collapsed on the
  page but remain available through expandable details.

## Boundary checklist

- [x] Render-only default-visibility change.
- [x] Native `<details>` / `<summary>` only.
- [x] Details closed by default (no `open` attribute).
- [x] No JavaScript and no new frontend dependency.
- [x] No boundary text removed, weakened, or paraphrased.
- [x] First-glance safety signals remain visible.
- [x] No provider calls.
- [x] No ChatGPT calls.
- [x] No `/v1/solve` calls.
- [x] No browser automation.
- [x] No CLI, shell, or subprocess execution.
- [x] No prompt submission.
- [x] No paste storage or capture editor.
- [x] No raw prompt/output viewer.
- [x] No new POST route.
- [x] No new write path.
- [x] No new status payload field.
- [x] No new or renamed card id.
- [x] Local Receipt Store remains the only controlled write path.

## Non-claims

The lane does not claim readiness, validation success, benchmark validity,
production readiness, scoring, ranking, winner selection, model superiority,
provider readiness, billing accuracy, or answer quality. It is a presentation
change that makes existing safety information easier to scan; it does not make
the console more capable and does not validate the product.

## Test plan

Focused tests must prove:

- The page includes native `<details>` and `<summary>` elements for the long
  boundary/reference sections.
- The new details elements are closed by default (no `open` attribute) and no
  JavaScript accordion/tab framework is introduced.
- The primary mode/safety banner text stays visible outside any details.
- All existing safety boundary strings remain present in the served HTML.
- All existing card ids remain present.
- The live-run button remains disabled.
- No new form is added except the existing receipt form.
- No new POST route is added except the existing receipt route.
- No raw prompt/output viewer or paste editor is introduced.
- No queue, runner, scheduler, scoring, ranking, winner, readiness, validation,
  benchmark, production, or superiority claim is introduced.
- The status JSON shape is unchanged.
