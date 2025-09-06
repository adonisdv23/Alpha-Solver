"""Deterministic prompt templates for local adapters."""
from __future__ import annotations

from typing import List


def summarize(text: str) -> str:
    return f"Summarize the following text:\n{text}\nSummary:"


def extract(text: str, keyword: str) -> str:
    return f"Extract '{keyword}' from the text:\n{text}\nExtract:"


def classify(text: str, labels: List[str]) -> str:
    opts = ", ".join(labels)
    return f"Classify the text into one of [{opts}]:\n{text}\nLabel:"


TEMPLATES = {
    "summarize": summarize,
    "extract": extract,
    "classify": classify,
}
