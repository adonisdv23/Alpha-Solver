"""Instruction adapter base class"""
from __future__ import annotations
from typing import Dict

class InstructionAdapter:
    family: str = "base"

    def render_prompt(self, plan_step: Dict) -> Dict[str, object]:
        raise NotImplementedError
