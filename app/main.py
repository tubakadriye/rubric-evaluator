from app.extractors.rubric import extract_rubric
from app.extractors.student_answers import extract_student_transcription
from app.extractors.teaching_resource import extract_teaching_material
from app.pipeline import run_pipeline
import json
import argparse


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--rubric", required=True)
    parser.add_argument("--teaching", required=True)
    parser.add_argument("--students", nargs="+", required=True)

    args = parser.parse_args()

    rubric = extract_rubric(args.rubric)
    teaching = extract_teaching_material(args.teaching)
    students = extract_student_transcription(args.students)

    result = run_pipeline(rubric, teaching, students)

    print(json.dumps(result, indent = 2))
    
    with open("output.json", "w") as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    main()