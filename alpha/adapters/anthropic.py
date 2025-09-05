from .base import InstructionAdapter

class AnthropicAdapter(InstructionAdapter):
    family = "anthropic"

    def render_prompt(self, plan_step):
        return {
            "system": f"Anthropic system for {plan_step.get('tool_id')}",
            "user": plan_step.get("prompt", ""),
            "schema": {}
        }
