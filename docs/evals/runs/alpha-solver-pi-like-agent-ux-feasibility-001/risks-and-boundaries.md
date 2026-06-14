# Risks and Boundaries

## Risk map

### Overfriendly tone weakening evidence boundaries

Risk: a friend-like tone could make uncertainty, blocked claims, or stop states feel optional.

Boundary: warmth must be subordinate to evidence. Responses should preserve citations, explicit uncertainty, and lane scope.

### Implied therapist or companion claims

Risk: Pi-like language can drift into emotional-support, therapy, or companion framing.

Boundary: Alpha Solver must not claim to provide therapy, mental-health support, companionship, emotional dependency, or personal relationship behavior.

### Hallucinated memory

Risk: conversational agents can imply continuity or memory not grounded in artifacts.

Boundary: memory summaries must be derived from explicit repository artifacts, current context, command output, or approved notes.

### Dependency on closed external products

Risk: direct reliance on a closed assistant product could create licensing, availability, privacy, and reproducibility risks.

Boundary: do not integrate Inflection Pi or similar services without exact operator-approved source links, API/license review, and a dedicated integration spec.

### Privacy issues if chats route outside Alpha Solver

Risk: operator chats may contain sensitive project, credential, planning, or private context.

Boundary: private local-first behavior is preferred. External routing requires explicit operator approval, data classification, redaction policy, and logging rules.

### Operator trust erosion if UX hides uncertainty

Risk: a polished conversational UX can make weak evidence appear stronger.

Boundary: the assistant must expose uncertainty, blocked evidence, and non-claims prominently.

## Hard boundaries preserved

- No direct Pi integration.
- No external service calls.
- No private user data use.
- No runtime code changes.
- No emotional-dependency or therapy claims.
- No weakened evidence-boundary language.
- No product-readiness claim.
