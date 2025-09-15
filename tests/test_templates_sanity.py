import yaml
from service.clarify import render

EXPECTED_INTENTS = {"summarize", "extract", "rewrite", "plan", "codegen", "classify", "cite", "web_extract"}


def _sample_context(variables):
    ctx = {}
    for name, meta in variables.items():
        default = meta.get("default", "sample")
        if isinstance(default, list):
            ctx[name] = default or ["x"]
        else:
            ctx[name] = default or "sample"
    return ctx


def test_template_deck_sanity():
    with open("service/clarify/templates.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    templates = data["templates"]
    intents = {t["intent"] for t in templates if t["intent"] != "clarify"}
    assert EXPECTED_INTENTS.issubset(intents)
    for tpl in templates:
        user = tpl.get("user", "")
        system = tpl.get("system", "")
        vars_meta = tpl.get("variables", {})
        ctx = _sample_context(vars_meta)
        rendered = render.render(tpl["id"], ctx, {tpl["id"]: user})
        assert "{{" not in rendered
        assert rendered.count("\n") < 25
        for line in rendered.splitlines():
            assert not line.strip().isupper()
        assert "SECRET" not in rendered
        assert rendered == render.render(tpl["id"], ctx, {tpl["id"]: user})
        assert system.count("\n") < 25
        for line in system.splitlines():
            assert not line.strip().isupper()
