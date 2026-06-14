# Residual Risks

- Candidate model families may be unavailable, too slow, or inconsistent on operator hardware.
- Local smoke can pass while routing quality remains poor.
- Synthetic routing tasks may be too easy and fail to represent real operator tasks.
- A model may produce plausible route explanations that are post-hoc rationalizations.
- Judge candidates may share biases with solver candidates.
- Safety reviewer candidates cannot establish safety validation without a stronger protocol and human review.
- Route labels may collapse multiple concerns, such as a coding task that is also a safety/boundary task.
- Operators may overread documentation-only matrices as behavior evidence.
- Future experiments could leak private data if task-bank controls are not enforced.
- Hardware or quantization differences may prevent reproducibility.
