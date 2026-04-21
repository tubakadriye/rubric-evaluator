import json
import re


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError(f"Invalid JSON output: {text[:200]}")

    try:
        return json.loads(match.group())
    except Exception as e:
        raise ValueError(f"JSON parse error: {e} | Raw: {text[:200]}")