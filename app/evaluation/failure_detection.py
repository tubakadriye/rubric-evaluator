from app.evaluation.metrics import (
    ambiguity_score_icc,
    discrimination_score_spearman,
    applicability_score
)


def detect_rubric_failures(grading_runs, good_scores, edge_scores, bad_scores):

    ambiguity = ambiguity_score_icc(grading_runs)
    discrimination = discrimination_score_spearman(good_scores, edge_scores, bad_scores)
    applicability = applicability_score(edge_scores, grading_runs)

    failures = []

    if ambiguity < 70:
        failures.append({
            "type": "ambiguity",
            "message": "Low inter-rater agreement (ICC).",
            "score": ambiguity
        })

    if discrimination < 60:
        failures.append({
            "type": "discrimination",
            "message": "Ranking between good, edge, bad is weak.",
            "score": discrimination
        })

    if applicability < 50:
        failures.append({
            "type": "applicability",
            "message": "Rubric does not generalize well to edge cases.",
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