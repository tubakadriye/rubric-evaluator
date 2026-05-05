import asyncio
from app.grading.grader_async import grade_student


async def simulate_grading_async(rubric, rubric_structured, students, rag, runs=3):
    all_runs = []

    for _ in range(runs):
        tasks = [grade_student(rubric, rubric_structured, s, rag) for s in students]
        results = await asyncio.gather(*tasks)
        all_runs.append(results)

    return all_runs


async def simulate_all(rubric, rubric_structured, students, synthetic, rag):
    return await asyncio.gather(
        simulate_grading_async(rubric, rubric_structured, students, rag),
        simulate_grading_async(rubric, rubric_structured, synthetic["good"], rag),
        simulate_grading_async(rubric, rubric_structured, synthetic["bad"], rag),
        simulate_grading_async(rubric, rubric_structured, synthetic["edge"], rag)
    )


def build_rater_runs(grading_runs_multi):
    """
    Converts:
    runs x students x models

    → raters x students

    Each (run, model) = one rater for ICC
    """
    runs = []

    for run in grading_runs_multi:
        runs.append([r["openai"] for r in run])
        runs.append([r["claude"] for r in run])

    return runs