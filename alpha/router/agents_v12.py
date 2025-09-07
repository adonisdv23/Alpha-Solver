from __future__ import annotations

"""Scaffold for future multi-agent router (v12)."""

from typing import Callable, Dict


def decomposer(text: str) -> str:
    """Return ``text`` unchanged (placeholder)."""
    return text


def checker(text: str) -> str:
    """Return ``text`` unchanged (placeholder)."""
    return text


def calculator(text: str) -> str:
    """Return ``text`` unchanged (placeholder)."""
    return text


AGENTS_V12: Dict[str, Callable[[str], str]] = {
    "decomposer": decomposer,
    "checker": checker,
    "calculator": calculator,
}

