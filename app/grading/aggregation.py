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

def summarize_runs(aggregated):
    return [
        f"Student {i+1}: mean={a['mean']:.1f}, std={a['std']:.1f}"
        for i, a in enumerate(aggregated)
    ]


def aggregate_multi(grading_runs_multi):
    result = []

    num_students = len(grading_runs_multi[0])

    for i in range(num_students):
        scores = []

        for run in grading_runs_multi:
            scores.append(run[i]["openai"].get("final_grade", 0))
            scores.append(run[i]["claude"].get("final_grade", 0))

        result.append({
            "mean": float(np.mean(scores)),
            "std": float(np.std(scores)),
            "min": float(np.min(scores)),
            "max": float(np.max(scores))
        })

    return result