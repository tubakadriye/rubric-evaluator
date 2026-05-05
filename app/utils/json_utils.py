import json
import re


# def extract_json(text):
#     match = re.search(r"\{.*\}", text, re.DOTALL)

#     if not match:
#         raise ValueError(f"Invalid JSON output: {text[:200]}")

#     try:
#         return json.loads(match.group())
#     except Exception as e:
#         raise ValueError(f"JSON parse error: {e} | Raw: {text[:200]}")
    

def extract_json(text):
    try:
        return json.loads(text)
    except:
        pass

    matches = re.findall(r"\{.*?\}", text, re.DOTALL)

    for m in matches:
        try:
            return json.loads(m)
        except:
            continue

    raise ValueError(f"JSON parse failed: {text[:300]}")