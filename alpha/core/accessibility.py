from __future__ import annotations
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from .loader import parse_yaml_lite


VOWELS = "aeiouy"


def count_syllables(word: str) -> int:
    word = word.lower()
    groups = re.findall(r"[aeiouy]+", word)
    return max(1, len(groups))


def flesch_reading_ease(text: str) -> float:
    sentences = max(1, len(re.findall(r"[.!?]", text)) or 1)
    words_list = re.findall(r"[a-zA-Z]+", text)
    words = max(1, len(words_list))
    syllables = sum(count_syllables(w) for w in words_list) or 1
    return 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)


def luminance(rgb: tuple[int, int, int]) -> float:
    def channel(c: int) -> float:
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def hex_to_rgb(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    return tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))


def contrast_ratio(fg: str, bg: str) -> float:
    l1 = luminance(hex_to_rgb(fg))
    l2 = luminance(hex_to_rgb(bg))
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


@dataclass
class AccessibilityConfig:
    readability_min: float = 60.0
    contrast_min: float = 4.5

    @classmethod
    def load(cls, path: str | Path = "config/accessibility.yaml") -> "AccessibilityConfig":
        p = Path(path)
        data: Dict[str, float] = {}
        if p.exists():
            data = parse_yaml_lite(p.read_text(encoding="utf-8")) or {}
        return cls(
            readability_min=float(data.get("readability_min", cls.readability_min)),
            contrast_min=float(data.get("contrast_min", cls.contrast_min)),
        )


class AccessibilityChecker:
    def __init__(self, config: AccessibilityConfig | None = None):
        self.config = config or AccessibilityConfig.load()

    @classmethod
    def from_config(cls) -> "AccessibilityChecker":
        return cls(AccessibilityConfig.load())

    def check_text(self, text: str) -> Dict[str, object]:
        score = flesch_reading_ease(text)
        return {"readability": score, "ok": score >= self.config.readability_min}

    def check_contrast(self, fg: str, bg: str) -> Dict[str, object]:
        ratio = contrast_ratio(fg, bg)
        return {"contrast": ratio, "ok": ratio >= self.config.contrast_min}
