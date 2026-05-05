# app/grading/grader_async.py

import asyncio
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from app.utils.json_utils import extract_json
from app.config import OPENAI_API_KEY, ANTHROPIC_API_KEY

openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
claude_client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)


def build_prompt(rubric, answer, rag):
    #context = rag.retrieve(answer)

    contexts = rag.retrieve_per_criterion(rubric)

    context_block = "\n\n".join([
        f"{c['criterion']}:\n{c['context']}"
        for c in contexts
    ])


    return f"""
Strict grader.

RUBRIC:
{rubric}

CRITERION-SPECIFIC CONTEXT:
{context_block}


ANSWER:
{answer}

Rules:
- Use rubric to grade
- Use teaching context as reference for correctness
- Do NOT invent criteria
- Do NOT use outside knowledge
- Final grade MUST be the sum of criterion scores
- Do NOT exceed max scores

Return STRICT JSON:
{{
  "criteria_scores": [
    {{
      "criterion": "string",
      "max_score": number,
      "score": number,
      "reason": "string"
    }}
  ],
  "final_grade": number,
  "overall_reason": "string"
}}
"""


#     return f"""
# Strict grader.

# RUBRIC:
# {rubric}

# RELEVANT TEACHING CONTEXT:
# {context}

# ANSWER:
# {answer}

# Rules:
# - Use rubric strictly
# - Use context to verify correctness
# - Do NOT hallucinate missing concepts

# Return STRICT JSON:

# {{
#   "criteria_scores": [
#     {{
#       "criterion": "string",
#       "max_score": number,
#       "score": number,
#       "reason": "string",
#       "is_ambiguous": true
#     }}
#   ],
#   "final_grade": number,
#   "overall_reason": "string"
# }}
# """


async def grade_answer_openai_async(rubric, answer, rag):
    prompt = build_prompt(rubric, answer, rag)

    res = await openai_client.responses.create(
        model="gpt-4.1",
        input=prompt,
        temperature=0.0
    )
    try:
        return extract_json(res.output_text)
    except Exception as e:
        return {
            "criteria_scores": [],
            "final_grade": 0,
            "overall_reason": "Parsing failed",
            "error": str(e),
            "raw_output": res.output_text
        }


async def grade_answer_claude_async(rubric, answer, rag):
    prompt = build_prompt(rubric, answer, rag)

    res = await claude_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        return extract_json(res.content[0].text)
    except Exception as e:
        return {
            "criteria_scores": [],
            "final_grade": 0,
            "overall_reason": "Parsing failed",
            "error": str(e),
            "raw_output": res.content[0].text
        }


async def grade_student(rubric, answer, rag):
    o, c = await asyncio.gather(
        grade_answer_openai_async(rubric, answer, rag),
        grade_answer_claude_async(rubric, answer, rag)
    )

    return {"openai": o, "claude": c}