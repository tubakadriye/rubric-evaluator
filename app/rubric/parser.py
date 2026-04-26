import re

def parse_rubric(rubric_text):

    # split sections
    case_section = re.search(
        r"Case study.*?Grading rubric.*?(?=Penalizations:|$)",
        rubric_text,
        re.DOTALL
    )

    penalty_section = re.search(
        r"Penalizations:(.*)",
        rubric_text,
        re.DOTALL
    )

    # -----------------------
    # TASK + SCENARIO
    # -----------------------
    task_block = case_section.group(0) if case_section else rubric_text

    instructions = []
    scenario_lines = []

    for line in task_block.split("\n"):
        l = line.strip()

        if not l:
            continue

        if "choose" in l.lower() or "apply" in l.lower():
            instructions.append(l)
        elif "scenario" in l.lower() or "smartcity" in l.lower():
            scenario_lines.append(l)

    # -----------------------
    # SCORING RULES
    # -----------------------
    per_action_rules = [
        {
            "name": "category_match",
            "weight": 0.5,
            "rule": "action corresponds to category"
        },
        {
            "name": "harm_description",
            "weight": 0.5,
            "rule": "clear harmful impact + specificity to SmartCity"
        }
    ]

    # -----------------------
    # PENALTIES
    # -----------------------
    penalties = []

    if penalty_section:
        for line in penalty_section.group(1).split("\n"):
            l = line.strip()
            if "-0.5" in l:
                penalties.append({
                    "name": "similar_actions",
                    "value": -0.5,
                    "rule": l
                })
            elif "-0.25" in l:
                penalties.append({
                    "name": "weak_impact",
                    "value": -0.25,
                    "rule": l
                })

    return {
        "task": {
            "name": "Case study",
            "total_points": 3,
            "instructions": instructions,
            "scenario": "\n".join(scenario_lines)
        },
        "scoring": {
            "per_action": per_action_rules,
            "penalties": penalties
        }
    }