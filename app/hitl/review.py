import json

def human_review(result):

    print("\n=== IMPROVED RUBRIC ===\n")
    print(result["improved_rubric"])

    print("\n=== EXPLANATION ===\n")
    print(json.dumps(result["explanation"], indent=2))

    choice = input("\nApprove? (y/n): ")

    if choice.lower() == "y":
        result["human_verified"] = True
        return result

    print("\nEdit rubric:")
    result["improved_rubric"] = input(">")

    print("\nEdit explanation JSON:")
    try:
        result["explanation"] = json.loads(input(">"))
    except:
        pass

    result["human_verified"] = True
    return result