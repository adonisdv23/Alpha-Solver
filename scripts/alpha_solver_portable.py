#!/usr/bin/env python3
"""Deterministic, offline reasoning helper.

This optional utility exposes two tiny reasoning strategies (ReAct-lite and
Chain-of-Thought-lite) that run without internet access or third‑party
packages.  The file is intentionally self‑contained and is not imported by the
project; running it has no effect on normal operation.  The goal is to give
chat-based systems a reproducible way to produce "better answers" while also
being honest about its limitations and suggesting specialised tools when
appropriate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import operator
import os
import random
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _stable_tiebreak(*vals: Any) -> float:
    """Return a deterministic float in [0,1) derived from *vals.*"""
    h = hashlib.sha256("|".join(map(str, vals)).encode("utf-8")).digest()
    return int.from_bytes(h[:8], "big") / 2**64


def load_context(args: argparse.Namespace) -> str:
    """Load context from --context-text or --context-file.

    If the file path exists its contents are read; otherwise the provided value
    is treated as literal context text.  Missing context yields an empty
    string.
    """

    if args.context_text:
        return args.context_text
    if args.context_file:
        if os.path.exists(args.context_file):
            return open(args.context_file, "r", encoding="utf-8").read()
        return args.context_file
    return ""


def chunk_context(ctx: str) -> List[str]:
    """Return non-empty paragraphs from *ctx* for pseudo-citations."""
    return [p.strip() for p in ctx.split("\n\n") if p.strip()]


def extract_assumptions(prompt: str, max_assumptions: int = 5) -> List[str]:
    """Naively split *prompt* into up to ``max_assumptions`` assumptions."""
    parts = re.split(r"[.?!]", prompt)
    return [p.strip() for p in parts if p.strip()][:max_assumptions]


def validate_assumptions(
    assumptions: List[str],
    context: str,
    max_citations: int = 3,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Validate assumptions against *context* using substring/token overlap."""

    context_lower = context.lower()
    context_tokens = set(re.findall(r"\w+", context_lower))
    chunks = chunk_context(context)
    validated: List[Dict[str, Any]] = []
    citations: List[Dict[str, Any]] = []

    offsets: List[int] = []
    pos = 0
    for ch in chunks:
        offsets.append(pos)
        pos += len(ch) + 2  # account for removed blank lines

    for assump in assumptions:
        a_low = assump.lower()
        found = False
        for ch, base in zip(chunks, offsets):
            ch_low = ch.lower()
            if a_low in ch_low:
                start = base + ch_low.index(a_low)
                end = start + len(a_low)
                citations.append({"span": [start, end], "quote": context[start:end][:80]})
                validated.append({"assumption": assump, "ok": True, "reason": "found"})
                found = True
                break
        if not found:
            a_tokens = set(re.findall(r"\w+", a_low))
            overlap = a_tokens & context_tokens
            if a_tokens and len(overlap) / len(a_tokens) > 0.5:
                token = sorted(overlap)[0]
                idx = context_lower.index(token)
                citations.append({"span": [idx, idx + len(token)], "quote": context[idx:idx+len(token)][:80]})
                validated.append({"assumption": assump, "ok": True, "reason": "overlap"})
            else:
                validated.append({"assumption": assump, "ok": False, "reason": "not_in_context"})
        if len(citations) >= max_citations:
            citations = citations[:max_citations]
            break
    return validated, citations


EXPR_RE = re.compile(r"(-?\d+)\s*([+\-*/])\s*(-?\d+)")
OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": lambda a, b: a // b if b else None,
}

# Keyword hints for specialised tools.  Mapping stays small so behaviour is
# deterministic and easy to audit.
TOOL_HINTS = {
    "image": "nano banana or another image tool",
    "picture": "nano banana or another image tool",
    "photo": "nano banana or another image tool",
    "video": "a dedicated video tool",
    "audio": "an audio editing tool",
    "diagram": "graphviz",
    "chart": "graphviz",
    "plot": "graphviz",
    "spreadsheet": "LibreOffice Calc",
    "excel": "LibreOffice Calc",
}


