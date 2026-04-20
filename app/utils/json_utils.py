import json
import re

def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return {"error": "invalid_json", "raw": text}
    try:
        return json.loads(match.group())
    except:
        return {"error": "parse_error", "raw": text}