from app.evaluation.metrics import (
    ambiguity_score,
    discrimination_score,
    applicability_score
)


def detect_rubric_failures(grading_runs, good_scores, edge_scores, bad_scores):

    ambiguity = ambiguity_score(grading_runs)
    discrimination = discrimination_score(good_scores, edge_scores, bad_scores)
    applicability = applicability_score(grading_runs, edge_scores)

    failures = []

    if ambiguity < 80:
        failures.append({
            "type": "ambiguity",
            "message": "Grading is inconsistent across runs.",
            "score": ambiguity
        })

    if discrimination < 70:
        failures.append({
            "type": "discrimination",
            "message": "Rubric fails to reliably rank good > edge > bad.",
            "score": discrimination
        })


    if applicability < 70:
        failures.append({
            "type": "applicability",
            "message": "Rubric does not handle full diversity of answer types.",
            "score": applicability
        })

    return {
        "scores": {
            "ambiguity": round(ambiguity, 2),
            "discrimination": round(discrimination, 2),
            "applicability": round(applicability, 2)
        },
        "failures": failures
    }