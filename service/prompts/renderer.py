"""Prompt deck renderer and helpers."""
from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List


def deck_sha(decks_yaml_text: str) -> str:
    """Return stable SHA256 hex digest for the given decks YAML text."""
    h = hashlib.sha256()
    h.update(decks_yaml_text.encode("utf-8"))
    return h.hexdigest()


def load_decks(path: str = "service/prompts/decks.yaml") -> Dict[str, Any]:
    """Load decks from a YAML file without external dependencies."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    sha = deck_sha(text)
    decks: Dict[str, Dict[str, str]] = {}
    current_deck: str | None = None
    current_key: str | None = None
    block_lines: List[str] = []
    collecting = False
    for line in text.splitlines():
        if not line.strip():
            continue
        if line.startswith("decks:"):
            continue
        if line.startswith("  ") and not line.startswith("    "):
            # New deck
            if collecting and current_deck and current_key:
                decks[current_deck][current_key] = "\n".join(block_lines).rstrip()
                collecting = False
                block_lines = []
            current_deck = line.strip().rstrip(":")
            decks[current_deck] = {}
        elif line.startswith("    ") and not line.startswith("      "):
            # key within deck
            if collecting and current_deck and current_key:
                decks[current_deck][current_key] = "\n".join(block_lines).rstrip()
                collecting = False
                block_lines = []
            key, rest = line.strip().split(":", 1)
            rest = rest.strip()
            if rest == "|":
                collecting = True
                current_key = key
                block_lines = []
            else:
                decks[current_deck][key] = rest
        else:
            if collecting and current_deck and current_key:
                block_lines.append(line[6:])
    if collecting and current_deck and current_key:
        decks[current_deck][current_key] = "\n".join(block_lines).rstrip()
    decks["_deck_sha"] = sha
    return decks


_TEMPLATE_RE = re.compile(r"{{\s*([a-zA-Z0-9_]+)(?:\|join\(\s*['\"]([^'\"]*)['\"]\s*\))?\s*}}");


def _render_template(template: str, ctx: Dict[str, Any]) -> str:
    def repl(match: re.Match) -> str:
        var = match.group(1)
        joiner = match.group(2)
        value = ctx.get(var, "")
        if joiner is not None:
            if isinstance(value, (list, tuple)):
                return joiner.join(str(x) for x in value)
            return str(value)
        return str(value)

    return _TEMPLATE_RE.sub(repl, template).strip()


def render(deck_name: str, ctx: Dict[str, Any], decks: Dict[str, Any]) -> Dict[str, str]:
    deck = decks[deck_name]
    system = _render_template(deck.get("system", ""), ctx)
    user = _render_template(deck.get("user_template", ""), ctx)
    return {"system": system, "user": user, "deck_sha": decks.get("_deck_sha", "")}


def to_route_explain(deck_name: str, deck_sha_str: str) -> Dict[str, str]:
    return {"prompt_deck": deck_name, "deck_sha": deck_sha_str}


def estimate_tokens(text: str) -> int:
    return len(text.split())


def compare_token_savings(baseline_prompts: List[str], new_prompts: List[str]) -> float:
    base = sum(estimate_tokens(p) for p in baseline_prompts)
    new = sum(estimate_tokens(p) for p in new_prompts)
    if base == 0:
        return 0.0
    return (base - new) / base * 100.0

