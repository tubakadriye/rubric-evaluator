from app.llm import call_llm


def grade_student_answer(rubric, answer):
    prompt = f"""
You are a strict and consistent grader.

IMPORTANT:
- Output MUST be valid JSON
- You MUST use ONLY the rubric below
- Do NOT introduce external knowledge
- If the rubric is unclear, explicitly say so

RUBRIC:
{rubric}

STUDENT ANSWER:
{answer}

TASK:
1. Extract ALL criteria from the rubric
2. Evaluate each criterion separately
3. Assign score strictly within defined max score
4. If a criterion is unclear → mark it as "ambiguous" -> is_ambiguous = true


Return STRICT JSON:

{{
  "criteria_scores": [
    {{
      "criterion": "string",
      "max_score": number,
      "score": number,
      "reason": "string",
      "is_ambiguous": true
    }}
  ],
  "final_grade": number,
  "overall_reason": "string"
}}
"""

    output = call_llm_text(prompt)
    try:
        return extract_json(output)
    except Exception as e:
        return {
            "criteria_scores": [],
            "final_grade": 0,
            "overall_reason": "Parsing failed",
            "error": str(e),
            "raw_output": output
        }



