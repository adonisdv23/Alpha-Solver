from .base import InstructionAdapter

class GeminiAdapter(InstructionAdapter):
    family = "gemini"

    def render_prompt(self, plan_step):
        return {
            "system": f"Gemini system for {plan_step.get('tool_id')}",
            "user": plan_step.get("prompt", ""),
            "schema": {}
        }
