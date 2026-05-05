import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import pingouin as pg


# ----------------------------
# 1. AMBIGUITY → ICC
# ----------------------------
def ambiguity_score_icc(grading_runs):
    """
    Measures inter-rater reliability using ICC.
    High ICC → low ambiguity.

    Uses:
    - ICC(A,1) → agreement between individual raters (preferred)
    - fallback: ICC(A,k)

    Returns score in [0,100]
    """

    data = []

    for r_idx, run in enumerate(grading_runs):
        for s_idx, g in enumerate(run):
            data.append({
                "student": s_idx,
                "rater": r_idx,
                "score": g.get("final_grade", 0)
            })

    df = pd.DataFrame(data)

    # Edge case: no variance → perfect agreement
    if df["score"].nunique() <= 1:
        return 100.0

    icc = pg.intraclass_corr(
        data=df,
        targets="student",
        raters="rater",
        ratings="score"
    )


    row = icc[icc["Type"].isin(["ICC(A,1)", "ICC(A,k)"])]

    row = icc[icc["Type"] == "ICC(A,1)"]

    if row.empty:
        row = icc[icc["Type"] == "ICC(A,k)"]

    if row.empty:
        return 0.0

    value = row["ICC"].iloc[0]

    # Clamp to valid ICC range
    value = max(-1.0, min(1.0, float(value)))

    # Map [-1,1] → [0,100]
    score = (value + 1) / 2 * 100
    return score


# ----------------------------
# 2. DISCRIMINATION → SPEARMAN
# ----------------------------
def discrimination_score_spearman(good, edge, bad):
    """
    Measures whether ranking is preserved:
    good > edge > bad using Spearman correlation.
    """

    scores = good + edge + bad

    # labels: good=2, edge=1, bad=0
    labels = (
        [2] * len(good) +
        [1] * len(edge) +
        [0] * len(bad)
    )

    if len(scores) < 2:
        return 0.0

    corr, _ = spearmanr(scores, labels)

    if np.isnan(corr):
        return 0.0

    # map [-1,1] → [0,100]
    score = float((corr + 1) / 2 * 100)
    return score


# ----------------------------
# 3. APPLICABILITY → EDGE VARIANCE
# ----------------------------
def applicability_score(edge_scores, grading_runs):
    """
    Measures how rubric handles edge cases.
    Uses standard deviation:
    - too low → rigid
    - too high → unstable
    Ideal → moderate variance
    """

    if not edge_scores:
        return 0.0

    std = np.std(edge_scores)

    overall_std = np.std([
        g["final_grade"]
        for run in grading_runs
        for g in run
    ]) + 1e-6

    stability = 1 - (std / overall_std)
    score = float(np.clip(stability, 0, 1) * 100)

    return score


# ----------------------------
# 4. CONSISTENCY → STD ACROSS RUNS
# ----------------------------
def consistency_score(grading_runs):
    """
    Measures within-model consistency (across runs).
    """

    stds = []

    for i in range(len(grading_runs[0])):
        vals = [r[i]["final_grade"] for r in grading_runs]
        stds.append(np.std(vals))

    mean_std = np.mean(stds)

    overall_std = np.std([
        g["final_grade"]
        for run in grading_runs
        for g in run
    ]) + 1e-6

    stability = 1 - (mean_std / overall_std)
    score = float(np.clip(stability, 0, 1) * 100)

    return score


# ----------------------------
# 5. CROSS-MODEL CONSISTENCY
# ----------------------------
def cross_model_consistency(results):
    """
    Measures agreement between OpenAI and Claude.
    """

    diffs = []

    for r in results:
        o = r["openai"].get("final_grade", 0)
        c = r["claude"].get("final_grade", 0)
        diffs.append(abs(o - c))

    if not diffs:
        return 100.0

    mean_diff = np.mean(diffs)
    std_diff = np.std(diffs)

    score = 1 - (mean_diff / (mean_diff + std_diff + 1e-6))
    return float(np.clip(score, 0, 1) * 100)