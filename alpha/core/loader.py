"""Simple registry loader using standard library only"""
import json
from pathlib import Path

REGISTRY_CACHE = {}

FILES = {
    "sections": "sections.yaml",
    "questions": "questions.json",
    "risks": "risks.json",
    "playbooks": "templates.playbooks.yaml",
    "policy_routes": "policy.routes.yaml",
    "tools": "tools.json",
    "secrets_vault": "secrets_vault.json",
    "budget_controls": "budget_controls.yaml",
    "audit_trail": "audit_trail.json",
    "sla_contracts": "sla_contracts.yaml",
    "simulation_configs": "simulation_configs.json",
    "dependency_graph": "dependency_graph.yaml",
    "circuit_breakers": "circuit_breakers.json",
    "data_classification": "data_classification.yaml",
    "clusters": "clusters.yaml",
    "regions": "regions.yaml",
    "patents": "patents.yaml",
    "forecasts": "forecasts.json",
}


def parse_value(token: str):
    token = token.strip()
    if token.startswith('"') and token.endswith('"'):
        return token[1:-1]
    if token.startswith("'") and token.endswith("'"):
        return token[1:-1]
    if token.startswith('{') and token.endswith('}'):
        inner = token[1:-1].strip()
        if not inner:
            return {}
        pairs = [p.strip() for p in inner.split(',') if p.strip()]
        result = {}
        for pair in pairs:
            if ':' in pair:
                k, v = pair.split(':', 1)
                result[k.strip()] = parse_value(v)
        return result
    if token.startswith('[') and token.endswith(']'):
        inner = token[1:-1].strip()
        if not inner:
            return []
        if inner.startswith('{') and inner.endswith('}'):
            return [parse_value(inner)]
        return [parse_value(p.strip()) for p in inner.split(',')]
    if token.lower() == 'true':
        return True
    if token.lower() == 'false':
        return False
    if token.lower() == 'null':
        return None
    try:
        if '.' in token:
            return float(token)
        return int(token)
    except ValueError:
        return token


def parse_yaml_lite(text: str):
    """Parse a small subset of YAML used in registries"""
    text = text.strip()
    if text.startswith('{') and text.endswith('}'):
        return parse_value(text)
    lines = []
    for raw in text.splitlines():
        line = raw.split('#', 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(raw) - len(raw.lstrip(' '))
        lines.append((indent, line.strip()))

    def parse_block(index: int, indent: int):
        result = None
        is_list = None
        while index < len(lines):
            ind, content = lines[index]
            if ind < indent:
                break
            if content.startswith('- '):
                if is_list is False:
                    break
                is_list = True
                item = content[2:].strip()
                if index + 1 < len(lines) and lines[index + 1][0] > ind:
                    val, index = parse_block(index + 1, lines[index + 1][0])
                    if item:
                        base = parse_value(item)
                        if isinstance(base, dict) and isinstance(val, dict):
                            base.update(val)
                            val = base
                    result.append(val)
                else:
                    if result is None:
                        result = []
                        is_list = True
                    result.append(parse_value(item))
                    index += 1
            else:
                if is_list:
                    break
                if result is None:
                    result = {}
                    is_list = False
                if ':' in content:
                    key, rest = content.split(':', 1)
                    rest = rest.strip()
                    if rest == '':
                        val, index = parse_block(index + 1, ind + 2)
                    else:
                        val = parse_value(rest)
                        index += 1
                    result[key.strip()] = val
                else:
                    index += 1
        if result is None:
            result = [] if is_list else {}
        return result, index

    parsed, _ = parse_block(0, 0)
    return parsed if parsed is not None else {}


def load_file(path: Path):
    try:
        text = path.read_text(encoding='utf-8')
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            if path.suffix in ('.yaml', '.yml'):
                return parse_yaml_lite(text)
    except Exception:
        pass
    return {}


def load_all(path="registries"):
    base = Path(path)
    for key, fname in FILES.items():
        file_path = base / fname
        if file_path.exists():
            REGISTRY_CACHE[key] = load_file(file_path)
        else:
            REGISTRY_CACHE[key] = {}
    return REGISTRY_CACHE
