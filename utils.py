import json

def try_parse_json(text: str):
    try:
        return json.loads(text), text
    except Exception:
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end != -1:
            try:
                snippet = text[start:end+1]
                return json.loads(snippet), text
            except Exception:
                pass
        return None, text