# Boundary and Risk Preservation

Preserved behavior:

- Pass 1 forbidden boundary claims fail closed before Pass 2.
- Pass 2 forbidden boundary claims fail closed before answer exposure.
- Safety and boundary failed-closed outputs suppress `answer`, `final_answer`, `considerations`, and `assumptions`.
- Explicit high-risk prompt terms or Pass 1 field terms block even for known prompt shapes.
- Generic unknown prompt shapes preserve conservative unknown/non-allowlisted risk behavior.
- Negated disclaimers such as “This does not prove production readiness” remain allowed when otherwise bounded.
