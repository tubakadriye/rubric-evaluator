from app.config import MODEL_ANALYSIS
from app.llm.client import call_llm
from app.utils.json_utils import extract_json

def analyze_rubric(rubric, teaching_material):
    prompt = f"""
You are an expert in exam design.

Your task is to evaluate how well the rubric aligns with the teaching material.

RUBRIC:
{rubric}

TEACHING MATERIAL:
{teaching_material}

IMPORTANT:
- Focus on alignment with teaching
- Identify missing concepts
- Identify unclear grading rules
- Do NOT invent new criteria

Evaluate it on:

1. Ambiguity → Is the rubric formulated with the objective, unambiguous criteria?
2. Applicability → Does the rubric cover the diversity of possible student responses?
3. Discrimination → Does the rubric clearly separate excellent from poor work?

Return STRICT JSON:

{{
  "ambiguity_issues": ["..."],
  "applicability_issues": ["..."],
  "discrimination_issues": ["..."],
  "alignment_issues": ["..."]
}}
"""
    output = call_llm(prompt, model= MODEL_ANALYSIS, temperature=0.4)
    return extract_json(output)