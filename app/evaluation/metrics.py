import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import pingouin as pg


# ----------------------------
# 1. AMBIGUITY → ICC
# ----------------------------
def ambiguity_score_icc(grading_runs):
    """
    Measures inter-rater reliability using Intraclass Correlation (ICC).
    High ICC → graders agree → low ambiguity.
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

    if df["score"].nunique() <= 1:
        return 100.0  # perfect agreement edge case

    icc = pg.intraclass_corr(
        data=df,
        targets="student",
        raters="rater",
        ratings="score"
    )

    value = icc[icc["Type"] == "ICC2"]["ICC"].values

    if len(value) == 0:
        return 0.0

    return float(np.clip(value[0], 0, 1) * 100)


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
    return float((corr + 1) / 2 * 100)


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

    return float(np.clip(stability, 0, 1) * 100)


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

    return float(np.clip(1 - mean_std / overall_std, 0, 1) * 100)


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

    max_diff = max(diffs) + 1e-6
    mean_diff = np.mean(diffs)

    return float(np.clip(1 - mean_diff / max_diff, 0, 1) * 100)