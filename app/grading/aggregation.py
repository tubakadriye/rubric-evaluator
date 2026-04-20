import numpy as np

def aggregate(grading_runs):
    result = []

    for i in range(len(grading_runs[0])):
        scores = [run[i]["final_grade"] for run in grading_runs]

        result.append({
            "mean": float(np.mean(scores)),
            "std": float(np.std(scores)),
            "min": float(np.min(scores)),
            "max": float(np.max(scores))
        })

    return result