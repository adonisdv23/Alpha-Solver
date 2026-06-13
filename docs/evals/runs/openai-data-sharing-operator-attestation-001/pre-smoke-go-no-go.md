# Pre-smoke go/no-go checklist

Before the next PR may run the first OpenAI call, all of the following must be true:

- [x] PR #502 merged.
- [x] PR #503 merged.
- [x] OpenAI data-sharing operator-verification packet merged.
- [ ] This operator-attestation packet merged.
- [ ] Operator has selected a dedicated or clearly bounded OpenAI project.
- [ ] Operator has manually verified data-sharing settings.
- [ ] Operator has manually verified billing readiness without committing private billing data.
- [ ] Operator has chosen a tiny synthetic prompt set.
- [ ] Redaction check is complete.
- [ ] The smoke lane has explicit cost and stop conditions.

This checklist is a precondition record only. It is not evidence of OpenAI validation, provider validation, API smoke success, token usage, eval execution, runtime readiness, or production readiness.
