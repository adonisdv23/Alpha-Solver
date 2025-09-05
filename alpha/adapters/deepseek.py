from .base import InstructionAdapter

class DeepseekAdapter(InstructionAdapter):
    family = "deepseek"

    def render_prompt(self, plan_step):
        return {
            "system": f"Deepseek system for {plan_step.get('tool_id')}",
            "user": plan_step.get("prompt", ""),
            "schema": {}
        }
