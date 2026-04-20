from app.llm import call_llm_text
from app.utils import extract_json

def generate_synthetic_answers(teaching, rubric):
    """
    Generates calibration dataset:
    - good answers
    - bad answers
    - edge cases
    """

    prompt = f"""
You are generating synthetic student answers for rubric evaluation.

TEACHING MATERIAL:
{teaching}

RUBRIC:
{rubric}

Generate:

1. 4 HIGH-QUALITY answers (full understanding)
2. 4 LOW-QUALITY answers (misunderstanding / missing parts)
3. 3 EDGE CASE answers (partially correct but ambiguous)

Return STRICT JSON:

{{
  "good": ["..."],
  "bad": ["..."],
  "edge": ["..."]
}}
"""

    return extract_json(call_llm_text(prompt))