
import asyncio
from app.evaluation.metrics import consistency_score, cross_model_consistency
from app.evaluation.utils import extract_scores
from app.grading.aggregation import aggregate, aggregate_multi, summarize_runs
from app.grading.simulation import build_rater_runs, simulate_all
from app.generation.synthetic import generate_synthetic_answers
from app.evaluation.failure_detection import detect_rubric_failures
from app.rubric.parser import parse_rubric
from app.rubric.analysis import analyze_rubric
from app.generation.improvement import improve_rubric
from app.hitl.review import human_review


def build_prompt(rubric, rubric_structured, teaching, students, aggregated_summary, consistency, cross_model_score, evaluation, rubric_analysis):

    student_block = "\n\n".join(
        [f"Student {i+1}:\n{s}" for i, s in enumerate(students)]
    )

    return f"""
You are an expert exam designer.

TASK:
Improve the grading rubric using MULTIPLE sources of evidence based on the following goals.

--- INPUTS ---

RUBRIC:
{rubric}

STRUCTURED RUBRIC
{rubric_structured}

RUBRIC ANALYSIS:
{rubric_analysis}

TEACHING MATERIAL:
{teaching}

STUDENT ANSWERS:
{student_block}

AGGREGATED SUMMARY
{aggregated_summary}

CONSISTENCY SCORE
{consistency}

CROSS-MODEL-CONSISTENCY
{cross_model_score}

EVALUATION:
{evaluation}

FAILURES DETECTED:
{evaluation["failures"]}

WARNINGS:
{evaluation["warnings"]}

INSIGHTS:
{evaluation["insights"]}


--- TASK ---

Improve the rubric by:
- Reducing ambiguity (make criteria precise)
- Increasing applicability (cover more answer types)
- Improving discrimination (differentiate quality levels)

Goals:
1. Ambiguity → All the graders reach the same interpretation independently.
2. Applicability → No valid answer type is left unaddressed by the rubric.
3. Discrimination → High-quality answers score significantly better than weak ones.

INTERPRETATION GUIDELINES:

- If ambiguity is high but cross-model consistency is low:
  → criteria wording is ambiguous, not precise enough

- If applicability is low:
  → rubric is missing rules for borderline answers

- If discrimination is high but top scores have low variance:
  → rubric lacks granularity at high performance levels

- If edge cases show inconsistent scores:
  → scoring boundaries are not clearly defined

Use these signals to:
- rewrite vague criteria into measurable rules
- define clear scoring boundaries
- add examples for borderline cases

Use these signals to identify concrete weaknesses in rubric design.

OUTPUT STRICT JSON:
{{
  "improved_rubric": "...",
  "explanation": {{
    "ambiguity": "...",
    "applicability": "...",
    "discrimination": "..."
  }}
}}
"""


def run_pipeline(rubric, teaching, students):

    # 1. STRUCTURE
    rubric_structured = parse_rubric(rubric)

    # 2. ANALYZE
    rubric_analysis = analyze_rubric(rubric, teaching)

    # 3. SYNTHETIC
    synthetic = generate_synthetic_answers(teaching, rubric)

    # 4. RUN ALL SIMULATIONS (ASYNC)
    grading_runs_multi, good_runs_multi, bad_runs_multi, edge_runs_multi = asyncio.run(
        simulate_all(rubric, students, synthetic)
    )

    # 5. 
    openai_runs = [[r["openai"] for r in run] for run in grading_runs_multi]
    all_raters = build_rater_runs(grading_runs_multi)

    # 6. AGGREGATION
    #aggregated = aggregate(openai_runs)
    aggregated = aggregate_multi(grading_runs_multi)
    aggregated_summary = summarize_runs(aggregated)

    # 7. CONSISTENCY
    consistency = consistency_score(openai_runs)

    # 8. CROSS MODEL
    flat_multi = [r for run in grading_runs_multi for r in run]
    cross_model_score = cross_model_consistency(flat_multi)

    # 9. EXTRACT SCORES
    good_scores = extract_scores(good_runs_multi)
    bad_scores  = extract_scores(bad_runs_multi)
    edge_scores = extract_scores(edge_runs_multi)

    # 10. EVALUATION
    evaluation = detect_rubric_failures(
        all_raters, #openai_runs,
        good_scores,
        edge_scores,
        bad_scores, 
        cross_model_score
    )

    # 11. PROMPT
    prompt = build_prompt(
        rubric,
        rubric_structured,
        teaching,
        students,
        aggregated_summary,   
        consistency,
        cross_model_score,
        evaluation,
        rubric_analysis
    )

    improved = improve_rubric(prompt)

    # 12. HUMAN REVIEW
    improved = human_review(improved)

    return {
#        "rubric_analysis": rubric_analysis,
        # "evaluation": evaluation,
        # "consistency": consistency,
        # "cross_model_consistency": cross_model_score,
        # "aggregated_scores": aggregated,
        "improved_rubric": improved.get("improved_rubric", ""),
        "explanation": improved.get("explanation", {})
    }