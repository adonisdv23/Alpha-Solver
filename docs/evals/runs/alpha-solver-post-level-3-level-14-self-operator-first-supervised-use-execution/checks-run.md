# Checks run (combined lane final checks)

Run on 2026-06-11 from the repo root on branch
`claude/eloquent-tesla-pmct3n` (created from `main` at `e04d4cc`), after the
supervised run and after every packet file was written.

```bash
git status --short
git diff --name-only
git diff --check
python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-packet
python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-packet-repair
python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-execution
python scripts/check_local_llm_packet_consistency.py   # full discovery
```

Results:

- Changed files versus `main` are exactly the allowed file list: the three
  repaired files of the merged first-use packet, the repair record packet,
  and this execution packet. No code, no tests, no other prior evidence
  packet, and no file outside the allowed list changed
  (`blocked_out_of_scope_change` did not trigger).
- `git diff --check`: no whitespace errors.
- Packet consistency: passed for each of the three directories
  individually, and for full discovery (128 packet directories scanned).
- Success criteria in `expected-artifacts.md` were met (see
  `execution-result.md`); the redaction review passed for every imported
  artifact (`redaction-record.md`).

## Forbidden-claim and unsafe-pattern scan

```bash
rg -n "production ready|runtime ready|provider ready|hosted ready|benchmark superior|benchmark validated|autonomous ready|autonomous|MVP ready|release ready|broad user ready|/v1/solve|deployment|billing|credential|secret|provider call|hosted model|git fetch|Path\(\"\$ROOT\"\)|<<'PY'" docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-packet docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-packet-repair docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-first-supervised-use-execution
```

83 hit lines in 30 files before this file was written; 85 in 31 files in
final state, because this `checks-run.md` itself quotes the scan command
and one reason text (its own row appears in the table below). Every hit
line was read in place and classified into exactly one of
`allowed_boundary_reference`, `forbidden_claim`,
`irrelevant_false_positive`, `safe_quoted_heredoc_environment_root`,
`unsafe_executable_plan_pattern`.

### First-use packet (38 hit lines, 11 files)

| File | Hits | Classification | Reason |
| --- | --- | --- | --- |
| `use-scope.md` | 9 | `allowed_boundary_reference` | The forbidden-surfaces list; every phrase appears only to forbid it. |
| `operator-confirmation-required.md` | 5 | `allowed_boundary_reference` | Quoted confirmation text that de-authorizes the listed surfaces. |
| `redaction-rules.md` | 4 | `allowed_boundary_reference` | Pre-import review items stating what must be absent. |
| `abort-conditions.md` | 4 | `allowed_boundary_reference` | Abort triggers naming forbidden values/patterns (2 original lines plus repaired condition 8 naming the removed network/expansion defects in order to forbid them). |
| `input-artifacts.md` | 3 | `allowed_boundary_reference` | Explicit input exclusions. |
| `evidence-boundary.md` | 3 | `allowed_boundary_reference` | Not-claims boundary statements. |
| `execution-command-plan.md` | 3 | 1 `safe_quoted_heredoc_environment_root` (line 30), 2 `allowed_boundary_reference` | Line 30 is the repaired executable step 2 block: ROOT passes through the shell environment before Python starts, Python reads `os.environ["ROOT"]`, the block contains no unexpanded-path use, and no shell expansion is needed inside the heredoc — all four conditions of the classification rule hold. The other two lines are prose stating the unexpanded pattern remains unsafe/blocked. |
| `use-target.md` | 2 | `allowed_boundary_reference` | Avoided-surfaces statement. |
| `source-evidence-reviewed.md` | 2 | 1 `irrelevant_false_positive`, 1 `allowed_boundary_reference` | Line 22's remote-fetch text is the packet-prep lane's historical prerequisite record from its own prior session — not executable first-use plan context; the other hit is a cited prep-packet file name. |
| `non-actions.md` | 2 | `allowed_boundary_reference` | Deliberate did-not statements. |
| `checks-plan.md` | 1 | `allowed_boundary_reference` | The quoted scan command itself. |

