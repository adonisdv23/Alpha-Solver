# ALPHA-SOLVER-NARRATIVE-CLAIM-SAFETY-LINTER-001 · Narrative Claim-Safety Linter

## Purpose

Add an offline, deterministic narrative claim-safety linter for docs packets and
narrative artifacts. The linter catches high-risk unsupported wording before a
founder memo, demo recap, evidence packet, or other shareable narrative turns a
limited artifact into an overbroad claim.

## Scope

- Define forbidden claim families for readiness, validation, benchmark,
  superiority, provider, public exposure, and security/privacy claims.
- Provide bounded alternative wording for each family in checker findings.
- Require explicit suppression rationale when a risky phrase must be retained as
  quoted text, a negative fixture, or another reviewed exception.
- Test the checker with synthetic founder-style memo and demo-style artifacts.
- Preserve evidence boundaries and residual risks.

## Non-goals

- Do not rewrite prior evidence.
- Do not delete evidence packets.
- Do not claim linter completeness.
- Do not call providers.
- Do not update Google Sheets.
- Do not validate behavior, benchmarks, security, privacy, readiness, public
  exposure, or provider operation.

## Forbidden claim families and bounded alternatives

| Family | Forbidden unsupported claim shape | Allowed bounded alternative |
| --- | --- | --- |
| Readiness | MVP, production, pilot, release, customer, runtime, or public readiness stated as achieved/proven. | State the artifact is operator-review-ready or records a limited local/supervised check, with remaining blockers. |
| Validation | MVP/product/system/solver/readiness stated as validated, proven, certified, or confirmed. | Say the check produced bounded evidence for the named fixture/run and list non-claims. |
| Benchmark | Benchmark proof, statistically significant, SOTA, best-in-class, or benchmark win claims. | Describe the exact sample, prompt set, and metric as exploratory or fixture-bound rather than benchmark proof. |
| Superiority | Alpha Solver broadly better/superior/smarter/more reliable than providers/models/competitors. | Use comparison-specific wording such as: in this limited fixture, reviewer X preferred output Y for criterion Z. |
| Provider | Provider approval/validation or provider reasoning orchestration readiness/proof without direct evidence. | State provider behavior only when directly evidenced; otherwise say provider-backed execution was not run or remains out of scope. |
| Public exposure | Public endpoint/public accessibility/safe for public use or sharing without exposure review. | Say whether an artifact is local, private, authenticated, or not assessed for public exposure. |
| Security/privacy | Secure, privacy validated, PII-safe, secret-safe, cannot leak, fully redacted, or zero-risk claims. | Use bounded wording such as: static checks found no known test secret fixture leaks; security/privacy review remains incomplete. |

## Suppression policy

Suppressions must be local to the line and must include an explicit rationale:

```md
<!-- claim-safety-ignore: rationale=quoted external wording retained for negative fixture -->
```

Bare suppressions are invalid. Suppressions are intended for quoted external
wording, synthetic negative fixtures, or reviewed exceptions, not for avoiding
claim-boundary work.

## Evidence packet

- Checker: `scripts/check_narrative_claim_safety.py`.
- Focused tests: `tests/test_narrative_claim_safety.py`.
- Synthetic founder-style fixture coverage: unsupported readiness, validation,
  superiority, and security/privacy claims.
- Synthetic demo-style fixture coverage: unsupported benchmark, provider, and
  public exposure claims.
- Validation command: `python -m pytest tests/test_narrative_claim_safety.py -q`.
- Whitespace validation: `git diff --check`.

## Residual risks

- Static phrase matching is incomplete and can miss paraphrases, sarcasm,
  tables, images, screenshots, and context split across sections.
- Some true claims may still need human evidence review even when the checker
  passes.
- Some allowed boundary contexts may hide a real issue if the surrounding prose
  is ambiguous.
- Suppression rationale quality is checked only structurally, not semantically.
- The checker does not inspect Google Sheets, provider systems, live endpoints,
  private documents, or binary artifacts.

## Acceptance criteria

- The linter exposes forbidden claim families and bounded alternatives.
- Founder-style and demo-style synthetic fixtures are covered by tests.
- Findings include family, line, matched snippet, understandable message, and a
  bounded alternative.
- Suppressions without explicit rationale fail.
- Validation runs do not call providers.
