from alpha.adapters import openai, anthropic, gemini, deepseek


def test_adapter_prompts():
    step = {"tool_id": "t", "prompt": "hi"}
    assert "OpenAI" in openai.OpenAIAdapter().render_prompt(step)["system"]
    assert "Anthropic" in anthropic.AnthropicAdapter().render_prompt(step)["system"]
    assert "Gemini" in gemini.GeminiAdapter().render_prompt(step)["system"]
    assert "Deepseek" in deepseek.DeepseekAdapter().render_prompt(step)["system"]
