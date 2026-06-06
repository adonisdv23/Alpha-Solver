# Spec Preservation Checklist

- [x] Canonical spec added at `.specs/LOCAL-LLM-SOLVER-ORCHESTRATION-001.md`.
- [x] `.specs/INDEX.md` updated with `LOCAL-LLM-SOLVER-ORCHESTRATION-001.md`.
- [x] Existing local runtime path described as closed and bounded to runtime smoke evidence only.
- [x] Next goal stated as orchestration wiring, not more prompt engineering.
- [x] Safety invariants preserved: default-off, opt-in, localhost/loopback only, no provider keys, finite timeout, no hosted fallback, `behavior_evidence=false`.
- [x] Production `/v1/solve` exposure remains blocked.
- [x] Dashboard exposure remains blocked.
- [x] Provider fallback remains blocked.
- [x] Evidence-model promotion remains blocked.
- [x] Model-quality, MVP, production, benchmark, and superiority claims remain blocked.
- [x] First implementation target selected as a non-production local orchestration runner.
- [x] Expert two-pass selected as the first quality-lift feature.
- [x] Local ToT-lite recorded as a later feature.
- [x] ReAct-lite and CoT self-validation recorded as later optional deterministic strategy surfaces.
- [x] Built code surfaces distinguished from approved runtime integration surfaces.
- [x] `alpha_solver_v225_p2_experts.py` stated as inactive unless separately approved as non-stub.
- [x] Exactly one selected next lane recorded.
