from .base import InstructionAdapter

class OpenAIAdapter(InstructionAdapter):
    family = "openai"

    def render_prompt(self, plan_step):
        return {
            "system": f"OpenAI system for {plan_step.get('tool_id')}",
            "user": plan_step.get("prompt", ""),
            "schema": {}
        }
