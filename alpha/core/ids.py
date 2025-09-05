"""Utilities for tool id normalization and validation"""
import re

def slugify_tool_id(text: str) -> str:
    """Normalize a tool id.
    Lowercase and replace invalid characters with underscores.
    Collapse repeats and strip leading/trailing separators.
    """
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9._-]+", ".", text)
    text = text.replace("_.", ".").replace("._", ".")
    text = re.sub(r"[.]+", ".", text)
    text = text.strip(".")
    return text

_ID_RE = re.compile(r"^[a-z0-9]+(?:[._-][a-z0-9]+)*$")

def validate_tool_id(tool_id: str) -> str:
    """Validate a normalized tool id.
    Returns the id if valid, else raises ValueError.
    """
    if not _ID_RE.fullmatch(tool_id):
        raise ValueError(f"invalid tool id: {tool_id}")
    return tool_id
