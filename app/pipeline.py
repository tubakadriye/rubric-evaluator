
from app.evaluation.metrics import consistency_score
from app.grading.aggregation import aggregate
from app.grading.simulation import simulate_grading
from app.generation.synthetic import generate_synthetic_answers
from app.evaluation.metrics import *
from app.evaluation.failure_detection import detect_rubric_failures
from app.rubric.parser import parse_rubric
from app.rubric.analysis import analyze_rubric
from app.generation.improvement import improve_rubric
from app.hitl.review import human_review


def build_prompt(rubric, rubric_structured, teaching, students, grading_runs, aggregated, consistency, evaluation, rubric_analysis):

    student_block = "\n\n".join(
        [f"Student {i+1}:\n{s}" for i, s in enumerate(students)]
    )

    return f"""
You are an expert exam designer.

TASK:
Improve the grading rubric using MULTIPLE sources of evidence baesd on the following goals.

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

GRADING RUNS:
{grading_runs}

AGGREGATED SCORES 
{aggregated}

CONSISTENCY SCORE
{consistency}

EVALUATION:
{evaluation}

FAILURES DETECTED:
{evaluation["failures"]}

--- TASK ---

Improve the rubric by:
- Reducing ambiguity (make criteria precise)
- Increasing applicability (cover more answer types)
- Improving discrimination (differentiate quality levels)

Goals:
1. Ambiguity → All the graders reach the same interpretation independently.
2. Applicability → No valid answer type is left unaddressed by the rubric.
3. Discrimination → High-quality answers score significantly better than weak ones.

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
    # 1. STRUCTURE RUBRIC 
    rubric_structured = parse_rubric(rubric)

    # 2. ANALYZE RUBRIC
    rubric_analysis = analyze_rubric(rubric, teaching)

    # 3. SIMULATE GRADING
    grading_runs = simulate_grading(rubric, students)

    # 4. AGGREGATE 
    aggregated = aggregate(grading_runs)

    # 5. CONSISTENCY 
    consistency = consistency_score(grading_runs)

    # 6. SYNTHETIC
    synthetic = generate_synthetic_answers(teaching, rubric)

    good_runs = simulate_grading(rubric, synthetic["good"])
    bad_runs = simulate_grading(rubric, synthetic["bad"])
    edge_runs = simulate_grading(rubric, synthetic["edge"])

    good_scores = [g["final_grade"] for r in good_runs for g in r]
    bad_scores = [g["final_grade"] for r in bad_runs for g in r]
    edge_scores = [g["final_grade"] for r in edge_runs for g in r]


    # 7. EVALUATION
    evaluation = detect_rubric_failures(
        grading_runs,
        good_scores,
        edge_scores,
        bad_scores
    )

    # 8. IMPROVE RUBRIC
    prompt = build_prompt(
        rubric,
        rubric_structured,
        teaching,
        students,
        grading_runs,
        aggregated,
        consistency,
        evaluation,
        rubric_analysis
        )
    
    improved = improve_rubric(prompt)

    # 9. HUMAN IN THE LOOP HERE
    improved = human_review(improved)

    return {
       "rubric_analysis": rubric_analysis,
        "evaluation": evaluation,
        "consistency": consistency,
        "aggregated_scores": aggregated,
        "improved_rubric": improved.get("improved_rubric", ""),
        "explanation": improved.get("explanation", {})
    }