from app.llm.client import call_llm
from app.utils.json_utils import extract_json
from app.config import MODEL_GRADING, TEMPERATURE_GRADING


def grade_answer(rubric, answer):

    prompt = f"""
You are a strict grader.

RUBRIC:
{rubric}

ANSWER:
{answer}

Return JSON:
{{
  "criteria_scores": [],
  "final_grade": number
}}
"""

    output = call_llm(prompt, MODEL_GRADING, TEMPERATURE_GRADING)
    return extract_json(output)