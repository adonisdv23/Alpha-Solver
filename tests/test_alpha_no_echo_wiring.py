from alpha_solver_entry import _tree_of_thought


PROMPTS = [
    "Explain photosynthesis in two plain-language sentences.",
    "Give a three-item checklist for packing for a one-night work trip.",
    "Help me choose a database for my app; I have not decided traffic, budget, or data model.",
    'Summarize the main claims of the 2025 paper "Quantum Bananas Cure Insomnia" without inventing facts.',
]


def _normalized(text: str) -> str:
    return " ".join(text.strip().lower().split())


def test_local_alpha_entrypoint_replaces_exact_prompt_echo_with_derived_answer():
    for prompt in PROMPTS:
        result = _tree_of_thought(prompt, seed=42, cache_path=None, enable_cache=False)

        assert _normalized(result["solution"]) != _normalized(prompt)
        assert _normalized(result["final_answer"]) != _normalized(prompt)
        assert result["solution"] == result["final_answer"]
        assert len(result["final_answer"].split()) >= 8
        assert result["reason"] == "prompt_echo_replaced_with_local_derived_answer"
        assert result["diagnostics"]["tot"]["echo_detected"] is True
        assert result["diagnostics"]["tot"]["raw_echo_answer"] == prompt


def test_unsupported_exact_echo_gets_safeout_instead_of_generic_canned_answer():
    prompt = "What is 2 + 2?"
    result = _tree_of_thought(prompt, seed=42, cache_path=None, enable_cache=False)

    assert _normalized(result["solution"]) != _normalized(prompt)
    assert _normalized(result["final_answer"]) != _normalized(prompt)
    assert "local deterministic answer: break the request" not in result["final_answer"].lower()
    assert result["final_answer"].startswith("SAFE-OUT:")
    assert "could not derive a substantive answer" in result["final_answer"]
    assert "supported context" in result["final_answer"]
    assert result["reason"] == "prompt_echo_replaced_with_unsupported_local_safeout"
    assert result["solution"] == result["final_answer"]
    assert result["diagnostics"]["tot"]["echo_detected"] is True
    assert result["diagnostics"]["tot"]["raw_echo_answer"] == prompt
    assert "prompt_echo_replaced_unsupported_local_safeout_no_provider" in result["evidence"]


def test_local_alpha_entrypoint_uses_substantive_fixture_shapes():
    photosynthesis = _tree_of_thought(PROMPTS[0], seed=42, cache_path=None, enable_cache=False)
    checklist = _tree_of_thought(PROMPTS[1], seed=42, cache_path=None, enable_cache=False)
    ambiguous = _tree_of_thought(PROMPTS[2], seed=42, cache_path=None, enable_cache=False)
    false_premise = _tree_of_thought(PROMPTS[3], seed=42, cache_path=None, enable_cache=False)

    assert "sunlight" in photosynthesis["final_answer"].lower()
    assert "1." in checklist["final_answer"] and "3." in checklist["final_answer"]
    assert "clarifying" in ambiguous["final_answer"].lower() or "clarify" in ambiguous["final_answer"].lower()
    assert "cannot substantiate" in false_premise["final_answer"].lower()