### Repair record packet (28 hit lines, 8 files)

| File | Hits | Classification | Reason |
| --- | --- | --- | --- |
| `repair-verification-before-execution.md` | 9 | `allowed_boundary_reference` | The quoted focused-scan command, its classification-table rows, and the conformance statement; all quote patterns in order to classify or forbid them. |
| `defects-repaired.md` | 7 | `allowed_boundary_reference` | Defect descriptions quoting the removed patterns and the repaired form. |
| `command-plan-before.md` | 5 | `allowed_boundary_reference` | The archived pre-repair plan, quoted verbatim as a defect record and explicitly marked defective and never executed; not executable command context. |
| `command-plan-after.md` | 3 | 1 `safe_quoted_heredoc_environment_root` (line 38), 2 `allowed_boundary_reference` | Verbatim copy of the repaired plan: its executable block is the same safe environment-handoff form; the other lines are the plan's own boundary prose. |
| `README.md` | 1 | `allowed_boundary_reference` | Defect summary naming the unexpanded pattern. |
| `checks-run.md` | 1 | `allowed_boundary_reference` | The quoted focused-scan command. |
| `evidence-boundary.md` | 1 | `allowed_boundary_reference` | Not-claims statement (readiness vocabulary quoted only to deny it). |
| `non-actions.md` | 1 | `allowed_boundary_reference` | Did-not statement. |

### Execution packet (19 hit lines, 12 files)

| File | Hits | Classification | Reason |
| --- | --- | --- | --- |
| `non-execution-proof.md` | 4 | `allowed_boundary_reference` | Per-surface non-execution proof rows; each names a surface to prove it was not touched. |
| `non-actions.md` | 3 | `allowed_boundary_reference` | Did-not statements. |
| `redaction-record.md` | 2 | `allowed_boundary_reference` | Review items stating what was confirmed absent. |
| `operator-confirmation-record.md` | 1 | `allowed_boundary_reference` | The verbatim recorded confirmation (de-authorization text). |
| `execution-scope.md` | 1 | `allowed_boundary_reference` | Descriptive reference to the repaired safe step 2 form. |
| `evidence-boundary.md` | 1 | `allowed_boundary_reference` | Not-claims statement. |
| `commands-run.md` | 1 | `safe_quoted_heredoc_environment_root` | Contemporaneous record of the executed step 2 command, which was exactly the safe environment-handoff form. |
| `imported-artifacts/checks/commands-run.txt` | 1 | `safe_quoted_heredoc_environment_root` | Same record, raw imported copy. |
| `imported-artifacts/inputs/approval-record.json` | 1 | `allowed_boundary_reference` | The recorded operator confirmation field (de-authorization text). |
| `imported-artifacts/execution-gate-result.json` | 1 | `allowed_boundary_reference` | The gate's own non-execution-boundary metadata string. |
| `imported-artifacts/checks/release-gate-check.json` | 1 | `allowed_boundary_reference` | The release-gate report's own boundary text ("does not run providers, hosted models, local models…"). |
| `checks-run.md` (this file) | 2 | `allowed_boundary_reference` | The quoted scan command itself and one classification reason quoting boundary text. |

### Totals and decision

Totals: `allowed_boundary_reference`: 80; `safe_quoted_heredoc_environment_root`: 4;
`irrelevant_false_positive`: 1; `forbidden_claim`: 0;
`unsafe_executable_plan_pattern`: 0.

Decision: **pass** — zero `forbidden_claim` and zero
`unsafe_executable_plan_pattern` classifications remain. No phrase appears
as an affirmative project status claim anywhere in the three packets, no
network-contacting command and no unexpanded-`$ROOT` heredoc remains in
executable command context, and the lane is not blocked.