def tool_suggestion(prompt: str) -> Optional[str]:
    """Return a specialised tool hint if the prompt matches a keyword."""

    p = prompt.lower()
    for key, hint in TOOL_HINTS.items():
        if key in p:
            return hint
    return None


def simple_reasoner(prompt: str, context: str, rng: random.Random) -> str:
    """Return a deterministic answer.

    If *prompt* contains a small arithmetic expression it is evaluated.  Next,
    the first line of the context is used, falling back to a shuffled echo of
    the prompt for determinism.
    """

    match = EXPR_RE.search(prompt)
    if match:
        a, op, b = int(match.group(1)), match.group(2), int(match.group(3))
        func = OPERATORS.get(op)
        result = func(a, b) if func else None
        if result is not None:
            return str(result)
    ctx = context.strip().splitlines()
    if ctx:
        return ctx[0][:200]
    words = prompt.split()
    rng.shuffle(words)
    return " ".join(words)[:200]


def numeric_sanity(prompt: str, answer: str) -> Tuple[bool, str]:
    """Validate arithmetic expressions if present in *prompt* or *answer*."""

    match = EXPR_RE.search(prompt)
    if match and answer.strip().isdigit():
        a, op, b = int(match.group(1)), match.group(2), int(match.group(3))
        func = OPERATORS.get(op)
        if func is None:
            return True, "no_op"
        expected = func(a, b)
        if expected is None:
            return False, "div_by_zero"
        if int(answer.strip()) != expected:
            return False, f"expected {expected}"
        return True, "ok"
    m2 = re.search(r"(-?\d+)\s*([+\-*/])\s*(-?\d+)\s*=\s*(-?\d+)", answer)
    if m2:
        a, op, b, given = int(m2.group(1)), m2.group(2), int(m2.group(3)), int(m2.group(4))
        func = OPERATORS.get(op)
        if func is None:
            return True, "no_op"
        expected = func(a, b)
        if expected is None or given != expected:
            return False, f"expected {expected}"
    return True, "ok"


def apply_rules(final_answer: str, rules: Dict[str, Any]) -> Tuple[bool, str]:
    """Apply regex/shape rules supplied via --rules-json."""

    if not rules:
        return True, "no_rules"
    if "answer_shape" in rules:
        try:
            pattern = re.compile(rules["answer_shape"])
        except re.error as exc:
            return False, f"bad_regex: {exc}"
        if not pattern.search(final_answer or ""):
            return False, "shape_mismatch"
    return True, "ok"


def compute_confidence(
    validated: List[Dict[str, Any]],
    numeric_ok: bool,
    rules_ok: bool,
    seed: int,
    prompt: str,
) -> float:
    """Derive deterministic confidence score."""

    base = 0.7
    if numeric_ok and rules_ok and all(v["ok"] for v in validated):
        base += 0.1
    elif not numeric_ok or not rules_ok or any(not v["ok"] for v in validated):
        base -= 0.2
    jitter = _stable_tiebreak(seed, prompt) * 0.05
    return round(max(0.0, min(1.0, base + jitter)), 3)


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

def run_react(prompt: str, context: str, rng: random.Random) -> Tuple[str, List[Dict[str, Any]]]:
    """Run a three-step ReAct-lite reasoning loop."""

    trace: List[Dict[str, Any]] = []
    for step in range(1, 4):
        thought = f"step {step}: review"
        observation = "checked"
        trace.append({"step": step, "thought": thought, "action": "self-check", "observation": observation})
    final_answer = simple_reasoner(prompt, context, rng)
    return final_answer, trace


