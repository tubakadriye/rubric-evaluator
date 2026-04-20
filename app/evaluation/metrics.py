import numpy as np
from itertools import combinations

def ambiguity_score(runs):
    total, diff = 0, 0

    for r1, r2 in combinations(runs, 2):
        for g1, g2 in zip(r1, r2):
            c1 = {c["criterion"]: c["score"] for c in g1.get("criteria_scores", [])}
            c2 = {c["criterion"]: c["score"] for c in g2.get("criteria_scores", [])}

            for k in set(c1) | set(c2):
                total += 1
                diff += abs(c1.get(k, 0) - c2.get(k, 0))

    return max(0, 100 - (diff / max(total,1)) * 100)


def discrimination_score(good, edge, bad):
    """
    Measures whether rubric preserves correct ranking:
    good > edge > bad
    """

    g, e, b = np.mean(good), np.mean(edge), np.mean(bad)


    # ranking correctness
    correct_order = int(g > e > b)

    # margins 
    margin_ge = g - e
    margin_eb = e - b

    margin_score = max(0, (margin_ge + margin_eb) * 50)

    return min(100, correct_order * 50 + margin_score)


def applicability_score(runs, edge_scores):
    coverage = len(edge_scores) / max(len(runs) * 10, 1)
    return min(100, coverage * 100)


def consistency_score(runs):
    stds = []
    for i in range(len(runs[0])):
        vals = [r[i]["final_grade"] for r in runs]
        stds.append(np.std(vals))
    return max(0, 100 - np.mean(stds)*50)

