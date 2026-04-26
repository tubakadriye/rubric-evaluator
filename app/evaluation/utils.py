def extract_scores(runs, mode="all"):
    scores = []

    for run in runs:
        for r in run:
            if mode == "all":
                for model in r:
                    scores.append(r[model]["final_grade"])
            else:
                scores.append(r[mode]["final_grade"])

    return scores