def run_cot(prompt: str, context: str, rng: random.Random) -> Tuple[str, List[Dict[str, Any]]]:
    """Run a tiny chain-of-thought sequence."""

    trace: List[Dict[str, Any]] = [
        {"step": 1, "thought": "analyse prompt"},
        {"step": 2, "thought": "consider context"},
        {"step": 3, "thought": "draft answer"},
    ]
    final_answer = simple_reasoner(prompt, context, rng)
    return final_answer, trace


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Deterministic offline solver")
    parser.add_argument("--strategy", choices={"react", "cot"}, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--context-text")
    parser.add_argument("--context-file")
    parser.add_argument("--rules-json")
    parser.add_argument("--human", action="store_true", help="print short summary")
    args = parser.parse_args(argv)

    rng = random.Random(args.seed)
    tool_hint = tool_suggestion(args.prompt)

    if tool_hint:
        output = {
            "strategy": args.strategy,
            "seed": args.seed,
            "final_answer": None,
            "confidence": 0.0,
            "assumptions": [],
            "validated": [],
            "trace": [],
            "citations": [],
            "safe_out": "better_tool_available",
            "reason": f"use {tool_hint}",
            "tool_hint": tool_hint,
        }
        print(json.dumps(output, separators=(",", ":")))
        if args.human:
            print(f"suggested tool: {tool_hint}", file=sys.stderr)
        return 0

    context = load_context(args)
    assumptions = extract_assumptions(args.prompt)
    validated, citations = validate_assumptions(assumptions, context)
    invalid_assumptions = [v["assumption"] for v in validated if not v["ok"]]

    if args.strategy == "react":
        final_answer, trace = run_react(args.prompt, context, rng)
    else:
        final_answer, trace = run_cot(args.prompt, context, rng)

    numeric_ok, numeric_reason = numeric_sanity(args.prompt, final_answer)

    rules: Dict[str, Any] = {}
    if args.rules_json:
        try:
            rules = json.loads(args.rules_json)
        except json.JSONDecodeError as exc:
            print(f"invalid rules-json: {exc}", file=sys.stderr)
            return 1
    rules_ok, rules_reason = apply_rules(final_answer, rules)

    confidence = compute_confidence(validated, numeric_ok, rules_ok, args.seed, args.prompt)
    penalty = min(0.3, 0.1 * len(invalid_assumptions))
    confidence = max(0.0, round(confidence - penalty, 3))

    need_clarify = (
        validated and (sum(1 for v in validated if v["ok"]) / len(validated) < 0.5)
    ) or confidence < 0.4

    clarify_text = None
    if need_clarify:
        if invalid_assumptions:
            clarify_text = f"Could you clarify '{invalid_assumptions[0]}'?"
        else:
            clarify_text = "Could you clarify your request?"

    output = {
        "strategy": args.strategy,
        "seed": args.seed,
        "final_answer": final_answer if numeric_ok and rules_ok and not need_clarify else None,
        "confidence": confidence if numeric_ok and rules_ok and not need_clarify else 0.0,
        "assumptions": assumptions,
        "validated": validated,
        "trace": trace,
        "citations": citations,
        "safe_out": None,
        "reason": "offline_mode",
    }

    if not numeric_ok or not rules_ok:
        output["safe_out"] = "halt_validation_failed"
        output["reason"] = numeric_reason if not numeric_ok else rules_reason
        print(json.dumps(output, separators=(",", ":")))
        if args.human:
            print(f"SAFE-OUT: {output['reason']}", file=sys.stderr)
        return 2

    if need_clarify:
        output["safe_out"] = "need_clarification"
        output["reason"] = "clarification_needed"
        print(json.dumps(output, separators=(",", ":")))
        if args.human:
            if clarify_text:
                print(f"clarify: {clarify_text}", file=sys.stderr)
            if invalid_assumptions:
                missing = ", ".join(invalid_assumptions[:2])
                print(f"needs context: {missing}", file=sys.stderr)
        return 0

    print(json.dumps(output, separators=(",", ":")))

    if args.human:
        summary = [
            f"answer: {final_answer}",
            f"confidence: {confidence}",
            f"validated: {sum(1 for v in validated if v['ok'])}/{len(validated)}",
        ]
        if citations:
            summary.append("cite: " + "; ".join(c["quote"] for c in citations[:2]))
        if invalid_assumptions:
            summary.append("needs context: " + ", ".join(invalid_assumptions[:2]))
        print(" | ".join(summary), file=sys.stderr)
    return 0


if __name__ == "__main__":  # pragma: no cover
    try:
        sys.exit(main())
    except Exception as exc:  # unexpected error
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
