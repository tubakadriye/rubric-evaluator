import re

def parse_rubric(rubric_text):
    """
    Deterministic parsing of rubric into structured format.
    """

    criteria = []

    pattern = r"(.*?)(\d+)\s*points?"
    matches = re.findall(pattern, rubric_text, re.IGNORECASE)

    for m in matches:
        criteria.append({
            "name": m[0].strip(),
            "max_score": int(m[1]),
            "description": m[0].strip()
        })

    return {"criteria": criteria}