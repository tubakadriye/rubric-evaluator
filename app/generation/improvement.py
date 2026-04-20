from app.llm.client import call_llm
from app.utils.json_utils import extract_json
from app.config import MODEL_GRADING, TEMP_GENERATION

def improve_rubric(prompt):
    out = call_llm(prompt, MODEL_GRADING, TEMP_GENERATION)
    return extract_json(out)