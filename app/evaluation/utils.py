def extract_scores(runs, model="openai"):
    return [
        r[model]["final_grade"]
        for run in runs
        for r in run
    ]