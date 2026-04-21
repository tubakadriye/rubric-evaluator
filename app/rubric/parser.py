import re


def parse_rubric(rubric_text):
    """
    Extract criteria with flexible patterns:
    supports: points, marks, score, pts
    """

    pattern = r"(.*?)(\d+)\s*(points?|marks?|score|pts?)"
    matches = re.findall(pattern, rubric_text, re.IGNORECASE)

    criteria = []

    for text, score, _ in matches:
        criteria.append({
            "name": text.strip(),
            "max_score": int(score),
            "description": text.strip()
        })

    return {"criteria": criteria}