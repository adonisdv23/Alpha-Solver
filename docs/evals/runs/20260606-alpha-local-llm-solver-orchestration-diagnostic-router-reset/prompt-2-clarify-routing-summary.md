# Prompt 2 Clarify Routing Summary

Prompt shape `underspecified_edit_or_performance` covers the retry 006 Prompt 2 style, including `Make it faster.`.

When Pass 1 is parseable and boundary-clean, and neither the user prompt nor Pass 1 fields contain explicit serious-risk terms, this prompt shape routes to `clarify` without Pass 2. Model-produced considerations and assumptions are not exposed. Vague risk labels such as information risk, unknown risk, medium risk, ambiguous request, insufficient context, or unclear requirements do not force a block for this shape.

If explicit serious-risk terms appear, the runner blocks with `answer`, `final_answer`, `considerations`, and `assumptions` empty.
