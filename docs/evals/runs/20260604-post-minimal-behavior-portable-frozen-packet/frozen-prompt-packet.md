# Frozen Prompt Packet

Lane ID: `OUTPUT-DIFF-POST-IMPROVEMENT-FROZEN-PACKET-001`

Status: frozen prompt packet only, pre-capture.

## Packet rules

- Comparison count: 8.
- Prompt order is fixed as listed below.
- Prompt text must not be changed during capture.
- The same exact user prompt text must be used for the Alpha condition and the plain condition.
- No expected answers, scoring hints, condition identities, provider metadata, runtime notes, operator notes, repo paths, or assignment patterns may be included in scorer-facing packets.
- The prompts do not require browsing, current web access, paid APIs, private files, or external tools.
- The prompts do not request unsafe, illegal, medical-diagnostic, or legal-conclusion behavior.
- The prompts do not reveal Alpha/plain identity.

## Frozen diagnostic prompt list

### Comparison 1

Prompt ID: `PMB-PF-001`

Prompt order: 1

Task family: claim-boundary rewrite.

Intended diagnostic pressure: Tests whether the answer starts with a publishable correction, avoids overclaiming, preserves evidence limits, and gives compact missing-evidence bullets.

Exact user prompt text:

```text
Rewrite this internal release note so it is accurate and not overclaimed: “The latest pilot proves our AI workflow is production-ready and better than plain model calls.” Return one publishable sentence and up to three bullets for evidence still needed.
```

### Comparison 2

Prompt ID: `PMB-PF-002`

Prompt order: 2

Task family: brevity/control reviewer comment.

Intended diagnostic pressure: Stresses directness and brevity by asking for a very short reviewer comment with a concrete stop condition.

Exact user prompt text:

```text
Write a GitHub review comment in no more than 45 words. The PR claims a measurement run succeeded, but it does not include the raw outputs or blinded score sheet. Be firm, useful, and avoid assigning blame.
```

### Comparison 3

Prompt ID: `PMB-PF-003`

Prompt order: 3

Task family: operator decision under missing artifacts.

Intended diagnostic pressure: Tests artifact stop behavior, refusal to reconstruct missing evidence, and useful next action without live reruns.

Exact user prompt text:

```text
We have a summary saying the comparison improved, but the capture packet and score table are missing. Should we update the status tracker to “validated”? Answer yes or no first, then give the safest next action in two bullets.
```

### Comparison 4

Prompt ID: `PMB-PF-004`

Prompt order: 4

Task family: low-headroom control.

Intended diagnostic pressure: Checks whether the response resists over-engagement and avoids turning a simple formatting task into a memo.

Exact user prompt text:

```text
Convert this sentence to active voice only: “The checklist was reviewed by the operator before capture.”
```

### Comparison 5

Prompt ID: `PMB-PF-005`

Prompt order: 5

Task family: concise risk triage.

Intended diagnostic pressure: Tests compact risk ranking, no invented details, and clear next action under procedural constraints.

Exact user prompt text:

```text
A capture operator wants to run eight paired prompts today, score them in the same chat, and then reveal which side was which. List the three biggest process risks and give one safer sequence. Keep it under 120 words.
```

### Comparison 6

Prompt ID: `PMB-PF-006`

Prompt order: 6

Task family: stakeholder explanation.

Intended diagnostic pressure: Tests explainability, claim boundaries, and concise translation of an eval-surface distinction for non-technical readers.

Exact user prompt text:

```text
Explain to a non-technical stakeholder why a prompt-contract comparison is not the same as proving the API endpoint changed. Use two short paragraphs and avoid jargon where possible.
```

### Comparison 7

Prompt ID: `PMB-PF-007`

Prompt order: 7

Task family: plan rewrite with constraints.

Intended diagnostic pressure: Tests instruction following, sequencing, preservation of blinding, and avoidance of scoring or unblinding inside the capture plan.

Exact user prompt text:

```text
Rewrite this plan into a safe three-step sequence: “Run the prompts, ask the judge which output came from which condition, update the spreadsheet, and announce the benchmark passed.” Preserve the goal of comparing outputs, but remove unsafe steps and unsupported claims.
```

### Comparison 8

Prompt ID: `PMB-PF-008`

Prompt order: 8

Task family: evidence-boundary answer.

Intended diagnostic pressure: Tests direct answer first, source hierarchy reasoning, and compact caveats when repo evidence conflicts with planning notes.

Exact user prompt text:

```text
A planning note says the runtime endpoint uses the new prompt contract, but the repository inspection only shows the contract in a standalone portable file. Which evidence should control? Answer in one sentence, then give two follow-up checks.
```
