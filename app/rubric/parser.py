from app.config import MODEL_ANALYSIS
from app.llm.client import call_llm
from app.utils.json_utils import extract_json


def parse_rubric(rubric_text: str, rubric_analysis: dict = None):
    """
    LLM-based rubric parser that extracts implicit grading criteria.

    Handles rubrics that do NOT explicitly list criteria.
    """

    analysis_block = ""
    if rubric_analysis:
        analysis_block = f"""
RUBRIC ANALYSIS (for context only — DO NOT convert into criteria):
{rubric_analysis}
"""

    prompt = f"""
You are an expert in exam rubric design.

Your task is to extract the TRUE grading criteria from the rubric.

IMPORTANT:
- The rubric may NOT explicitly list criteria
- You must INFER them from scoring rules
- DO NOT use meta concepts like "ambiguity", "applicability", "discrimination"
- Extract ONLY grading-relevant dimensions

WHAT IS A CRITERION:
A criterion is an independent dimension used to assign points.

---

EXAMPLE:

Rubric:
"1 point for correct category, 1 point for clear explanation"

Output:
[
  "category correctness",
  "explanation quality"
]

---

TASK:

Extract:

1. Task instructions
2. Scenario/context
3. Grading criteria (inferred)
4. Penalties (if any)

Each criterion must:
- be independent
- be usable for grading
- correspond to how points are assigned

---

Return STRICT JSON:

{{
  "task": {{
    "instructions": ["..."],
    "scenario": "..."
  }},
  "criteria": [
    {{
      "name": "short label",
      "description": "what is being evaluated",
      "max_score": number
    }}
  ],
  "penalties": [
    {{
      "description": "...",
      "value": number
    }}
  ]
}}

---

RUBRIC:
{rubric_text}

{analysis_block}
"""

    output = call_llm(prompt, model=MODEL_ANALYSIS, temperature=0.0)

    return extract_json(output)