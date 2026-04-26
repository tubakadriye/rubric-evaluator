from app.evaluation.metrics import (
    ambiguity_score_icc,
    discrimination_score_spearman,
    applicability_score
)
import numpy as np


def detect_rubric_failures(grading_runs, good_scores, edge_scores, bad_scores, cross_model_score):

    ambiguity = ambiguity_score_icc(grading_runs)
    discrimination = discrimination_score_spearman(good_scores, edge_scores, bad_scores)
    applicability = applicability_score(edge_scores, grading_runs)

    failures = []
    warnings = []
    insights = []

    # ----------------------------
    # 🚨 HARD FAILURES (rubric is broken)
    # ----------------------------

    if ambiguity < 75:
        failures.append({
            "type": "ambiguity",
            "message": "Low inter-rater agreement (ICC).",
            "score": ambiguity
        })

    if discrimination < 70:
        failures.append({
            "type": "discrimination",
            "message": "Rubric cannot distinguish good vs bad answers.",
            "score": discrimination
        })

    if applicability < 60:
        failures.append({
            "type": "applicability",
            "message": "Rubric fails on edge cases (too rigid or incomplete).",
            "score": applicability
        })

    if cross_model_score < 50:
        failures.append({
            "type": "cross_model",
            "message": "Severe disagreement between models → rubric highly ambiguous.",
            "score": cross_model_score
        })

    # ----------------------------
    # ⚠️ WARNINGS (subtle weaknesses)
    # ----------------------------

    # 1. Score saturation (important!)
    if ambiguity > 90 and np.std(good_scores) < 0.1:
        warnings.append({
            "type": "saturation",
            "message": "Top scores have near-zero variance → rubric too coarse or dataset too easy."
        })

    # 2. Cross-model disagreement (key signal)
    if 50 <= cross_model_score < 70:
        warnings.append({
            "type": "cross_model",
            "message": "Moderate disagreement between models → rubric wording ambigous."
        })

    # 3. Weak edge handling
    if 50 <= applicability < 70:
        warnings.append({
            "type": "edge_cases",
            "message": "Edge cases inconsistently graded → rubric lacks precision."
        })

    # 4. Overfitting to clear cases
    if discrimination > 90 and applicability < 70:
        warnings.append({
            "type": "overfit",
            "message": "Rubric works well for clear cases but struggles on borderline answers."
        })

    # 5. Hidden Ambiguity
    if ambiguity > 90 and cross_model_score < 70:
        warnings.append({
        "type": "hidden_ambiguity",
        "message": "High agreement within runs but disagreement across models → rubric wording unclear."
    })

     # ----------------------------
    # 🧠 INTERPRETABILITY INSIGHTS
    # ----------------------------

    if ambiguity > 90 and cross_model_score < 70:
        insights.append(
            "High agreement within model but disagreement across models → hidden ambiguity in wording."
        )

    if discrimination > 90 and np.std(good_scores) < 0.1:
        insights.append(
            "High discrimination but saturated top scores → rubric lacks granularity at high end."
        )

    if applicability < 70:
        insights.append(
            "Edge cases reveal missing rules or unclear boundaries in rubric."
        )


    return {
        "scores": {
            "ambiguity": round(ambiguity, 2),
            "discrimination": round(discrimination, 2),
            "applicability": round(applicability, 2),
            "cross_model": round(cross_model_score, 2)
        },
        "failures": failures, 
        "warnings" : warnings,
        "insights": insights
    }