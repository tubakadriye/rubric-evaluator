from app.grading.grader import grade_answer

def simulate_grading(rubric, students, runs=3):
    return [
        [grade_answer(rubric, s) for s in students]
        for _ in range(runs)
    ]