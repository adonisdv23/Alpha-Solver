# Sanitization Log

Lane ID: `OUTPUT-DIFF-POST-IMPROVEMENT-PORTABLE-CAPTURE-001`

Status: operator-only sanitization record. This file is not scorer-facing.

## Sanitization rules applied

- Raw outputs remain exact and separate in `raw-outputs/`.
- The scorer-facing packet was built as a separate sanitized artifact.
- Direct brand, provider, route, condition, heading, footer, and envelope tells were removed or neutralized in the scorer-facing packet.
- Pipeline-confirmation branding was removed from scorer-facing material.
- Substantive answer content, caveats, reasoning, risks, assumptions, recommendations, omissions, verbosity, contradictions, and answer-quality defects were preserved.
- Sanitization was applied symmetrically: both outputs were rendered under neutral Output A / Output B labels with no source labels.
- The operator-only assignment map was kept out of the scorer-facing packet.

## Per-comparison notes

| Comparison ID | Prompt ID | Sanitization notes |
| --- | --- | --- |
| comparison-001 | PMB-PF-001 | Removed envelope headings, route label, expert-team heading, safe-out heading, shortlist heading, confidence label, and pipeline footer from one source output. Preserved the publishable sentence, evidence bullets, caveat that a pilot does not prove readiness, and additional claim-boundary considerations as neutral text. No provider tells were present. |
| comparison-002 | PMB-PF-002 | Removed envelope headings, route label, expert-team heading, safe-out heading, shortlist heading, confidence label, and pipeline footer from one source output. Preserved the reviewer comment and non-blaming artifact stop rationale. No provider tells were present. |
| comparison-003 | PMB-PF-003 | Removed envelope headings, route label, expert-team heading, safe-out heading, shortlist heading, confidence label, and pipeline footer from one source output. Preserved the `Stop: No.` opening, missing-artifact rationale, and no-reconstruction/no-status-update guidance. No provider tells were present. |
| comparison-004 | PMB-PF-004 | Removed envelope headings, route label, expert-team heading, safe-out heading, shortlist heading, confidence label, and pipeline footer from one source output. Preserved the active-voice conversion and noted the extra preserved considerations neutrally. No provider tells were present. |
| comparison-005 | PMB-PF-005 | Removed envelope headings, route label, expert-team heading, safe-out heading, shortlist heading, confidence label, and pipeline footer from one source output. Preserved the three risks, safer sequence, and process-separation caveats. No provider tells were present. |
| comparison-006 | PMB-PF-006 | Removed envelope headings, route label, expert-team heading, safe-out heading, shortlist heading, confidence label, and pipeline footer from one source output. Preserved the two-paragraph endpoint distinction and endpoint-evidence caveat. No provider tells were present. |
| comparison-007 | PMB-PF-007 | Removed envelope headings, route label, expert-team heading, safe-out heading, shortlist heading, confidence label, and pipeline footer from one source output. Preserved the three-step sequence and separation of capture, scoring, and unblinding. No provider tells were present. |
| comparison-008 | PMB-PF-008 | Removed envelope headings, route label, expert-team heading, safe-out heading, shortlist heading, confidence label, and pipeline footer from one source output. Preserved the evidence hierarchy answer and follow-up checks. No provider tells were present. |

## Sanitization failures or stop conditions

No sanitization failures were observed. No direct tells required substantive rewriting to remove. No stop condition was triggered.
